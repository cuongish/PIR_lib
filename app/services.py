import sqlalchemy.orm
from typing import TYPE_CHECKING

import app.database as _database
import app.models as _models
import app.schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_contact(contact: _schemas.CreateContact,
                         db: sqlalchemy.orm.Session) -> _schemas.Contact:
    contact = _models.Contact(**contact.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return _schemas.Contact.from_orm(contact)


async def get_contact(contact_id: int, db: sqlalchemy.orm.Session):
    contact = db.query(_models.Contact).filter(_models.Contact.id == contact_id).first()
    return contact


async def delete_contact(contact: _models.Contact, db: sqlalchemy.orm.Session):
    db.delete(contact)
    db.commit()


async def update_contact(contact_data: _schemas.CreateContact,
                         contact: _models.Contact, db: sqlalchemy.orm.Session) -> _schemas.Contact:
    contact.first_name = contact_data.first_name
    contact.last_name = contact_data.last_name
    contact.email = contact_data.email
    contact.gender = contact_data.gender
    contact.ip_address = contact_data.ip_address
    contact.country_code = contact.country_code

    db.commit()
    db.refresh(contact)

    return _schemas.Contact.from_orm(contact)
