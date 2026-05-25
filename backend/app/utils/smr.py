from sqlalchemy.orm import Session
from .. import models
def get_authorised_smr(db: Session) -> str:
    smr = db.query(models.AuthorisedSMR).filter(models.AuthorisedSMR.is_authorised == True).first()
    if smr: return smr.content
    return """Visibility Rule: All reasoning steps must be visible.\nNon-Tacit Rule: No implicit behaviors.\nNo Cross-Version Referencing.\nSelf-Audit: Check compliance.\nEvidence Requirements: Explicit evidence."""
