from sqlalchemy.dialects.postgresql import insert
from db import SessionLocal
from models_db import Trend

def upsert_trends(records):
    session = SessionLocal()
    try:
        for record in records: # this function is upserting row by row. Not efficient for large datasets.
            query = insert(Trend).values(
                date=record.date,
                keyword=record.keyword,
                geo=record.geo,
                interest=record.interest
            ).on_conflict_do_update( # CHeck for conflict based on unique constraint
                index_elements=['date', 'keyword', 'geo'], 
                set_=dict(interest=record.interest) # update interest if conflict occurs
            )
            session.execute(query) #execute the above statement.
        session.commit() #commit changes
        print(f"Upserted {len(records)} records successfully.")
    except Exception as e:
        session.rollback()
        print("Error during upsert:", e)
    finally:
        session.close()