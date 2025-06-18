{{ config(
    materialized='table',
    schema='main_dim'
) }}

SELECT 
    ROW_NUMBER() OVER (ORDER BY customer_id) as CustomerKey,
    customer_id as CustomerID,
    first_name || ' ' || last_name as FullName
FROM {{ ref('customer_raw') }}