from django.urls import path
from .apis import (ListProductsAPI, UpdateProductAPI)


urlpatterns = [
    path('v1/products/', ListProductsAPI.as_view(), name='list_products'),
    path('v1/products/<int:pk>/', UpdateProductAPI.as_view(), name='update_product'),
]
