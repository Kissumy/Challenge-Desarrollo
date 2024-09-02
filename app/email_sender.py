import smtplib
from email.mime.text import MIMEText
from app.logger import log_info, log_error, log_critical
from config.config import SMTP_USERNAME, SMTP_PASSWORD, DEFAULT_EMAIL, SMTP_SERVER, SMTP_PORT, DEFAULT_CUSTOMER_EMAIL

def send_email(db_name: str, manager_id: str, owner_id: str, manager_db_id: int) -> None:

	manager_mail = manager_id

	if manager_id == "unknown":
		manager_mail = DEFAULT_CUSTOMER_EMAIL

	subject = f"Action Required: Classification Review for Database"
	body = f"""
Dear Manager ID: {manager_mail},


I hope you are ok.

As part of the anual information classification process, we request your review of the classification for the following database:

- Database Name: {db_name}
- Owner ID: {owner_id}
- Manager ID: {manager_id}
- Current Classification: High

Please confirm if the previous information reflects the sensitivity and importance of the data contained within this database. If any updates or changes are needed, please let us know to correct the information.

If you have any questions or need aditional information, please do not hesitate to contact our security team

regards
	"""

	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = DEFAULT_EMAIL
	msg['To'] = manager_mail

	try:
		server = smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT)
		server.starttls()
		server.login(SMTP_USERNAME, SMTP_PASSWORD)
		server.send_message(msg, msg['From'], msg['To'])
		server.quit()
		log_info(f"Email sent to manager saved as ID = {manager_db_id} for database database classified as High.")

	except smtplib.SMTPException as e:
		log_error(f"Error sending email manager saved as ID = {manager_db_id} for database database classified as High: {str(e)}")
		raise(f"Error sending email manager saved as ID = {manager_db_id} for database database classified as High: {str(e)}")
	except Exception as e:
		log_critical(f"Unexpected error sending email: {str(e)}")
		raise(f"Unexpected error sending email: {str(e)}")