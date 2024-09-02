import logging

def setup_logs(LOG_PATH_FILE: str = 'messages.log') -> None:
	logging.basicConfig(
		filename = LOG_PATH_FILE,
		level = logging.INFO,  
		format = '%(asctime)s:%(levelname)s:%(message)s',
		filemode = 'a'
	)

def log_info(message: str) -> None:
	logging.info(message)

def log_warning(message: str) -> None:
	logging.warning(message)

def log_error(message: str) -> None:
	logging.error(message)

def log_critical(message: str) -> None:
	logging.critical(message)