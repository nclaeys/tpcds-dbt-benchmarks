import argparse
from dbt.cli.main import dbtRunner


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launch dbt")
    parser.add_argument("-m", "--model", dest="model", help="the name of the model to execute with dbt", required=True)
    main_args = parser.parse_args()

    res = dbtRunner().invoke(["run", "--profiles-dir", "/opt/spark/work-dir/dbt", "--project-dir", "/opt/spark/work-dir/dbt/dbt_spark_tpcds", "--select", f"models/normal/tpcds_{main_args.model}.sql"])
    if not res.success:
        raise Exception(res.exception)
