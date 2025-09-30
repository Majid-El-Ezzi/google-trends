from sqlalchemy.dialects.postgresql import insert
from db import SessionLocal
from models_db import Trend

        
def upsert_trends(records, batch_size=50):
    session = SessionLocal()
    try:
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            for record in batch:
                query = insert(Trend).values(
                    date=record.date,
                    keyword=record.keyword,
                    geo=record.geo,
                    interest=record.interest
                ).on_conflict_do_update( # CHeck for conflict based on unique constraint 
                    index_elements=['date', 'keyword', 'geo'], # columns that define uniqueness
                    set_=dict(interest=record.interest)# update interest if conflict occurs
                )
                session.execute(query) #execute the above statement.
            session.commit() #commit changes
            print(f"Upserted batch {i//batch_size + 1} ({len(batch)} records).")
    except Exception as e:
        session.rollback()
        print("Error during batch upsert:", e)
    finally:
        session.close()
