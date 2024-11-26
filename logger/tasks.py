from celery import shared_task
from .models import ProductViewLog
from product.models import Product
from category.models import Category
import csv
from datetime import timedelta
from django.utils.timezone import now

@shared_task
def SharedTask():
    
    print("this is the shared task!!")

@shared_task
def GetProductViewLogs():
    time_threshold = now() - timedelta(hours=24)
    logs = ProductViewLog.objects.filter(viewed_at__gte=time_threshold)

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
        

    filename = f"Most viewed products from {time_threshold.strftime('%Y-%m-%d')} to {now().strftime('%Y-%m-%d')} - {now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Category','Product', 'View Count'])

        for category, view in most_viewed.items():
            csvwriter.writerow([category, view['product'], view['views']])

    print(f"task finished successfully! {filename}")

