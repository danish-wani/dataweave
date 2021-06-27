from django.http import Http404
from django.db.models import Q, Count
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductsSerializer
from products.models import Product
from .paginations import CustomPagination


class ListProductsAPI(ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'brand', 'source', 'subcategory']

    USE_ORM = False

    def get_queryset(self):
        """

        """
        search_text = self.request.query_params.get('search')

        if self.USE_ORM:

            return self.get_queryset_from_orm(search_text)

        return self.get_queryset_from_raw(search_text)

    @staticmethod
    def get_queryset_from_orm(search):
        """

        """

        if search:
            condition = Q(Q(title__icontains=search) | Q(sku__icontains=search))
            return Product.objects.filter(condition)

        return Product.objects.all()

    @staticmethod
    def get_queryset_from_raw(search_text):
        """

        """
        sql_query = """
            SELECT * FROM products;
        """

        if search_text:
            search_text = '%' + search_text + '%'

            sql_query = """
                SELECT * FROM products WHERE title like %s or sku like %s
            """
            params = [search_text, search_text]

            queryset = Product.objects.raw(sql_query, params)

            return queryset

        return Product.objects.raw(sql_query)


class ListProductsRawQueryAPI(ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = CustomPagination
    filter_by_fields = ['category', 'brand', 'source', 'subcategory']

    def get_queryset(self):
        """

        """
        query_params = self.request.query_params

        if any([query_params.get(field) for field in self.filter_by_fields]):
            return self.get_filtered_queryset(query_params)

        return self.get_queryset_from_raw(query_params)

    def get_filtered_queryset(self, query_params):
        """

        """
        params = list()
        search_text = query_params.get('search')
        field_value_pairs = dict()

        for field in self.filter_by_fields:
            if query_params.get(field):
                field_value_pairs[field] = query_params.get(field)

        sql_query = """
            SELECT * FROM products WHERE
        """
        filter_query = str()

        if search_text:
            search_text = '%' + search_text + '%'

            search_filter = """
                (title like %s or sku like %s)
            """
            params = [search_text, search_text]
            filter_query = search_filter + " and "

        for field, value in field_value_pairs.items():
            filter_query += field + " =%s and "
            params.append(value)

        filter_query = filter_query.strip().rstrip('and')

        sql_query += filter_query

        queryset = Product.objects.raw(sql_query, params)

        return queryset

    @staticmethod
    def get_queryset_from_raw(query_params):
        """

        """
        search_text = query_params.get('search')

        sql_query = """
            SELECT * FROM products;
        """

        if search_text:
            search_text = '%' + search_text + '%'

            sql_query = """
                SELECT * FROM products WHERE title like %s or sku like %s
            """
            params = [search_text, search_text]

            queryset = Product.objects.raw(sql_query, params)

            return queryset

        return Product.objects.raw(sql_query)


class UpdateProductAPI(UpdateAPIView):
    serializer_class = ProductsSerializer
    USE_ORM = True

    def get_queryset(self):
        """

        """
        if self.USE_ORM:
            return Product.objects.all()

        sql_query = """
            SELECT * FROM products;
        """
        return Product.objects.raw(sql_query)

    def get_object(self):
        """

        """
        pk = self.kwargs.get('pk')

        if pk and Product.objects.filter(pk=pk).exists():
            if self.USE_ORM:
                return Product.objects.filter(pk=pk).last()

            sql_query = """
                SELECT * FROM products WHERE id=%s;
            """

            return Product.objects.raw(sql_query, [pk])

        raise Http404


class DiscountProductBucketsAPI(APIView):
    bucket_1 = (None, 0)    # 0% discount
    bucket_2 = (0, 10)      # 0 - 10% discount
    bucket_3 = (10, 30)     # 10 - 30% discount
    bucket_4 = (30, 50)     # 30 - 50% discount
    bucket_5 = (50, None)   # > 50% discount

    buckets = {
        'bucket_1': {'bucket': bucket_1, 'label': '0%'},
        'bucket_2': {'bucket': bucket_2, 'label': '0 - 10%'},
        'bucket_3': {'bucket': bucket_3, 'label': '10 - 30%'},
        'bucket_4': {'bucket': bucket_4, 'label': '30 - 50%'},
        'bucket_5': {'bucket': bucket_5, 'label': '> 50%'},
    }

    def get(self, request, *args, **kwargs):
        """

        """
        try:
            data = self.get_result_from_orm()

            return Response(
                data=data,
                status=HTTP_200_OK
            )
        except Exception as e:

            return Response(
                data={'Error': e},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_result_from_orm(self):
        """

        """
        for bucket, bucket_data in self.buckets.items():
            values = bucket_data.get('bucket')

            if values[0] is not None and values[1] is not None:
                bucket_data.update(
                    {
                        'aggregate': Count('discount', filter=Q(discount__gte=values[0], discount__lte=values[1]))
                    }
                )

            elif values[0] is None:
                bucket_data.update(
                    {
                        'aggregate': Count('discount', filter=Q(discount=values[1]))
                    }
                )

            elif values[1] is None:
                bucket_data.update(
                    {
                        'aggregate': Count('discount', filter=Q(discount__gt=values[0]))
                    }
                )

        query_result = Product.objects.aggregate(
            bucket_1=self.buckets.get('bucket_1').get('aggregate'),
            bucket_2=self.buckets.get('bucket_2').get('aggregate'),
            bucket_3=self.buckets.get('bucket_3').get('aggregate'),
            bucket_4=self.buckets.get('bucket_4').get('aggregate'),
            bucket_5=self.buckets.get('bucket_5').get('aggregate')
        )

        data = dict()
        for bucket, bucket_data in self.buckets.items():
            data.update(
                {
                    bucket_data.get('label'): query_result.get(bucket, 0)
                }
            )

        return data


class DiscountProductBucketsRawQueryAPI(APIView):
    bucket_1 = (None, 0)    # 0% discount
    bucket_2 = (0, 10)      # 0 - 10% discount
    bucket_3 = (10, 30)     # 10 - 30% discount
    bucket_4 = (30, 50)     # 30 - 50% discount
    bucket_5 = (50, None)   # > 50% discount

    buckets = {
        'bucket_1': {'bucket': bucket_1, 'label': '0%'},
        'bucket_2': {'bucket': bucket_2, 'label': '0 - 10%'},
        'bucket_3': {'bucket': bucket_3, 'label': '10 - 30%'},
        'bucket_4': {'bucket': bucket_4, 'label': '30 - 50%'},
        'bucket_5': {'bucket': bucket_5, 'label': '> 50%'},
    }

    def get(self, request, *args, **kwargs):
        """

        """
        try:
            data = self.get_result_from_raw_query()

            return Response(
                data=data,
                status=HTTP_200_OK
            )
        except Exception as e:

            return Response(
                data={'Error': e},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_result_from_raw_query(self):
        """

        """
        sql_selection, params = self.get_sql_if_functions()

        sql_query = f"""
                    select  id {sql_selection} from products;
                """
        query_result = Product.objects.raw(sql_query, params)[0]

        data = dict()
        for bucket, bucket_data in self.buckets.items():

            data.update(
                {
                    bucket_data.get('label'): int(getattr(query_result, bucket)) if hasattr(query_result, bucket) else 0
                }
            )

        return data

    def get_sql_if_functions(self):
        """

        """
        sql_selection = ", "
        params = list()

        for bucket, bucket_data in self.buckets.items():
            bucket_values = bucket_data.get('bucket')

            if bucket_values[0] is not None and bucket_values[1] is not None:
                sql_selection += """ sum(if(discount>=%s and discount<=%s, 1, 0)) as %s, """
                params.extend([bucket_values[0], bucket_values[1], bucket])

            elif bucket_values[0] is None:
                sql_selection += """ sum(if(discount=%s, 1, 0)) as %s, """
                params.extend([bucket_values[1], bucket])

            elif bucket_values[1] is None:
                sql_selection += """ sum(if(discount>%s, 1, 0)) as %s, """
                params.extend([bucket_values[0], bucket])

        sql_selection = sql_selection.strip().rstrip(',')

        return sql_selection, params
