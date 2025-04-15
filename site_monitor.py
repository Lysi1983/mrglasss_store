import requests
import smtplib
import os
import time
import signal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables
load_dotenv()

# Email configuration
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS').lower() == 'true'

# Site to monitor - replace with your actual website URL
SITE_URL = "https://mrglass24.com/"  # Change this to your website URL

def check_site_status():
    """Check if the site is up and running"""
    try:
        response = requests.get(SITE_URL)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error checking site status: {e}")
        return None

def send_email(subject, body):
    """Send an email notification"""
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = MAIL_USERNAME
        message['To'] = MAIL_USERNAME  # Sending to self, can be changed
        message['Subject'] = subject
        
        # Attach body
        message.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            if MAIL_USE_TLS:
                server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(message)
        
        print(f"Email sent successfully at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_site_task():
    """Task to check site status and send email if status is 200"""
    print(f"Checking site status at {time.strftime('%Y-%m-%d %H:%M:%S')}...")
    status_code = check_site_status()
    
    if status_code == 200:
        subject = "Site Status Alert: Site is UP"
        body = f"The site {SITE_URL} is up and running with status code 200."
        send_email(subject, body)
    else:
        print(f"Site status: {status_code}")

def main():
    print("Starting site monitoring service with APScheduler...")
    scheduler = BackgroundScheduler()
    
    # Schedule the job to run every hour from 6:00 to 23:00
    scheduler.add_job(
        check_site_task,
        'cron',
        hour='6-23',  # Run every hour from 6 AM to 11 PM
        minute=0,     # Run at the start of each hour
        id='site_monitor_job',
        name='Check website status hourly'
    )
    
    # Define signal handler for graceful shutdown
    def signal_handler(sig, frame):
        print('Shutting down scheduler...')
        scheduler.shutdown()
        print("Scheduler stopped.")
        exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Run an immediate check when starting
        check_site_task()
        
        # Start the scheduler
        scheduler.start()
        print(f"Scheduler started. Monitoring {SITE_URL} hourly from 6 AM to 11 PM.")
        print("To keep running after terminal exit, use: python -m site_monitor.py &")
        print("Or use: nohup python site_monitor.py > monitor.log 2>&1 &")
        
        # Keep the main thread alive
        while True:
            time.sleep(60)  # Check every minute to reduce CPU usage
            
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
