FROM public.ecr.aws/dataminded/spark-k8s-glue:v3.3.2-hadoop-3.3.5-v2

WORKDIR /opt/spark/work-dir
USER 0
COPY requirements.txt requirements.txt
#Put dependencies in it's own layer as a cache, if you change code only the code layer needs to be rebuild
RUN python3 -m pip install --no-cache-dir -r requirements.txt --no-dependencies

COPY . .
WORKDIR /opt/spark/work-dir/dbt/dbt_spark_tpcds

ENV PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
COPY dbt/profiles.yml /root/.dbt/profiles.yml

# install dependencies
RUN dbt deps
