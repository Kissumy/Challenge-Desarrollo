from dotenv import load_dotenv
import os

# Cargar las variables desde el archivo .env
load_dotenv(encoding="utf-8")

# Asignar las variables de entorno a las variables dentro del codigo
JSON_PATH_FILE = os.getenv('JSON_PATH_FILE')
CSV_PATH_FILE = os.getenv('CSV_PATH_FILE')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

LOG_PATH_FILE = os.getenv('LOG_PATH_FILE')

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
DEFAULT_EMAIL = os.getenv('DEFAULT_EMAIL')

DEFAULT_CUSTOMER_EMAIL = os.getenv('DEFAULT_CUSTOMER_EMAIL')