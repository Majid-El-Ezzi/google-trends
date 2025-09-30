from db import SessionLocal
from models_db import Trend
from pandas import DataFrame
from pytrends.request import TrendReq
from models import Record
from upsert_db import upsert_trends
import time

def is_db_empty():
    session = SessionLocal()
    try:
        return session.query(Trend).count() == 0 # Check if table is empty
    except Exception as e:
        print("Error checking if DB is empty:", e)
        return True
    finally:
        session.close()
        
def fetch_all_trends(keyword: str, timeframe: str, geo: str="") -> DataFrame: # Fetch trends with retries
    pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25)) # Increased timeout to handle slow responses
    for attempt in range(3):
        try:
            pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
            df: DataFrame = pytrends.interest_over_time()
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            return df
        except Exception as e:
            print(f"Error fetching (attempt {attempt+1}): {e}")
            time.sleep(30 * (attempt + 1))  # exponential wait due to rate limiting and error 429 (too many requests)
    raise RuntimeError("Failed to fetch after retries.")


def df_to_records(df: DataFrame, keyword: str, geo: str): # Convert dataframe to pydantic records for upsert
    records = []
    for index, row in df.iterrows():
        try:
            rec = Record(
                date=index.to_pydatetime(),
                keyword=keyword,
                geo=geo,
                interest=int(row[keyword])
            )
            records.append(rec)
        except Exception as e:
            print("Error converting to records:", e)
    return records

def run_pipe(keyword:str, geo: str=""):
    timeframe = "today 3-m" if is_db_empty() else "now 7-d" # Fetch last 3 months if DB empty, else last 7 days
    print(f"Fetching data for '{keyword}' from Google Trends for timeframe '{timeframe}'...")
    
    df = fetch_all_trends(keyword, timeframe, geo) # fetch data
    print(f"Fetched {len(df)} rows from Google Trends.")
    
    records = df_to_records(df, keyword, geo) # convert to records suitable for upsert
    print(f"Converted to {len(records)} records.")
    
    if records:
        upsert_trends(records) # upsert into DB
    else:
        print("No records to upsert.")

if __name__ == "__main__": 
    run_pipe("Ballon d'Or", "")