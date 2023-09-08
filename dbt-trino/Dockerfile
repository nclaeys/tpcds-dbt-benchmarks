FROM public.ecr.aws/dataminded/dbt:v1.4.0-1

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install --requirement requirements.txt

COPY . .

WORKDIR /app/dbt/dbt_trino_tpcds

ENV DBT_PROFILES_DIR="/app/dbt"
ENV DBT_PROJECT_DIR="/app/dbt/dbt_trino_tpcds"

# install dependencies
RUN dbt deps
