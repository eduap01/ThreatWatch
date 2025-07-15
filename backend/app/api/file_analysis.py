import datetime
import hashlib
import traceback

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.file import FileAnalysis
from backend.app.schemas.file import FileAnalysisOut

router = APIRouter(prefix="/files", tags=["files"])

import logging

@router.post("/upload", response_model=FileAnalysisOut)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        sha256 = hashlib.sha256(content).hexdigest()

        existing = db.query(FileAnalysis).filter(FileAnalysis.sha256 == sha256).first()
        if existing:
            return FileAnalysisOut.from_attributes(existing)

        result_summary = "Clean" if b"virus" not in content else "Infected"

        file_record = FileAnalysis(
            filename=file.filename,
            content_type=file.content_type,
            sha256=sha256,
            result_summary=result_summary,
            uploaded_at=datetime.utcnow()
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        return FileAnalysisOut.from_attributes(file_record)

    except Exception as e:
        print(f"Error uploading file: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Internal error uploading file")


