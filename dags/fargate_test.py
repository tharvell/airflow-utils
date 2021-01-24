from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
# from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.contrib.operators.ecs_operator import ECSOperator


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
dag = DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
)

hello_world = ECSOperator(
    task_id="hello_world",
    dag=dag,
    aws_conn_id="aws_ecs",
    cluster="fargate-test",
    task_definition="hello-world",
    launch_type="FARGATE",
    overrides={
        "containerOverrides": [
            {
                "name": "hello-world-container",
                "command": ["echo", "hello", "world"],
            },
        ],
    },
    tags={
        "Customer": "X",
        "Project": "Y",
        "Application": "Z",
        "Version": "0.0.1",
        "Environment": "Development",
    },
    awslogs_group="/ecs/hello-world",
    awslogs_stream_prefix="prefix_b/hello-world-container",  # prefix with container name
)

hello_world