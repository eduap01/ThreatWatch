import asyncio
import json
import os
import hashlib
import datetime

from aio_pika import connect_robust
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from backend.app.api.file_analysis import scan_with_virustotal
from backend.app.core.database import Base
from backend.app.models.file import FileAnalysis


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

# DB engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async def handle_message(message):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            file_id = data["file_id"]
            filename = data["filename"]
            sha256 = data["sha256"]
            content = data["content"].encode("latin1")  # recupera el binario original

            print(f"Recibido: {filename} (sha256: {sha256})")

            # Analizar con VirusTotal
            result_summary = await scan_with_virustotal(content)

            # Guardar resultado en BDD
            db = SessionLocal()
            file_record = db.query(FileAnalysis).filter(FileAnalysis.id == file_id).first()
            if file_record:
                file_record.result_summary = result_summary
                file_record.analyzed_at = datetime.datetime.utcnow()
                db.commit()
                print(f"Resultado guardado: {result_summary}")
            db.close()

        except Exception as e:
            print(f"Error procesando mensaje: {e}")

async def main():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("file_analysis", durable=True)
    print("Esperando mensajes...")
    await queue.consume(handle_message)

if __name__ == "__main__":
    asyncio.run(main())
