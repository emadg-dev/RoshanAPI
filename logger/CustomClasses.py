from product.models import Product, ProductViewLog
from django.utils.timezone import now

def Log_Product_View(user, product):
    ProductViewLog.objects.create(user=user, product=product)