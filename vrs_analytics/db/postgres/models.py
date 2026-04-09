from sqlalchemy import (Column,String,Date,DateTime,Float,Integer,func)
from sqlalchemy.dialects.postgresql import JSONB
from vrs_analytics.core.base import Base

class VRSAnalytics(Base):
    __tablename__ = "vrs_analytics"

    transaction_id = Column(String, primary_key=True, index=True)
    transaction_date = Column(Date, nullable=False)
    transaction_ts_utc = Column(DateTime(timezone=True), nullable=False)
    currency = Column(String(10))
    revenue = Column(Float)
    sale_amount = Column(Float)
    partner_name = Column(String)
    commission = Column(Float)
    partner_response = Column(JSONB)  # full booking JSON
    check_in_date = Column(Date)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    property = Column(JSONB)  # single_property JSON payload

    property_id = Column(String)
    property_name = Column(String)
    feature_image = Column(String)
    property_type_category = Column(String)
    bedroom = Column(Integer)
    country = Column(String)
    country_code = Column(String)
    city = Column(String)
    display_location = Column(String)
    location_id = Column(String)
    location_slug = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    owner_id = Column(String)
