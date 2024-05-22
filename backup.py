import json
import logging
import os
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

try:
    import schedule
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
    import schedule

try:
    from plyer import notification
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plyer"])
    from plyer import notification

# Global Constants
DATE_FORMAT = "%Y-%m-%d"
LOG_FILE = "backup.log"

# Load configuration
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

config = load_config()

# Logging configuration
log_dir = config.get("log_dir", ".logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging configuration
session_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = os.path.join(log_dir, f"backup_{session_time}.log")
logging.basicConfig(
    handlers=[RotatingFileHandler(
        log_file_path,
        maxBytes=config.get("log_max_bytes", 1024*1024),
        backupCount=config.get("log_backup_count", 5)
    )],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def backup_folder(folder_config):
    folder_path = folder_config["path"]
    exclude = folder_config.get("exclude", [])
    backup_root = folder_config.get("backup_path", False)
    
    folder_name = os.path.basename(folder_path)
    if backup_root:
        backup_dir = os.path.join(backup_root, f".backup_{folder_name}")
    else:
        backup_dir = os.path.join(os.path.dirname(folder_path), f".backup_{folder_name}")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_name = f"{folder_name}_backup_{datetime.now().strftime(DATE_FORMAT)}.zip"
    backup_path = os.path.join(backup_dir, backup_name)
    
    if os.path.exists(backup_path):
        logging.info(f"Backup {backup_path} already exists.")
        return

    with zipfile.ZipFile(backup_path, "w") as backup_zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file_path.startswith(ex) for ex in exclude):
                    continue
                arcname = os.path.relpath(file_path, folder_path)
                backup_zip.write(file_path, arcname)
    
    backup_size = sum(os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(backup_dir) for file in files)
    logging.info(f"Backup created: {backup_path}, Size: {backup_size / (1024*1024):.2f} MB")
    
    if config.get("enable_notifications", True):
        notification.notify(
            title="Backup Completed",
            message=f"Backup created: {backup_path}, Size: {backup_size / (1024*1024):.2f} MB",
            app_name="Backup Script",
            timeout=10
        )

def cleanup_old_backups(folder_config):
    folder_path = folder_config["path"]
    backup_root = folder_config.get("backup_path", False)
    
    if backup_root:
        backup_folder_path = os.path.join(backup_root, f".backup_{os.path.basename(folder_path)}")
    else:
        backup_folder_path = os.path.join(os.path.dirname(folder_path), f".backup_{os.path.basename(folder_path)}")
    backup_files = [f for f in os.listdir(backup_folder_path) if f.endswith(".zip")]
    
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    monthly_backups = set()
    yearly_backups = set()
    
    for backup in backup_files:
        try:
            date_str = backup.split("_")[-1].replace(".zip", "")
            backup_date = datetime.strptime(date_str, DATE_FORMAT)
            
            if backup_date >= week_ago:
                continue
            
            if backup_date.day == 1:
                if backup_date.month == 1:
                    yearly_backups.add(backup)
                else:
                    monthly_backups.add(backup)
            else:
                os.remove(os.path.join(backup_folder_path, backup))
                logging.info(f"Deleted old backup: {backup}")
        
        except (ValueError, IndexError):
            continue
    
    for backup in backup_files:
        try:
            date_str = backup.split("_")[-1].replace(".zip", "")
            backup_date = datetime.strptime(date_str, DATE_FORMAT)
            
            if backup_date < week_ago:
                if backup in monthly_backups or backup in yearly_backups:
                    continue
                os.remove(os.path.join(backup_folder_path, backup))
                logging.info(f"Deleted old backup: {backup}")
        
        except (ValueError, IndexError):
            continue

def enforce_backup_size_limit(backup_root):
    total_size = 0
    backup_files = []
    
    for root, dirs, files in os.walk(backup_root):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            backup_files.append((file_path, file_size))
    
    max_size = config.get("max_backup_size_mb", 100) * 1024 * 1024
    if total_size > max_size:
        backup_files.sort(key=lambda x: os.path.getmtime(x[0]))
        while total_size > max_size and backup_files:
            oldest_file = backup_files.pop(0)
            os.remove(oldest_file[0])
            total_size -= oldest_file[1]
            logging.info(f"Deleted backup due to size limit: {oldest_file[0]}")

def job():
    folders_to_backup = config["folders_to_backup"]
    for folder_config in folders_to_backup:
        backup_folder(folder_config)
        cleanup_old_backups(folder_config)
        if folder_config.get("backup_path"):
            enforce_backup_size_limit(folder_config["backup_path"])

schedule.every().day.at(config["backup_time"]).do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    job()  # Ensure backup is created if the script was not run at the scheduled time
    run_schedule()
