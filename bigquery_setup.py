# pip install -r requirements.txt
# # in requerements.txt
# # line1: mysql-connector-python
# # line2: google-cloud-bigquery
# # line3: pandas-gbq

from google.cloud import bigquery

project_id = 'your project name'
dataset_name = 'mydataset'
table_name = 'employee_info_raw'
table_id = f'{dataset_name}.{table_name}'

# Create a BigQuery client.
client = bigquery.Client(project=project_id)

# create datset if not exists.
def create_dataset_bigquery(client, dataset_name):
  try :
    query = f"""
    CREATE SCHEMA IF NOT EXISTS {dataset_name} 
    OPTIONS(
      location="us"
      )
    """
    results = client.query(query).result()
    print("Dataset created")
  except Exception as e:
    print(f"Dataset could not be created, an error occured: {e}")

# create table if not exists
def create_table_bigquery(client, table_id):
  try:
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_id} (
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
    print("Table created")
  except Exception as e:
    print(f"Table could not be created, an error occured: {e}")


 # insert values in the table.
def insert_data_bigquery(client, table_id):
  try:
    query = f"""
    INSERT {table_id}
    VALUES (1, 'sachin', 'SE', 'pune, India', 'working', '1900-01-01')
    """
    results = client.query(query).result()
    print("Data inserted in the Table ")
  except Exception as e:
    print(f"Data could not be inserted, an error occured: {e}")

# Query the bigquery table 
def get_bigquery_data(client, table_id):
  try:
    query = f"""
    SELECT *
    FROM {table_id}
    """
    results = client.query(query).result()
    # Print the results.
    for row in results:
      print(row['name'])
  except Exception as e:
    print("Unable to query result, an error ocurred: {e}")

if __name__== "__main__":
    create_dataset_bigquery(client, dataset_name)
    create_table_bigquery(client, table_id)
    insert_data_bigquery(client, table_id)
    get_bigquery_data(client, table_id)



 
    
        
    




