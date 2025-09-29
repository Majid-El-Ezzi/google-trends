from db import Base, engine
from models_db import Trend

# Create the table in the database
Base.metadata.create_all(bind=engine)
print("Database initialized and table created.")