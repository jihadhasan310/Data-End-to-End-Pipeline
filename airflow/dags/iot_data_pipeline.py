from airflow import DAG
from airflow.operators.bash_operator import BashOperator # type: ignore
from airflow.utils.dates import days_ago # type: ignore

dag = DAG('iot_data_pipeline', default_args={'owner': 'airflow'}, schedule_interval='@daily', start_date=days_ago(1))

t1 = BashOperator(
    task_id='extract_data',
    bash_command='spark-submit --master local[2] /opt/spark-apps/kafka_to_hdfs.py',
    dag=dag
)

t2 = BashOperator(
    task_id='clean_and_enrich_data',
    bash_command='spark-submit --master local[2] /opt/spark-apps/enrich_and_clean_data.py',
    dag=dag
)

t3 = BashOperator(
    task_id='transform_data_to_druid',
    bash_command='spark-submit --master local[2] /opt/spark-apps/hdfs_to_druid.py',
    dag=dag
)

t4 = BashOperator(
    task_id='monitor_health',
    bash_command='curl -X GET http://prometheus:9090/api/v1/query?query=up',
    dag=dag
)

t1 >> t2 >> t3 >> t4
