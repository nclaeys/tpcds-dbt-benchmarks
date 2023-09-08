from airflow import DAG
from conveyor.factories import ConveyorDbtTaskFactory
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import datetime, timedelta


default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": datetime.now() - timedelta(days=2),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "dbt-trino-tpcds", default_args=default_args, schedule_interval="@daily", max_active_runs=1, concurrency=1
)

def run_tpcds_benchmark_for_model(modelName):
  ConveyorContainerOperatorV2(
      dag=dag,
      task_id=f"dbt-tpcds-{modelName}",
      arguments=["build", "--profiles-dir", "/app/dbt", "--project-dir", "/app/dbt/dbt_trino_tpcds", "--target", "trino", "--select", f"models/normal/tpcds_{modelName}.sql"],
      instance_type="mx.micro",
      instance_life_cycle="on-demand",
  )

for model in range(1,100):
  if model < 10:
    run_tpcds_benchmark_for_model(f"q0{model}")
  else:
    run_tpcds_benchmark_for_model(f"q{model}")

