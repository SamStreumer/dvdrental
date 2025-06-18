{{ config(
    materialized='table',
    schema='main_dim'
) }}

SELECT
    ROW_NUMBER() OVER (ORDER BY a.address_id) as LocationKey,
    a.address_id as AddressID,
    ci.city || ', ' || co.country as CityCountry
FROM {{ ref('address_raw') }} a
JOIN {{ ref('city_raw') }} ci ON a.city_id = ci.city_id
JOIN {{ ref('country_raw') }} co ON ci.country_id = co.country_id