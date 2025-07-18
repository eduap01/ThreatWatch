import datetime
import hashlib
import asyncio
import os

import httpx
import traceback

from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.file import FileAnalysis
from backend.app.schemas.file import FileAnalysisOut
from backend.app.services.producer import send_analysis_task

router = APIRouter(prefix="/files", tags=["files"])

load_dotenv()
VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

async def scan_with_virustotal(content: bytes) -> str:
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
            return f"Error uploading to VT: {upload_response.text}"

        analysis_id = upload_response.json()["data"]["id"]

        await asyncio.sleep(10)

        async with httpx.AsyncClient() as client:
            analysis_response = await client.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers=headers
            )

        if analysis_response.status_code != 200:
            return f"Error fetching results: {analysis_response.text}"

        stats = analysis_response.json()["data"]["attributes"]["stats"]
        if stats["malicious"] > 0:
            return f"Infected (malicious: {stats['malicious']})"
        else:
            return "Clean"

    except Exception as e:
        print(f"VT scan error: {e}")
        traceback.print_exc()
        return "error during VT scan"


@router.post("/upload", response_model=FileAnalysisOut)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        sha256 = hashlib.sha256(content).hexdigest()

        # Verificar si ya está analizado
        existing = db.query(FileAnalysis).filter(FileAnalysis.sha256 == sha256).first()
        if existing:
            return FileAnalysisOut.from_attributes(existing)

        # Guardar el archivo en la base de datos con estado "pendiente"
        file_record = FileAnalysis(
            filename=file.filename,
            content_type=file.content_type,
            sha256=sha256,
            result_summary="Pending",
            uploaded_at=datetime.datetime.utcnow()
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)

        # Enviar tarea a RabbitMQ
        await send_analysis_task({
            "file_id": file_record.id,
            "filename": file.filename,
            "sha256": sha256,
            "content": content.decode("latin1")  # codifica binario a string temporalmente
        })

        return FileAnalysisOut.from_attributes(file_record)

    except Exception as e:
        print(f"Error uploading file: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal error uploading file")
