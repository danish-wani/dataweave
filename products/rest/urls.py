from django.urls import path
from .apis import (ListProductsAPI, UpdateProductAPI, DiscountProductBucketsAPI, ListProductsRawQueryAPI)


urlpatterns = [
    path('v1/products/', ListProductsAPI.as_view(), name='v1_list_products'),
    path('v2/products/', ListProductsRawQueryAPI.as_view(), name='v2_list_products'),
    path('v1/products/discount-buckets/', DiscountProductBucketsAPI.as_view(), name='discount_product_buckets'),
    path('v1/products/<int:pk>/', UpdateProductAPI.as_view(), name='update_product'),
]
