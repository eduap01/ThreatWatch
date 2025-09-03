import datetime
import hashlib
import asyncio
import os
import json

import httpx
import traceback

from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.redis import redis_client
from backend.app.models.file import FileAnalysis
from backend.app.schemas.file import FileAnalysisOut
from backend.app.services.producer import send_analysis_task

router = APIRouter(prefix="/files", tags=["files"])

load_dotenv()
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

async def heuristic_analysis(content: bytes) -> dict:
    try:
        headers = {
            "x-apikey": VT_API_KEY
        }
        files = {"file": ("file", content)}

        async with httpx.AsyncClient() as client:
            upload_response = await client.post(
                "https://www.virustotal.com/api/v3/files",
                headers=headers,
                files=files
            )

        if upload_response.status_code != 200:
            return {"error": f"Error uploading to VT: {upload_response.text}"}

        analysis_id = upload_response.json()["data"]["id"]

        await asyncio.sleep(10)

        async with httpx.AsyncClient() as client:
            analysis_response = await client.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers=headers
            )

        if analysis_response.status_code != 200:
            return {"error": f"Error fetching results: {analysis_response.text}"}

        stats = analysis_response.json()["data"]["attributes"]["stats"]
        # Devolvemos todo el resultado de forma estructurada
        return {
            "status": "Infected" if stats["malicious"] > 0 else "Clean",
            "malicious": stats.get("malicious", 0),
            "undetected": stats.get("undetected", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0)
        }

    except Exception as e:
        print(f"VT scan error: {e}")
        traceback.print_exc()
        return {"error": "error during VT scan"}



@router.post("/upload", response_model=FileAnalysisOut)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        sha256 = hashlib.sha256(content).hexdigest()

        existing = db.query(FileAnalysis).filter(FileAnalysis.sha256 == sha256).first()
        if existing:
            return FileAnalysisOut.model_validate(existing, from_attributes=True)

        file_record = FileAnalysis(
            filename=file.filename,
            content_type=file.content_type,
            sha256=sha256,
            content=content,
            result_summary="Pending",
            uploaded_at=datetime.datetime.utcnow()
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        await send_analysis_task({
            "file_id": file_record.id,
            "filename": file.filename,
            "sha256": sha256,
            "content": content.decode("latin1")
        })

        return FileAnalysisOut.model_validate(file_record, from_attributes=True)

    except Exception as e:
        print(f"Error uploading file: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error uploading file")


@router.get("/files/{file_id}", response_model=FileAnalysisOut)
def get_file_analysis(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileAnalysis).filter(FileAnalysis.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File analysis not found")
    return file_record

@router.get("/analyze/{file_id}", response_model=FileAnalysisOut)
async def analyze_file_by_id(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileAnalysis).filter(FileAnalysis.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Ejecuta heurístico propio
    result_summary = heuristic_analysis(file_record.content, file_record.filename)

    status = result_summary["classification"]

    # Guarda el estado en Redis
    redis_client.set(f"file:{file_id}:status", status)
    redis_client.set(f"file:{file_id}:summary", json.dumps(result_summary))

    # Actualiza la base de datos
    file_record.result_summary = json.dumps(result_summary)
    file_record.analyzed_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(file_record)

    return FileAnalysisOut.from_orm(file_record)


##Endpoint para consultar estado
@router.get("/files/{file_id}/status", response_model=dict)
def get_file_status(file_id: int):
    status = redis_client.get(f"file:{file_id}:status")
    if not status:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return {"file_id": file_id, "status": status}


