from db.db_connection import Session
from db.models import Photos

def sync_data(records):
    session = Session()
    inserted = 0
    updated = 0

    try:
        for record in records:
            existing = session.query(Photos).filter_by(id=record["id"]).first()

            if existing:
                # Skip if data is same , and update if data is different
                if (existing.title != record["title"]):
                    
                    existing.title = record["title"]
                    updated += 1
            else:
                # insert new data
                new_post = Photos(
                    id=record["id"],
                    title=record["title"],
                    url=record["url"]
                )
                session.add(new_post)
                inserted += 1

        session.commit()
        print(f"Sync done -> Inserted: {inserted}, Updated: {updated}")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
