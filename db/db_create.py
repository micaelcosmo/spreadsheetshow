from sqlalchemy import create_engine

username = 'root'
password = 'root'
host = 'localhost'
port = 3306
DB_NAME = 'spreadsheetshow'

engine = create_engine(f"mysql://{username}:{password}@{host}:{port}")

with engine.connect() as conn:
    # Do not substitute user-supplied database names here.
    conn.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
