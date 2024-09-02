import psycopg
from app.email_sender import send_email
from app.logger import log_info, log_error, log_critical
from config.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def connect_to_db():
  """
  Returns:
      psycopg.connection:
  """
  
  try:
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    log_info("Connected to PostgreSQL database successfully.")
    return conn
  except Exception as e:
    log_critical(f"Failed to connect to PostgreSQL database: {str(e)}")
    raise(f"Failed to connect to PostgreSQL database: {e}")


def create_db_tables(conn, cursor) -> None:
  """
  Args:
      conn: psycopg.connection:
      cursor: psycopg.cursor
  """

  try:
      
    # Create normalized tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Managers
                  (id SERIAL PRIMARY KEY, email TEXT UNIQUE)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Owners
                  (id SERIAL PRIMARY KEY, email TEXT UNIQUE, manager_id INTEGER,
                  FOREIGN KEY(manager_id) REFERENCES Managers(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Databases
                  (id SERIAL PRIMARY KEY, database_name TEXT, classification TEXT, owner_id INTEGER,
                  FOREIGN KEY(owner_id) REFERENCES Owners(id))''')
    
    conn.commit()
    log_info("PostgreSQL database initialized successfully.")

  except Exception as e:
    log_critical(f"Error initializing PostgreSQL database: {str(e)}")
    print(f"Error initializing PostgreSQL database: {str(e)}")

def get_manager_id(cursor, manager_email: str) -> int:
  """
  Args:
      cursor: psycopg.cursor
      manager_email: str
  """
  try:
    manager_email = manager_email.strip().lower()
    cursor.execute('''INSERT INTO Managers(email) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;''', 
                  (manager_email,))
    result = cursor.fetchone()
    if result is None:
      cursor.execute('''SELECT id FROM Managers WHERE email = %s''',
                    (manager_email,))
      manager_id = cursor.fetchone()[0]
    else:
      manager_id = result[0]
    return manager_id
  
  except Exception as e:
    log_error(f"Error processing manager {manager_email}: {str(e)}")
    raise(f"Error processing manager {manager_email}: {str(e)}")
    
def get_owner_id(cursor, manager_id: int, owner_email: str) -> int:
    """
    Args:
        cursor: psycopg.cursor 
        manager_id: int
        owner_email: str
    """
    try:
        owner_email = owner_email.strip().lower()
        cursor.execute('''INSERT INTO Owners (email, manager_id) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING RETURNING id''',
                      (owner_email, manager_id))
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute('''SELECT id FROM owners WHERE email = %s''', 
                          (owner_email,))
            owner_id = cursor.fetchone()[0]
        else:
            owner_id = result[0]
        return owner_id
    
    except Exception as e:
        log_error(f"Error processing owner {owner_email}: {str(e)}")
        raise(f"Error processing owner {owner_email}: {str(e)}")
    
def insert_to_database(entry: dict[str: str], cursor):
  """
  Args:
      entry: dict[str: str]
      cursor: psycopg.cursor
  """

  db_name = entry["db_name"]
  classification = entry["classification"]
  manager_id = get_manager_id(cursor, entry["manager_email"])
  owner_id = get_owner_id(cursor, manager_id, entry["owner_email"])
  cursor.execute("INSERT INTO Databases (database_name, classification, owner_id) VALUES (%s, %s, %s)",
                (db_name, classification, owner_id))
  
  if classification == "high":
    send_email(db_name, entry["manager_email"], entry["owner_email"],manager_id)

def save_to_database(combined_data: list[dict[str: str]]) -> None:
  try:
    conn = connect_to_db()
    if conn is None:
      return

    cursor = conn.cursor()

    create_db_tables(conn, cursor)
    for entry in combined_data:
      insert_to_database(entry, cursor)
        
    conn.commit()
    cursor.close()
    conn.close()
    log_info("Data saved to PostgreSQL database successfully.")

  except Exception as e:
    log_critical(f"Error saving data to PostgreSQL database: {str(e)}")
    raise(f"Error saving data to PostgreSQL database: {str(e)}")

