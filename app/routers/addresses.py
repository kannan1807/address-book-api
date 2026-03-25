"""Address CRUD + proximity search endpoints."""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=schemas.AddressResponse, status_code=201)
def create(payload: schemas.AddressCreate, db: Session = Depends(get_db)):
    """Create a new address."""
    logger.info("POST /addresses — creating address for '%s'", payload.name)
    try:
        address = crud.create_address(db, payload)
        logger.info("POST /addresses — success, id=%s", address.id)
        return address
    except Exception as e:
        logger.error("POST /addresses — failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to create address")


@router.get("/", response_model=list[schemas.AddressResponse])
def list_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all addresses with pagination."""
    logger.info("GET /addresses — skip=%s limit=%s", skip, limit)
    try:
        addresses = crud.get_all_addresses(db, skip, limit)
        logger.info("GET /addresses — returned %s records", len(addresses))
        return addresses
    except Exception as e:
        logger.error("GET /addresses — failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch addresses")


@router.get("/nearby/search", response_model=list[schemas.AddressResponse])
def nearby(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: Session = Depends(get_db)
):
    """Find all addresses within a given distance (km) from coordinates."""
    logger.info(
        "GET /addresses/nearby/search — lat=%s lon=%s km=%s",
        latitude, longitude, distance_km
    )
    try:
        results = crud.get_nearby_addresses(db, latitude, longitude, distance_km)
        logger.info(
            "GET /addresses/nearby/search — found %s addresses within %skm",
            len(results), distance_km
        )
        return results
    except Exception as e:
        logger.error("GET /addresses/nearby/search — failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Failed to search nearby addresses")


@router.get("/{address_id}", response_model=schemas.AddressResponse)
def read_one(address_id: int, db: Session = Depends(get_db)):
    """Get a single address by ID."""
    logger.info("GET /addresses/%s — fetching", address_id)
    try:
        addr = crud.get_address(db, address_id)
        if not addr:
            logger.warning("GET /addresses/%s — not found", address_id)
            raise HTTPException(status_code=404, detail="Address not found")
        logger.info("GET /addresses/%s — success", address_id)
        return addr
    except HTTPException:
        raise
    except Exception as e:
        logger.error("GET /addresses/%s — failed: %s", address_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch address")


@router.patch("/{address_id}", response_model=schemas.AddressResponse)
def update(
    address_id: int,
    payload: schemas.AddressUpdate,
    db: Session = Depends(get_db)
):
    """Partially update an address."""
    logger.info("PATCH /addresses/%s — updating", address_id)
    try:
        addr = crud.update_address(db, address_id, payload)
        if not addr:
            logger.warning("PATCH /addresses/%s — not found", address_id)
            raise HTTPException(status_code=404, detail="Address not found")
        logger.info("PATCH /addresses/%s — success", address_id)
        return addr
    except HTTPException:
        raise
    except Exception as e:
        logger.error("PATCH /addresses/%s — failed: %s", address_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to update address")


@router.delete("/{address_id}", status_code=204)
def delete(address_id: int, db: Session = Depends(get_db)):
    """Delete an address by ID."""
    logger.info("DELETE /addresses/%s — deleting", address_id)
    try:
        if not crud.delete_address(db, address_id):
            logger.warning("DELETE /addresses/%s — not found", address_id)
            raise HTTPException(status_code=404, detail="Address not found")
        logger.info("DELETE /addresses/%s — success", address_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("DELETE /addresses/%s — failed: %s", address_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to delete address")