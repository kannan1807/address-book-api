"""Pydantic schemas — validation + API documentation."""
from pydantic import BaseModel, Field, field_validator


class AddressBase(BaseModel):
    name:      str   = Field(..., min_length=1, max_length=200)
    street:    str   = Field(..., min_length=1)
    city:      str   = Field(..., min_length=1)
    country:   str   = Field(..., min_length=1)
    latitude:  float = Field(..., ge=-90,  le=90)
    longitude: float = Field(..., ge=-180, le=180)


class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    # All fields optional for partial updates (PATCH)
    name:      str   | None = None
    street:    str   | None = None
    city:      str   | None = None
    country:   str   | None = None
    latitude:  float | None = Field(default=None, ge=-90,  le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class AddressResponse(AddressBase):
    id: int
    model_config = {"from_attributes": True}


class NearbyQuery(BaseModel):
    latitude:  float = Field(..., ge=-90,  le=90)
    longitude: float = Field(..., ge=-180, le=180)
    distance_km: float = Field(..., gt=0, description="Radius in kilometres")