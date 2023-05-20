from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.job_offer import JobOffer
from app.schemas.job_offer import JobOfferCreate, JobOfferUpdate

class CRUDJobOffer(CRUDBase[JobOffer, JobOfferCreate, JobOfferUpdate]):
    def create(self, db: Session, obj_in: JobOfferCreate) -> JobOffer:
        obj_in_data = obj_in.dict()
        db_obj = JobOffer(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: JobOffer, obj_in: JobOfferUpdate
    ) -> JobOffer:
        obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

job_offer = CRUDJobOffer(JobOffer)
