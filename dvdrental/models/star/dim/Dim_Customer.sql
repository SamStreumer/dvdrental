-- models/star/dim/Dim_Customer.sql

SELECT
    *
FROM {{ source('dvdrental', 'customer') }}