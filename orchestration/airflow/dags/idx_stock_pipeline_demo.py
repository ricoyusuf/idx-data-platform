import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="idx_stock_pipeline_demo",
    schedule=None,
    start_date=pendulum.datetime(
        2026, 1, 1, tz="Asia/Jakarta"
    ),
    catchup=False,
    tags=["idx-data-platform", "learning"],
)
def idx_stock_pipeline_demo():

    @task
    def prepare():
        print("DAG started successfully.")
        print("This is a demo task; no stock data is changed.")

    @task
    def finish():
        print("Demo workflow completed.")

    prepare() >> finish()


idx_stock_pipeline_demo()