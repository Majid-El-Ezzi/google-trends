from pytrends.request import TrendReq
from pandas import DataFrame
import matplotlib.pyplot as plt
from models import Record


# Initialization
pytrends = TrendReq(hl="en-US", tz=0)

# Build a request for keyword "Ballon d'Or" (last 7 days)
pytrends.build_payload(["Ballon d'Or"], timeframe="today 1-m", geo="") # Worldwide

# Fetch interest over time
df: DataFrame = pytrends.interest_over_time()
day_data = df.loc["2025-09-22"]


print("Total rows:", len(df))
print("Row for 22 Sep 2025:")
print(day_data)

# Converting DataFrame --> Pydantic Records
def convert_to_records(df, keyword: str, geo:str): # Convert DataFrame to list of records based on models.py
    records = []
    for index, row in df.iterrows():
        try:
            rec = Record(
                date=index.to_pydatetime(), # Convert Timestamp to datetime
                keyword=keyword,
                geo=geo,
                interest=int(row[keyword])
            )
            records.append(rec)
        except Exception as e:
            print("Error converting to records:", e)
    return records

records = convert_to_records(df, "Ballon d'Or", "")
print('------------------------------')
print(f"Converted {len(records)} records out of {len(df)} rows.")
print('------------------------------')
print(records[:3]) # Print first 3 recordss
