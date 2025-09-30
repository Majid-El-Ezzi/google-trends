from db import Base, engine
from models_db import Trend

# Create the table in the database
def init_db():
    print("Initializing database...")
    # Create all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

if __name__ == "__main__":
    init_db()