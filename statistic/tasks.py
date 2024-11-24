from celery import shared_task

@shared_task
def SharedTask():
    
    print("this is the shared task!!")