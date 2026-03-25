"""CRUD operations — all DB interactions are isolated here."""
import logging
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import get_distance_km

logger = logging.getLogger(__name__)


def create_address(db: Session, data: schemas.AddressCreate) -> models.Address:
    address = models.Address(**data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    logger.info("Created address id=%s", address.id)
    return address

def get_address(db: Session, address_id: int) -> models.Address | None:
    return db.query(models.Address).filter(
        models.Address.id == address_id
    ).first()


def get_all_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


def update_address(
    db: Session, address_id: int, data: schemas.AddressUpdate
) -> models.Address | None:
    address = get_address(db, address_id)
    if not address:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    logger.info("Updated address id=%s", address_id)
    return address

def delete_address(db: Session, address_id: int) -> bool:
    address = get_address(db, address_id)
    if not address:
        return False
    db.delete(address)
    db.commit()
    logger.info("Deleted address id=%s", address_id)
    return True


def get_nearby_addresses(
    db: Session, lat: float, lon: float, distance_km: float
) -> list[models.Address]:
    # Fetch all, then filter by Haversine distance in Python
    all_addresses = db.query(models.Address).all()
    return [
        addr for addr in all_addresses
        if get_distance_km(lat, lon, addr.latitude, addr.longitude) <= distance_km
    ]