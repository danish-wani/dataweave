
# Django REST Project

A Simple Django Rest project which providees the following APIs:

Products listing, searching, filtering and discount bucket APIs.


## API Reference

#### Get all products using ORM

```http
  GET /api/v1/products/
```

#### Get all products using Raw SQL query

```http
  GET /api/v2/products/
```


#### Get all products having search text in either sku or title field using ORM query

```http
  GET /api/v1/products/?search=${search_text}
```

#### Get all products having search text in either sku or title field using Raw SQL query

```http
  GET /api/v2/products/?search=${search_text}
```


#### Get all products having value in given field using ORM query

```http
  GET /api/v1/products/?source=${source_name}
```

#### Get all products having value in given field using Raw SQL query

```http
  GET /api/v2/products/?category=${category_name}
```





#### Update Product

```http
  PUT /api/v1/products/${pk}/
  PATCH /api/v1/products/${pk}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. Id of item to fetch |


#### Request Body

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `brand`      | `string` | **Optional**. Brand name |
| `category`      | `string` | **Optional**. Category name |
| `sub_category`      | `string` | **Optional**. Sub Category name |
| `product_type`      | `string` | **Optional**. Product type |



  
## Optimizations

Firstly I haved added pagination to all GET queries, records per page are set to 10 only.

For discount-buckets API, the raw SQL query is optimized and uses only a single query to fetch the count of all discount buckets.

`SELECT  id ,  SUM(IF(discount=0, 1, 0)) AS bucket_1, SUM(IF(discount>=0 and discount<=10, 1, 0)) AS bucket_2, SUM(IF(discount>=10 and discount<=30, 1, 0)) AS bucket_3, SUM(IF(discount>=30 and discount<=50, 1, 0)) AS bucket_4, 
SUM(IF(discount>50, 1, 0)) AS bucket_5 FROM products;`


I have used SQL **IF function** for getting the counts of different discount buckets in a single query.


Also the **ORM** for the above use the ORM aggregation to fetch the count in a single ORM query
## Environment Variables

You can optionally add env variable in the .env file and define the following Variables in there;

`DEBUG`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_HOST`

`DB_PORT`

  
## Installation 

Install dataweave project

```bash 
  # create virtual environment 

  virtualenv -p python3 env_dataweave
  source env_dataweave/bin/activate
  
  # clone repo
  git clone https://github.com/danish-wani/dataweave.git

  cd dataweave

  # install requirements
  pip install -r requirements.txt

  # set env variables in .env

  # run migrations
  python manage.py migrate


  # load .sql file which contains only insert statements

  
  # if you are using MySQL
  mysql -u <username> -p <password>  <database_name>  <  <sql_file>

  # Add the below variable in mysql conf under [mysqld]
  sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
  sudo service mysql restart
  
  # run tests
  python manage.py test


  #run server
  python manage.py runserver

  
```
    
