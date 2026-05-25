from sqlalchemy.orm import Session
from .. import models
def log_audit(db: Session, user_id: int, action: str, entity_type: str, entity_id: int, metadata: dict = None):
    db.add(models.AuditLog(user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id, metadata=metadata or {}))
    db.commit()
