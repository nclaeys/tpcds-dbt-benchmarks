# Tpcds benchmark with dbt and Spark

Copied all queries from duckdb tpcds benchmark and made them work with s3 input/output.
The only change that needed to be performed on the initial queries was that Spark requires backticks instead of single quotes for column names.
This means the following changes need to be made:

### change quotes in names
```
SELECT sum(cs_ext_discount_amt) AS `excess discount amount`
```
instead of:
```
SELECT sum(cs_ext_discount_amt) AS "excess discount amount"
```

### different substring function
The `substring` function need to be replaced by the `substr` function


## Running dbt queries against Spark
Since dbt 1.5.0, dbt released their functional API, which makes it a lot easier to integrate dbt with the Spark session.
This results in exactly the same setup as is used when executing pyspark code.

The entrypoint for executing our dbt models is the `runner.py` file.
This is specified in our Airflow dag configuration by specifying the file in the application property.
In the `profiles.yml` we specify that we use the `session` option for connecting with the [Spark dbt adapter](https://docs.getdbt.com/docs/core/connect-data-platform/spark-setup).

## Results

We ran the benchmark for all queries on m.2xlarge machines, which have 8 vcpu and 32Gb of RAM and attached 100GB of disk storage.
The benchmarks use Spark in local mode, which means that both the driver and the executor run on the same node.

A couple of queries were not able to run, need to investigate further.
Did not investigate further for the blogpost as it will not change anything in my conclusions.  

| Query | Time (s) |
|-------|----------|
| q01   | 31.50    |
| q02   |          |
| q03   | 26.90    |
| q04   | 545.89   |
| q05   | 88.57    |
| q06   | 70.02    |
| q07   | 41.23    |
| q08   | 29.15    |
| q09   | 58.69    |
| q10   | 36.29    |
| q11   | 149.02   |
| q12   | 17.90    |
| q13   | 47.55    |
| q14   | 204.48   |
| q15   | 31.59    |
| q16   |          |
| q17   | 191.98   |
| q18   | 46.28    |
| q19   | 35.95    |
| q20   | 22.44    |
| q21   | 28.45    |
| q22   | 81.50    |
| q23   | 286.35   |
| q24   | 116.97   |
| q25   | 193.46   |
| q26   | 30.31    |
| q27   | 76.20    |
| q28   | 85.91    |
| q29   | 190.21   |
| q30   | 27.84    |
| q31   | 65.07    |
| q32   | 30.59    |
| q33   | 42.30    |
| q34   | 30.12    |
| q35   | 43.06    |
| q36   | 33.54    |
| q37   | 46.13    |
| q38   | 58.64    |
| q39   | 41.37    |
| q40   | 67.51    |
| q41   | 10.28    |
| q42   | 23.14    |
| q43   | 24.89    |
| q44   | 33.81    |
| q45   | 22.16    |
| q46   | 39.19    |
| q47   | 55.47    |
| q48   | 40.38    |
| q49   | 86.17    |
| q50   | 86.15    |
| q51   | 103.18   |
| q52   | 22.88    |
| q53   | 26.80    |
| q54   | 67.80    |
| q55   | 23.50    |
| q56   | 40.19    |
| q57   | 38.09    |
| q58   | 40.57    |
| q59   | 45.35    |
| q60   | 39.73    |
| q61   |          |
| q62   | 21.11    |
| q63   | 26.01    |
| q64   | 324.72   |
| q65   | 83.63    |
| q66   | 39.42    |
| q67   | 341.76   |
| q68   | 43.10    |
| q69   | 35.86    |
| q70   |          |
| q71   | 38.28    |
| q72   | 824.70   |
| q73   | 30.24    |
| q74   | 134.81   |
| q75   | 106.56   |
| q76   | 38.21    |
| q77   | 49.37    |
| q78   | 260.34   |
| q79   |          |
| q80   | 282.86   |
| q81   | 30.84    |
| q82   | 61.59    |
| q83   | 23.61    |
| q84   | 22.59    |
| q85   |          |
| q86   | 21.20    |
| q87   | 65.56    |
| q88   | 74.07    |
| q89   | 29.37    |
| q90   | 18.56    |
| q91   | 21.26    |
| q92   | 24.56    |
| q93   | 148.63   |
| q94   | 53.89    |
| q95   | 128.79   |
| q96   | 20.14    |
| q97   | 70.36    |
| q98   | 31.09    |
| q99   | 27.56    |

