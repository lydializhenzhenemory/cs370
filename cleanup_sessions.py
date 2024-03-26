import json
import pymysql
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import time

with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

def cleanup_expired_sessions():
    now = datetime.utcnow()
    # delete when 3 hours inactivate
    inactive_threshold = now - timedelta(hours=3)
    
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # passed their expiration time or guest sessions that have been inactive for more than 3 hours
            cursor.execute("""
                DELETE FROM game_sessions 
                WHERE expiration_time < %s
                   OR (is_guest = 1 AND last_activity < %s)
            """, (now, inactive_threshold))
            connection.commit()
            print(f"Expired sessions cleaned up at: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    except pymysql.MySQLError as e:
        print("Error cleaning up sessions:", e)
    finally:
        connection.close()

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_expired_sessions, 'interval', hours=1)
scheduler.start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
