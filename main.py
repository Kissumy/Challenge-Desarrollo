from app.data_loader import load_json, load_csv
from app.data_conviner import convine_data
from app.database_handler import save_to_database
from app.logger import setup_logs, log_info, log_critical
from config.config import JSON_PATH_FILE, CSV_PATH_FILE, LOG_PATH_FILE


def main():

  setup_logs(LOG_PATH_FILE)

  try:
    log_info("The process has started.")

    databases_data = load_json(JSON_PATH_FILE)
    user_data = load_csv(CSV_PATH_FILE)

    combined_data = convine_data(databases_data, user_data)

    save_to_database(combined_data)
    
    log_info("The process has ended without any issue.")

  except Exception as e:
        log_critical(f"error during program execution: {str(e)}")

if __name__ == "__main__":
  main()