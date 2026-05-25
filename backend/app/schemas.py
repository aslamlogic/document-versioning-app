from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import UserRole, DocumentStatus
class UserBase(BaseModel): email: EmailStr
class UserCreate(UserBase): password: str; role: Optional[UserRole] = UserRole.EDITOR
class UserOut(UserBase): id: int; role: UserRole; created_at: datetime; class Config: from_attributes = True
class Token(BaseModel): access_token: str; token_type: str
class DocumentCreate(BaseModel): name: str
class DocumentOut(BaseModel): id: int; name: str; created_by: int; created_at: datetime; class Config: from_attributes = True
class VersionCreate(BaseModel): version_number: str; is_automatic_version: bool = True
class VersionOut(BaseModel): id: int; document_id: int; version_number: str; status: DocumentStatus; file_path: Optional[str]; diff_report: Optional[str]; validation_report: Optional[str]; is_automatic_version: bool; created_at: datetime; class Config: from_attributes = True
class NoteCreate(BaseModel): content: str
class NoteOut(BaseModel): id: int; version_id: int; user_id: int; content: str; created_at: datetime
class SMRCreate(BaseModel): content: str; version: str
class SMROut(BaseModel): id: int; content: str; version: str; is_authorised: bool; uploaded_at: datetime
