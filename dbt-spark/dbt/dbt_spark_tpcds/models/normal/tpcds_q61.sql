

WITH catalog_sales AS (
    select * from {{ source('external_source', 'catalog_sales') }}
),
store_sales AS (
    select * from {{ source('external_source', 'store_sales') }}
),
date_dim AS (
    select * from {{ source('external_source', 'date_dim') }}
),
store AS (
    select * from {{ source('external_source', 'store') }}
),
customer AS (
    select * from {{ source('external_source', 'customer') }}
),
customer_address AS (
    select * from {{ source('external_source', 'customer_address') }}
),
promotion AS (
    select * from {{ source('external_source', 'promotion') }}
),
item AS (
    select * from {{ source('external_source', 'item') }}
)
SELECT promotions,
       total,
       cast(promotions as decimal(15,4))/cast(total as decimal(15,4))*100
FROM
    (SELECT sum(ss_ext_sales_price) promotions
     FROM store_sales,
          store,
          promotion,
          date_dim,
          customer,
          customer_address,
          item
     WHERE ss_sold_date_sk = d_date_sk
       AND ss_store_sk = s_store_sk
       AND ss_promo_sk = p_promo_sk
       AND ss_customer_sk= c_customer_sk
       AND ca_address_sk = c_current_addr_sk
       AND ss_item_sk = i_item_sk
       AND ca_gmt_offset = -5
       AND i_category = 'Jewelry'
       AND (p_channel_dmail = 'Y'
         OR p_channel_email = 'Y'
         OR p_channel_tv = 'Y')
       AND s_gmt_offset = -5
       AND d_year = 1998
       AND d_moy = 11) promotional_sales cross join
    (SELECT sum(ss_ext_sales_price) total
     FROM store_sales,
          store,
          date_dim,
          customer,
          customer_address,
          item
     WHERE ss_sold_date_sk = d_date_sk
       AND ss_store_sk = s_store_sk
       AND ss_customer_sk= c_customer_sk
       AND ca_address_sk = c_current_addr_sk
       AND ss_item_sk = i_item_sk
       AND ca_gmt_offset = -5
       AND i_category = 'Jewelry'
       AND s_gmt_offset = -5
       AND d_year = 1998
       AND d_moy = 11) all_sales
ORDER BY promotions,
         total
    LIMIT 100