from app.logger import log_info

def convine_data(json_data: list[dict[str: str]], csv_data) -> list[dict[str: str]]:
	"""
	Args:
		json_data: list[dict[str: str]]
		csv_data: DataFrame
	"""
	log_info("Starting data processing.")

	combined_data = []
	for entry in json_data:
		db_name = entry.get("db_name")
		owner_email = entry.get("owner_email")
		classification = entry.get("classification")
		manager_email = csv_data.loc[csv_data['user_id'] == owner_email, "user_manager"].values
		manager_email = manager_email[0] if len(manager_email) > 0 else "unknown" 
		
		combined_data.append({
			"db_name": db_name,
			"owner_email": owner_email,
			"manager_email": manager_email,
			"classification": classification
		})
	
	log_info("Data processed successfully.")
	return combined_data