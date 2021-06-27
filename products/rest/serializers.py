from rest_framework import serializers
from products.models import Product


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['urlh', 'status', 'sku', 'title', 'thumbnail', 'url', 'source', 'seller', 'crawl_date',
                            'crawl_time', 'mrp', 'available_price', 'discount', 'stock']
