from pathlib import Path
import os
from dotenv import load_dotenv
from mongoengine import connect

# Optional mongomock fallback for tests/local dev when no real Mongo is available
try:
    import mongomock  # type: ignore
except Exception:
    mongomock = None

# Loading environment variables from the project .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Getting the MongoDB connection string from .env
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if not CONNECTION_STRING:
    # No external Mongo URI provided — tests or local dev can use mongomock
    if not mongomock:
        raise Exception("The Connection String is not set in the .env file and mongomock is not installed. Set CONNECTION_STRING or install mongomock.")

def init_db():
    # Connect auth DB (alias: auth_db)
    if CONNECTION_STRING:
        connect(db="project_manager_auth", alias="auth_db", host=CONNECTION_STRING)
        connect(db="project_manager", alias="project_db", host=CONNECTION_STRING)
    else:
        # Use mongomock for in-memory testing/dev
        connect(db="project_manager_auth", alias="auth_db", host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
        connect(db="project_manager", alias="project_db", host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
# `os` is Python's standard library module for interacting with the operating system (env vars, paths, etc.).
