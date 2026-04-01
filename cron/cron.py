import schedule
import time
from db.db_connection import get_connection
from service.api_client import fetch_data
from service.upsert import sync_data

def job():
    print("Api Call")
    data = fetch_data()
    sync_data(data)

def run() :
    get_connection()  
    print("Scheduler Start")
    
    job() 
    schedule.every(1).minutes.do(job)  

    while True:
        schedule.run_pending()
        time.sleep(1)
