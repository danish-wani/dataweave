from datetime import datetime, date
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
from django.urls import reverse
from .models import Product


class ProductTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(urlh='12345abcde', title='Test Product', source='Amazon', crawl_date=date.today(),
                               thumbnail='https://abc.com', url='http://abc.com', crawl_time=datetime.now(), mrp=200,
                               available_price=189, stock='In stock', discount=0.5)

    def test_product_listing_v1_api(self):
        self.client.get(reverse('v1_list_products'))

    def test_product_listing_v2_api(self):
        self.client.get(reverse('v2_list_products'))

    def test_product_update_api(self):

        product = Product.objects.all().last()

        response = self.client.put(
            reverse('update_product', kwargs={'pk': product.pk}),
            data={
                'category': 'Test Category',
                'discount': 1
            },
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get('category'), 'Test Category')

        # should not update discount field because it's set as read only in serializer
        self.assertNotEqual(response.data.get('discount'), '1')

    def test_v1_search_product_api(self):

        response = self.client.get(
            reverse('v1_list_products'),
            data={
                'search': 'Product',
            },
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

        for obj in response.data.get('results'):
            self.assertIn('Test Product', obj.get('title'))

    def test_v2_search_product_api(self):

        response = self.client.get(
            reverse('v2_list_products'),
            data={
                'search': 'Product',
            },
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

        for obj in response.data.get('results'):
            self.assertIn('Test Product', obj.get('title'))
