from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum
class UserRole(str, enum.Enum): ADMIN = "admin"; EDITOR = "editor"; REVIEWER = "reviewer"
class DocumentStatus(str, enum.Enum): DRAFT = "draft"; REVIEW = "review"; APPROVED = "approved"; PUBLISHED = "published"
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EDITOR)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    versions = relationship("Version", back_populates="document")
class Version(Base):
    __tablename__ = "versions"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    version_number = Column(String)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    file_path = Column(String, nullable=True)
    diff_report = Column(Text, nullable=True)
    validation_report = Column(Text, nullable=True)
    is_automatic_version = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    document = relationship("Document", back_populates="versions")
    notes = relationship("Note", back_populates="version")
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("versions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    version = relationship("Version", back_populates="notes")
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(Integer)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class AuthorisedSMR(Base):
    __tablename__ = "authorised_smrs"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    version = Column(String)
    is_authorised = Column(Boolean, default=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
