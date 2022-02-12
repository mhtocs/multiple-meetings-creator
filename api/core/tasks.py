from api import celery
import time


@celery.task()
def process_file(filename: str):
    wait_time = 15
    print(f"process_file will take {wait_time} seconds")
    time.sleep(wait_time)
    print("process_file completed")
