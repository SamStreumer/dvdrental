{{ config(
    materialized='table',
    schema='main_fct'
) }}


SELECT 
    city_id as LocationKey,
    AVG(amount) as Amount_AVG
FROM (
    SELECT 
        (SELECT city_id FROM main.address WHERE address_id = 
            (SELECT address_id FROM main.customer WHERE customer_id = payment.customer_id LIMIT 1)
        LIMIT 1) as city_id,
        payment.amount
    FROM main.payment
) payment_with_city
WHERE city_id IS NOT NULL
GROUP BY city_id