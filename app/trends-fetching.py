from pytrends.request import TrendReq
from pandas import DataFrame
import matplotlib.pyplot as plt

# Initialization
pytrends = TrendReq(hl="en-US", tz=0)

# Build a request for keyword "Ballon d'Or" (last 7 days)
pytrends.build_payload(["Ballon d'Or"], timeframe="now 7-d", geo="") # Worldwide

# Fetch interest over time
df: DataFrame = pytrends.interest_over_time()
day_data = df.loc["2025-09-22"]


print("Total rows:", len(df))
print("Rows for 22 Sep 2025:")
print(day_data)


# Plot the hourly interest values for 22 Sep 2025
day_data["Ballon d'Or"].plot(
    kind="line",
    figsize=(12,5),
    title="Ballon d'Or Search Interest on 22 Sep 2025 (Hourly)"
)

plt.xlabel("Hour of the Day")
plt.ylabel("Search Interest (0–100)")
plt.grid(True)
plt.show()