-- models/raw/payment_raw.sql
SELECT * FROM {{ source('dvdrental', 'payment') }}