from .database import engine, SessionLocal
from . import models
from .utils.auth import get_password_hash
def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if not admin:
        admin = models.User(email="admin@example.com", hashed_password=get_password_hash("admin123"), role=models.UserRole.ADMIN)
        db.add(admin)
    smr = db.query(models.AuthorisedSMR).filter(models.AuthorisedSMR.is_authorised == True).first()
    if not smr:
        default_smr = models.AuthorisedSMR(content="Visibility Rule: All reasoning steps must be visible.\nNon-Tacit Rule: No implicit behaviors.\nNo Cross-Version Referencing.\nSelf-Audit: Check compliance.\nEvidence Requirements: Explicit evidence.", version="v1.0", is_authorised=True, uploaded_by=admin.id if admin else 1)
        db.add(default_smr)
    db.commit()
    db.close()
    print("Initialized with admin: admin@example.com / admin123")
if __name__ == "__main__":
    init_db()
