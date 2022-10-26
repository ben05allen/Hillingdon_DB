from sqlmodel import create_engine


sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"
engine = create_engine(sqlite_url, echo=False)

