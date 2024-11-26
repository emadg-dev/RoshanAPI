from celery import shared_task
from .models import ProductViewLog
from product.models import Product
from category.models import Category
import csv
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count, Max

@shared_task
def SharedTask():
    
    print("this is the shared task!!")

@shared_task
def GetProductViewLogs():
    time_threshold = now() - timedelta(hours=24)
    logs = ProductViewLog.objects.filter(viewed_at__gte=time_threshold)
    # sorted_logs = (
    #     logs.values('category__id', 'category__name')
    #     .annotate(
    #         most_viewed_product=Max('product__id'),
    #         max_views=Count('product__id')
    #     )
    #     .order_by('category__name')
    # )

    views_list = {}
    categories = Category.objects.all()
    for category in categories:
        views_list[category] = {}

    for log in logs:
        category = log.product.category
        product = log.product

        if product not in views_list[category]:
            views_list[category][product] = 0
        views_list[category][product] += 1
    
    most_viewed = {}
    for category, products in views_list.items():
        
        mv_product = max(products, key=products.get)
        most_viewed[category] = {
            'product': mv_product,
            'views': products[mv_product]
        }
        

    filename = f"Most viewed products from {time_threshold.strftime('%Y-%m-%d_%H-%M-%S')} to {now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Category','Product', 'View Count'])

        for category, view in most_viewed.items():
            csvwriter.writerow([category, view['product'], view['views']])


        # for index in sorted_logs:
        #     category = index['category__name']
        #     product_id = index['most_viewed_product']
        #     views = index['max_views']

        #     product = Product.objects.get(pk=product_id)
        #     csvwriter.writerow([category, product, views])

    print(f"task finished successfully! {filename}")



# from celery import shared_task
# import time
# import logging

# logger = logging.getLogger(__name__)

# @shared_task(name='count_to_10')     
# def count_task():  
#     logger.info("Task started: Count to 10")      
#     for i in range(1, 11):
#         logger.info(i)
#         time.sleep(1)
#     logger.info("Task completed!")
#     return 'Task Done!'


# @shared_task(name='send_newsletter')  
# def send_newsletter():
#     logger.info("Task started: Sending Newsletters")      
#     for i in range(1, 11):
#         logger.info(f'{i}. Newsletter')
#         time.sleep(1)
#     logger.info("All Newsletter sent!")       
#     return 'Completed!'