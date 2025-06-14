-- models/star/fct/Fact_Payment.sql

SELECT
    customer_id,
    SUM(amount) AS total_paid
FROM {{ source('dvdrental', 'payment') }}
GROUP BY customer_id
ORDER BY customer_id