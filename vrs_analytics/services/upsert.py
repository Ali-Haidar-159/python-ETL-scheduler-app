from datetime import datetime
from vrs_analytics.db.postgres.db_operations import Session
from vrs_analytics.db.postgres.models import VRSAnalytics
from vrs_analytics.notifier.mailer import send_email

def sync_data(records):
    session = Session()
    inserted = 0
    updated = 0

    try:
        for rec in records:
            transaction_id = rec.get("transaction_id")
            
            # Check if transaction already exists
            existing = session.query(VRSAnalytics).filter_by(transaction_id=transaction_id).first()
            
            # Extract booking-level fields
            transaction_date = rec.get("transaction_date")
            transaction_ts_utc = rec.get("transaction_ts_utc")
            currency = rec.get("currency")
            revenue = rec.get("revenue")
            sale_amount = rec.get("sale_amount")
            partner_response = rec.get("partner_response")
            check_in_date = rec.get("check_in_date")
            
            # Extract property-level fields safely
            property_info_root = rec.get("property_info") or {}
            property_info = property_info_root.get("Data", {}).get(rec.get("property_id"), {})
            property_payload = property_info
            property_name = property_info.get("PropertyName")
            feature_image = property_info.get("FeatureImage")
            property_type_category = property_info.get("PropertyTypeCategory")
            bedroom = property_info.get("BedRoom")
            country = property_info.get("Country")
            country_code = property_info.get("CountryCode")
            city = property_info.get("City")
            display_location = property_info.get("Display")
            location_id = property_info.get("LocationId")
            location_slug = property_info.get("LocationSlug")
            latitude = property_info.get("Lat")
            longitude = property_info.get("Lon")
            owner_id = property_info.get("OwnerId")
            partner_name = partner_response.get("partnerName") if partner_response else None
            commission = partner_response.get("totalPrice", {}).get("commission") if partner_response else None
            property_id = property_info.get("ID")
            
            if existing:
                # Update existing record
                existing.transaction_date = transaction_date
                existing.transaction_ts_utc = transaction_ts_utc
                existing.currency = currency
                existing.revenue = revenue
                existing.sale_amount = sale_amount
                existing.partner_response = partner_response
                existing.check_in_date = check_in_date
                existing.property = property_payload
                existing.property_id = property_id
                existing.property_name = property_name
                existing.feature_image = feature_image
                existing.property_type_category = property_type_category
                existing.bedroom = bedroom
                existing.country = country
                existing.country_code = country_code
                existing.city = city
                existing.display_location = display_location
                existing.location_id = location_id
                existing.location_slug = location_slug
                existing.latitude = latitude
                existing.longitude = longitude
                existing.owner_id = owner_id
                existing.partner_name = partner_name
                existing.commission = commission
                existing.updated_at = datetime.now()
                updated += 1
            else:
                # Insert new record
                new_record = VRSAnalytics(
                    transaction_id=transaction_id,
                    transaction_date=transaction_date,
                    transaction_ts_utc=transaction_ts_utc,
                    currency=currency,
                    revenue=revenue,
                    sale_amount=sale_amount,
                    partner_response=partner_response,
                    check_in_date=check_in_date,
                    property=property_payload,
                    property_id=property_id,
                    property_name=property_name,
                    feature_image=feature_image,
                    property_type_category=property_type_category,
                    bedroom=bedroom,
                    country=country,
                    country_code=country_code,
                    city=city,
                    display_location=display_location,
                    location_id=location_id,
                    location_slug=location_slug,
                    latitude=latitude,
                    longitude=longitude,
                    owner_id=owner_id,
                    partner_name=partner_name,
                    commission=commission ,
                    created_at = datetime.now() ,
                    updated_at = datetime.now() 
                )
                session.add(new_record)
                inserted += 1
        
        session.commit()
        print(f"Sync done -> Inserted: {inserted}, Updated: {updated}")
        
        # email send to notify
        now = datetime.now()
        email_body = f"Sync done -> Inserted: {inserted}, Updated: {updated} -- time : {now}"
        send_email(email_body)
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
