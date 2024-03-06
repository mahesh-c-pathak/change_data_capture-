# pip install -r requirements.txt
# # in requerements.txt
# # line1: mysql-connector-python
# # line2: google-cloud-bigquery
# # line3: pandas-gbq

from google.cloud import bigquery

project_id = 'your project name'
dataset_name = 'mydataset'
table_name = 'employee_info_raw'
table_id = 'mydataset.employee_info_raw'

# Create a BigQuery client.
client = bigquery.Client(project=project_id)

# create datset if not exists.
def create_dataset_bigquery(client):
  try :
    query = """
    CREATE SCHEMA IF NOT EXISTS mydataset 
    OPTIONS(
      location="us"
      )
    """
    results = client.query(query).result()
  except Exception as e:
    print(f"Dataset could not be created, an error occured: {e}")

# create table if not exists
def create_table_bigquery(client):
  try:
    query = """
    CREATE TABLE IF NOT EXISTS mydataset.employee_info_raw (
    id INT64,
    name STRING,
    job_title STRING,
    working_location STRING,
    working_status STRING,
    insert_update_date DATE)
    PARTITION BY insert_update_date
    OPTIONS(
    description="Bq Table to Store CloudSql Employee Table data"
    ); 
    """
    results = client.query(query).result()
  except Exception as e:
    print(f"Table could not be created, an error occured: {e}")

 # insert values in the table.
def insert_data_bigquery(client):
  try:
    query = """
    INSERT `mydataset.employee_info_raw` (id, name, job_title, working_location, working_status, insert_update_date )
    VALUES (1, 'sachin', 'SE', 'pune, India', 'working', '1900-01-01')
    """
    results = client.query(query).result()
    print("Data inserted in the Table ")
  except Exception as e:
    print(f"Data could not be inserted, an error occured: {e}")

# Query the bigquery table for max uploaded date
def get_bigquery_data(client):
  try:
    query = """
    SELECT *
    FROM `gcs-pipeline.demo_dataset.demo_table`
    """
    results = client.query(query).result()
    # Print the results.
    for row in results:
      print(row['name'])
  except Exception as e:
    print("Unable to query result, an error ocurred: {e}")

if __name__== "__main__":
    create_dataset_bigquery(client)
    create_table_bigquery(client)
    insert_data_bigquery(client)
    get_bigquery_data(client)



 
    
        
    




