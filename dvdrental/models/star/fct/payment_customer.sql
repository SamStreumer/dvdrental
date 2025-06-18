{{ config(
    materialized='table',
    schema='main_dim'
) }}

WITH customer_payments AS (
    SELECT
        customer_id,
        COUNT(*) as aantal_transacties,
        SUM(amount) as totale_opbrengst,
        AVG(amount) as gemiddelde_opbrengst
    FROM {{ ref('payment_raw') }}
    GROUP BY customer_id
)
SELECT 
    dc.CustomerKey,
    cp.gemiddelde_opbrengst as Amount_AVG,
    cp.totale_opbrengst as Amount_SUM
FROM customer_payments cp
JOIN {{ ref('Dim_Customer') }} dc ON cp.customer_id = dc.CustomerID