# Tpcds-dbt-benchmarks

I created this repository for a blogpost, I wrote, comparing 3 SQL engines (e.g. Spark, Duckdb, Trino) with dbt.
The blogpost can be found [here](https://medium.com/datamindedbe/head-to-head-comparison-of-dbt-sql-engines-497d71535881).
This repository contains the tpcds queries inside a standard dbt project, which uses the respective dbt adapter. 

## Prerequisites

### Data 
The data is generated using the [Databricks toolkit](https://github.com/databricks/tpcds-kit) together with the [Databricks sql perf](https://github.com/databricks/spark-sql-perf).
The resulting jars are added to a spark docker container following the instructions provided in [eks spark benchmark](https://github.com/aws-samples/eks-spark-benchmark) and the full setup can be seen in `data/Dockerfile`.

#### Generate data locally
We use dsdgen of the databricks toolkit for generating the data. An example on how to use the resulting docker image:

```shell
docker build -f data/Dockerfile -t tpcds-benchmark .
docker run -v /tmp/tpcds:/var/data -it sql-benchmark /opt/spark/bin/spark-submit --master "local[*]" --name somename \
       --deploy-mode client --class com.amazonaws.eks.tpcds.DataGeneration local:///opt/spark/work-dir/eks-spark-benchmark-assembly-1.0.jar \ 
       /var/data /opt/tpcds-kit/tools parquet 1 10 false false true # These are the application arguments required by the DataGeneration class: data location, path to tpcds toolkit, data format, scale factor, number partitions, create partitioned fact tables, shuffle to get partitions into single files, set logging to WARN 
```

The previous command generates all input data as parquet files with a scale factor of 1 and 10 partitions (For the benchmark we used 100 and 100 as values). If you want to generate more date, you should change the corresponding parameters.
The data is written to `/var/data` in the docker container which is mounted under `/tmp/tpcds`.

#### Generate data on eks
The same Spark container can be used when generating data in eks. If you add a role to the pod, you can directly write data to a s3 path. 

## Tpc-ds results

We ran the benchmark for all queries on m.2xlarge machines, which have 8 vcpu and 32Gb of RAM and attached 100GB of disk storage.
All except 5 queries return successfully. I need to investigate further why these 5 queries go OOM, even on larger instances.

| Query | Trino (s) | Duckdb (s) | Spark (s) |
|-------|-----------|------------|-----------|
| q01   | 7.38      | 9.55       | 31.50     |
| q02   | 28.28     | 18.12      |           |
| q03   | 22.33     | 11.46      | 26.90     |
| q04   | 354.57    | 83.04      | 545.89    |
| q05   | 25.22     | 42.64      | 88.57     |
| q06   | 54.67     | 41.28      | 70.02     |
| q07   | 23.91     | 21.72      | 41.23     |
| q08   | 19.52     | 13.75      | 29.15     |
| q09   | 22.86     | 59.95      | 58.69     |
| q10   | 12.56     | 20.16      | 36.29     |
| q11   | 225.64    | 47.93      | 149.02    |
| q12   | 12.57     | 5.15       | 17.90     |
| q13   | 117.94    | 29.36      | 47.55     |
| q14   | 333.01    | 147.68     | 204.48    |
| q15   | 8.95      | 11.69      | 31.59     |
| q16   | 75.78     | 27.44      |           |
| q17   | 30.29     | 18.74      | 191.98    |
| q18   | 10.32     | 16.84      | 46.28     |
| q19   | 20.87     | OOM        | 35.95     |
| q20   | 9.91      | 5.05       | 22.44     |
| q21   | 27.76     | 8.73       | 28.45     |
| q22   | 93.56     | 26.91      | 81.50     |
| q23   | 214.32    | OOM        | 286.35    |
| q24   | 51.12     | 25.96      | 116.97    |
| q25   | 34.07     | 21.31      | 193.46    |
| q26   | 9.94      | 10.65      | 30.31     |
| q27   | 55.38     | 42.43      | 76.20     |
| q28   | 20.05     | 45.84      | 85.91     |
| q29   | 36.46     | 15.92      | 190.21    |
| q30   | 7.07      | 10.01      | 27.84     |
| q31   | 39.47     | 31.35      | 65.07     |
| q32   | 6.05      | 9.58       | 30.59     |
| q33   | 17.27     | 21.29      | 42.30     |
| q34   | 16.92     | 7.89       | 30.12     |
| q35   | 22.53     | 13.10      | 43.06     |
| q36   | 72.11     | 30.01      | 33.54     |
| q37   | 13.19     | 12.73      | 46.13     |
| q38   | 41.08     | 15.84      | 58.64     |
| q39   | 64.36     | 14.14      | 41.37     |
| q40   | 15.09     | 8.84       | 67.51     |
| q41   | 2.48      | 1.16       | 10.28     |
| q42   | 24.22     | 7.15       | 23.14     |
| q43   | 23.79     | 8.14       | 24.89     |
| q44   | 10.61     | 20.78      | 33.81     |
| q45   | 20.91     | 6.02       | 22.16     |
| q46   | 25.02     | 13.50      | 39.19     |
| q47   | 322.21    | 53.80      | 55.47     |
| q48   | 116.01    | 13.83      | 40.38     |
| q49   | 18.34     | 35.11      | 86.17     |
| q50   | 32.86     | 11.07      | 86.15     |
| q51   | 45.93     | 43.87      | 103.18    |
| q52   | 16.35     | 7.17       | 22.88     |
| q53   | 30.07     | 8.68       | 26.80     |
| q54   | 24.61     | 67.14      | 67.80     |
| q55   | 16.79     | 6.87       | 23.50     |
| q56   | 16.91     | 19.42      | 40.19     |
| q57   | 55.25     | 27.39      | 38.09     |
| q58   | 129.86    | 23.86      | 40.57     |
| q59   | 51.99     | 29.74      | 45.35     |
| q60   | 18.99     | 18.17      | 39.73     |
| q61   | 72.51     | 22.46      |           |
| q62   | 20.22     | 4.42       | 21.11     |
| q63   | 29.4      | 8.64       | 26.01     |
| q64   | 118.74    | OOM        | 324.72    |
| q65   | 41.21     | 29.27      | 83.63     |
| q66   | 38.89     | 14.57      | 39.42     |
| q67   | 195.89    | 521.49     | 341.76    |
| q68   | 25.82     | 15.25      | 43.10     |
| q69   | 13.28     | 14.55      | 35.86     |
| q70   | /         | 20.36      |           |
| q71   | 18.95     | 22.41      | 38.28     |
| q72   | 2863.07   | 47.15      | 824.70    |
| q73   | 14.3      | 7.76       | 30.24     |
| q74   | 95.37     | 33.63      | 134.81    |
| q75   | 58.01     | 53.12      | 106.56    |
| q76   | 10.34     | 15.83      | 38.21     |
| q77   | 20.31     | 29.11      | 49.37     |
| q78   | 77.46     | 63.17      | 260.34    |
| q79   | 36.80     | 13.92      |           |
| q80   | 61.24     | 48.35      | 282.86    |
| q81   | 6.82      | 8.38       | 30.84     |
| q82   | 19.05     | 14.79      | 61.59     |
| q83   | 25.28     | 8.15       | 23.61     |
| q84   | 5.29      | 5.24       | 22.59     |
| q85   | 18.91     | 12.43      |           |
| q86   | 6.8       | 5.28       | 21.20     |
| q87   | 40.21     | 17.78      | 65.56     |
| q88   | 81.98     | 31.30      | 74.07     |
| q89   | 36.66     | 9.75       | 29.37     |
| q90   | 7.64      | 5.95       | 18.56     |
| q91   | 7.73      | 5.09       | 21.26     |
| q92   | 10.77     | 7.26       | 24.56     |
| q93   | 25.82     | 15.25      | 148.63    |
| q94   | 15.28     | 13.10      | 53.89     |
| q95   | 27.22     | OOM        | 128.79    |
| q96   | 46.24     | 4.88       | 20.14     |
| q97   | 22.99     | 20.31      | 70.36     |
| q98   | 38.15     | 7.73       | 31.09     |
| q99   | 24.59     | 7.05       | 27.56     |
