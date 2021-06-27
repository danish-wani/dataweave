from django.db import models


class Product(models.Model):
    """

    """
    urlh = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    subcategory = models.CharField(max_length=100, null=True, blank=True)
    product_type = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    title = models.TextField()
    thumbnail = models.URLField(max_length=500)
    url = models.URLField(max_length=500)
    source = models.CharField(max_length=100)
    seller = models.CharField(max_length=200, null=True, blank=True)
    crawl_date = models.DateField()
    crawl_time = models.DateTimeField()
    mrp = models.FloatField()
    available_price = models.FloatField()
    discount = models.FloatField()
    stock = models.CharField(max_length=20)

    class Meta:
        db_table = 'products'

    def __str__(self):
        """

        """
        return str(self.title) + ' | ' + str(self.mrp)
