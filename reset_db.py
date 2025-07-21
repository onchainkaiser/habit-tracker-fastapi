# reset_db.py

from database import Base, engine  # Adjust imports based on your project structure
import models  # Ensure this imports all models so SQLAlchemy sees them

def reset_database():
    print("🔁 Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped.")
    
    print("🔧 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created.")

if __name__ == "__main__":
    reset_database()
