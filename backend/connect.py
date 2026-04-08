from sqlmodel import create_engine, Session
from settings import DBSettings


# load_dotenv()   # loads contents of the .env file into the script's environment

"""
Checks if the DB URL is valid and creates a session engine for database connection.
"""
def connect_engine():
    database_url = DBSettings().database_url
    print(f"Database URL from connect.py: {database_url}")

    # database_url = os.getenv("DATABASE_URL")

    # error handling - no .env file found
    if not database_url:
        print("database_url not found in .env file.")

    # error handing - when creating an engine object
    """"
    Future notes: Struggled to maintain connection with database due to the following reasons:
        1. Using 'with' block to establish connection with database, but after the exiting the block, the connection is closed.
        2.  
    """
    db = create_engine(database_url, echo=False)
    try:
        print("Connection with DB was successful!.")
        conn = db.connect()
        return conn
    except Exception as e:
        return f"Connection failed: {e}"

engine = connect_engine()

# Creates a session when an API call is made
def get_db():
    with Session(engine) as session:
        print(session.get_bind())
        yield session
