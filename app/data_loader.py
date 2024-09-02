import json
import pandas as pd
import re
from app.logger import log_info, log_warning, log_error, log_critical


def validate_email(email: str) -> bool: 
  email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 
  return re.match(email_regex, email) is not None


def sanitized_data(json_data: list) -> list[dict[str: str]]:
  sanitized_data = []
  index = 0

  for json_item in json_data:
    index +=1
    db_name = json_item.get('db_name')
    if not db_name:
      db_name = 'Unknown Database'
      log_warning(f"Missing Database name for registry {index}. designated name: 'Unknown Database'.")
    
    owner_email = json_item.get('owner_email')
    if not owner_email or not validate_email(owner_email):
      owner_email = 'Unknown Email'
      log_warning(f"Missing or invalid owner mail for registry {index}. designated Email: 'Unknown Email'.")

    classification = json_item.get('classification')
    classification_level = ['high', 'medium', 'low']
    if not classification or classification not in classification_level: 
      classification = 'missing'
      log_warning(f"Missing or invalid classification for registry {index}. designated classification: 'missing'.")

    sanitized_data.append({
      'db_name': db_name,
      'owner_email': owner_email,
      'classification': classification
    })

  return sanitized_data


def load_json(json_path_file: str) -> list[dict[str: str]]:
  log_info(f"Extracting data from {json_path_file}.")
  try:
    with open(json_path_file) as json_file: 
      json_data = json.load(json_file)

      return sanitized_data(json_data)
    
  except FileNotFoundError:
    log_error(f"The file {json_path_file} was not found.")
    raise(f"The file {json_path_file} was not found.")
  except json.JSONDecodeError:
    log_error(f"The file {json_path_file} is not a valid JSON.")
    raise(f"The file {json_path_file} is not a valid JSON.")
  except Exception as e:
    log_critical(f"Unexpected error loading JSON file {json_path_file}: {str(e)}")
    raise(f"Unexpected error loading JSON file {json_path_file}: {str(e)}")
  

def validate_csv_colums(csv_data) -> None:
  """
  Args:
    csv_data: DataFrame
  """
  required_columns = ['row_id', 'user_id', 'user_state', 'user_manager']

  for column in required_columns:
    if column not in csv_data.columns:
      log_error(f"Required column '{column}' is missing in the CSV file.")
      raise(f"Required column '{column}' is missing in the CSV file.")
    
def validate_row_data(row) -> None:
  """
  validate that user_id and user_manager have a correct email format, if not it rise an excemption 

  Args:
      row: Series
  """
  if not validate_email(row['user_id']):
    log_error(f"Invalid user email in the row: {row['row__id']}")
    raise(f"Invalid user email in the row: {row['row__id']}")
  
  if not validate_email(row['user_manager']):
    log_error(f"Invalid manager email in the row: {row['row__id']}")
    raise(f"Invalid manager email in the row: {row['row__id']}")
    
def extract_csv_data(csv_data) -> list:
  """
  Args:
    csv_data: DataFrame
  """
  validated_data = []
  for index, row in csv_data.iterrows():
    validate_row_data(row)

    validated_data.append(row)
  return validated_data

def load_csv(csv_path_file: str):
  """
  Returns:
    DataFrame
  """
  log_info(f"Extracting data from {csv_path_file}.")
  try:
    csv_data = pd.read_csv(csv_path_file)

    validate_csv_colums(csv_data)

    return pd.DataFrame(extract_csv_data(csv_data))
  
  except FileNotFoundError:
    log_error(f"The file {csv_path_file} was not found.")
    raise(f"The file {csv_path_file} was not found.")
  except pd.errors.EmptyDataError:
    log_error(f"The CSV file {csv_path_file} is empty.")
    raise(f"The CSV file {csv_path_file} is empty.")
  except pd.errors.ParserError:
    log_error(f"Could not parse the CSV file {csv_path_file}.")
    raise(f"Could not parse the CSV file {csv_path_file}.")
  except Exception as e:
    log_critical(f"Unexpected error loading the CSV file {csv_path_file}: {str(e)}")
    raise(f"Unexpected error loading the CSV file {csv_path_file}: {str(e)}")



