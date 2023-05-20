# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.token import Token  # noqa
from app.models.job_offer import JobOffer  # noqa
