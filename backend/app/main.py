from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os, shutil
from . import models, schemas, database
from .utils import auth, executor, validator, diff, versioning, smr, audit
from .database import get_db

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/api/auth/login", response_model=schemas.Token)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, email, password)
    if not user: raise HTTPException(401)
    return {"access_token": auth.create_access_token(data={"sub": user.id}), "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserOut)
async def get_me(current_user = Depends(auth.get_current_user)): return current_user

@app.post("/api/documents", response_model=schemas.DocumentOut)
async def create_document(doc: schemas.DocumentCreate, current_user = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    new_doc = models.Document(name=doc.name, created_by=current_user.id)
    db.add(new_doc); db.commit(); db.refresh(new_doc)
    audit.log_audit(db, current_user.id, "create_document", "document", new_doc.id, {"name": doc.name})
    return new_doc

@app.get("/api/documents", response_model=List[schemas.DocumentOut])
async def list_documents(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    return db.query(models.Document).all()

@app.post("/api/documents/{doc_id}/upload_previous")
async def upload_previous(doc_id: int, file: UploadFile = File(...), name: str = Form(...), current_user = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not doc: raise HTTPException(404)
    upload_dir = f"/app/uploads/previous/{doc_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    version = models.Version(document_id=doc_id, version_number="v0.1", file_path=file_path)
    db.add(version); db.commit()
    audit.log_audit(db, current_user.id, "upload_previous", "document", doc_id, {"file": file.filename})
    return {"version_id": version.id}
