from django.db.models import Q
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductsSerializer
from products.models import Product
from .paginations import StandardResultsSetPagination


class ListProductsAPI(ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'brand', 'source', 'subcategory']

    ORM = True

    def get_queryset(self):
        """

        """
        search = self.request.query_params.get('search')

        if self.ORM:

            return self.get_queryset_from_orm(search)

        return self.get_queryset_from_raw(search)

    @staticmethod
    def get_queryset_from_orm(search):
        """

        """

        if search:
            return Product.objects.filter(Q(title__icontains=search) | Q(sku__icontains=search))

        return Product.objects.all()

    @staticmethod
    def get_queryset_from_raw(search):
        """

        """
        sql_query = """
            SELECT * FROM products;
        """

        if search:
            search_text = '%' + search + '%'

            sql_query = """
                SELECT * FROM products WHERE title like %s or sku like %s;
            """

            return Product.objects.raw(sql_query, [search_text, search_text])

        return Product.objects.raw(sql_query, [])
