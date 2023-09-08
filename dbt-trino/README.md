# Tpcds benchmarking with dbt and Trino

Started from the queries used for dbt with duckdb.
Needed to modify the queries since Trino syntax requires an explicit alias for aggregation columns. 
This means that the following changes in many queries:

```
SELECT avg(ss_quantity) agg1,
FROM store_sales
```

instead of:
```
SELECT avg(ss_quantity),
FROM store_sales
```

## Results

We ran the benchmark for all Trino queries using the following trino configuration:
- 1 coordinator node on mx.2xlarge on-demand node
- 1 worker nodes on mx.2xlarge on-demand node
- max query memory per node: 16Gb
- max JVM max heap: 24Gb

mx.2xlarge machines have:
- 8 vcpu 
- 32Gb of RAM 
- we attached 100GB of disk storage but this seems to not be used by trino for spilling on these queries and datasets

For executing the queries with dbt we use the [dbt Trino adapter](https://github.com/starburstdata/dbt-trino)
Q70 does not work because Trino does not support correlated query syntax (need to investigate if we can reformulate the query):
`Given correlated subquery is not supported`

| Query | Trino (s) |
|-------|-----------|
| q01   | 7.38      |
| q02   | 28.28     |
| q03   | 22.33     |
| q04   | 354.57    |
| q05   | 25.22     |
| q06   | 54.67     |
| q07   | 23.91     |
| q08   | 19.52     |
| q09   | 22.86     |
| q10   | 12.56     |
| q11   | 225.64    |
| q12   | 12.57     |
| q13   | 117.94    |
| q14   | 333.01    |
| q15   | 8.95      |
| q16   | 75.78     |
| q17   | 30.29     |
| q18   | 10.32     |
| q19   | 20.87     |
| q20   | 9.91      |
| q21   | 27.76     |
| q22   | 93.56     |
| q23   | 214.32    |
| q24   | 51.12     |
| q25   | 34.07     |
| q26   | 9.94      |
| q27   | 55.38     |
| q28   | 20.05     |
| q29   | 36.46     |
| q30   | 7.07      |
| q31   | 39.47     |
| q32   | 6.05      |
| q33   | 17.27     |
| q34   | 16.92     |
| q35   | 22.53     |
| q36   | 72.11     |
| q37   | 13.19     |
| q38   | 41.08     |
| q39   | 64.36     |
| q40   | 15.09     |
| q41   | 2.48      |
| q42   | 24.22     |
| q43   | 23.79     |
| q44   | 10.61     |
| q45   | 20.91     |
| q46   | 25.02     |
| q47   | 322.21    |
| q48   | 116.01    |
| q49   | 18.34     |
| q50   | 32.86     |
| q51   | 45.93     |
| q52   | 16.35     |
| q53   | 30.07     |
| q54   | 24.61     |
| q55   | 16.79     |
| q56   | 16.91     |
| q57   | 55.25     |
| q58   | 129.86    |
| q59   | 51.99     |
| q60   | 18.99     |
| q61   | 72.51     |
| q62   | 20.22     |
| q63   | 29.4      |
| q64   | 118.74    |
| q65   | 41.21     |
| q66   | 38.89     |
| q67   | 195.89    |
| q68   | 25.82     |
| q69   | 13.28     |
| q70   | /         |
| q71   | 18.95     |
| q72   | 2863.07   |
| q73   | 14.3      |
| q74   | 95.37     |
| q75   | 58.01     |
| q76   | 10.34     |
| q77   | 20.31     |
| q78   | 77.46     |
| q79   | 36.80     |
| q80   | 61.24     |
| q81   | 6.82      |
| q82   | 19.05     |
| q83   | 25.28     |
| q84   | 5.29      |
| q85   | 18.91     |
| q86   | 6.8       |
| q87   | 40.21     |
| q88   | 81.98     |
| q89   | 36.66     |
| q90   | 7.64      |
| q91   | 7.73      |
| q92   | 10.77     |
| q93   | 25.82     |
| q94   | 15.28     |
| q95   | 27.22     |
| q96   | 46.24     |
| q97   | 22.99     |
| q98   | 38.15     |
| q99   | 24.59     |

