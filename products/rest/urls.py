from django.urls import path
from .apis import ListProductsAPI


urlpatterns = [
    path('v1/products/', ListProductsAPI.as_view(), name='list_products')
]
