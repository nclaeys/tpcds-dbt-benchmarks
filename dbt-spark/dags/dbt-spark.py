from airflow import DAG
from conveyor.factories import ConveyorDbtTaskFactory
from conveyor.operators import ConveyorSparkSubmitOperatorV2
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
    "dbt-spark-tpcds", default_args=default_args, max_active_runs=1, concurrency=10
)

def run_tpcds_benchmark_for_model(modelName):
  ConveyorSparkSubmitOperatorV2(
      dag=dag,
      mode="local",
      task_id=f"dbt-spark-tpcds-m2xlarge-{modelName}",
      application="local:///opt/spark/work-dir/runner.py",
      aws_role="dbt-spark-tpcds-{{ macros.datafy.env() }}",
      application_args=["--model", f"{modelName}"],
      driver_instance_type="mx.2xlarge",
      instance_life_cycle="on-demand",
      executor_disk_size=100,
  )

for model in range(1,100):
  if model < 10:
    run_tpcds_benchmark_for_model(f"q0{model}")
  else:
    run_tpcds_benchmark_for_model(f"q{model}")

