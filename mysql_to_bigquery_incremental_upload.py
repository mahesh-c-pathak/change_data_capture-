# pip install -r requirements.txt
# # in requerements.txt
# # line1: mysql-connector-python
# # line2: google-cloud-bigquery
# # line3: pandas-gbq

import mysql.connector as mysql
from google.cloud import bigquery
import json
import pandas as pd
from collections import OrderedDict
import pandas_gbq

project_id = 'your project name'
dataset_name = 'your dataset name'
table_name = 'your table name'
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



# Query the bigquery table for max uploaded date
def get_latest_date(client, table_id):
  try:
    query = f"""
    SELECT MAX(insert_update_date)
    FROM {table_id}
    """
    results = client.query(query).result()
    # Print the results.
    latest_date = []
    for row in results:
      latest_date.append(row[0])
    return latest_date
  except Exception as e:
    print("Unable to query result, an error ocurred: {e}")

# Query the mysql table for rows greater than max uploaded date in bigquery
def incremental_load(latest_date):
  cnx = mysql.connect(
        user='user', 
        password='password', 
        database='mysql',
        host='127.0.0.1', 
        port=3306
    )
  cursor = cnx.cursor()
  mysql_query = "SELECT * FROM Employee_info WHERE insert_update_date > %s"
  cursor.execute(mysql_query, latest_date)
  rows = cursor.fetchall()
  return rows

# insert values in the bigquery table.
def insert_data_bigquery(new_records, project_id, table_id) :
  try:
    column_names=["id", "name", "job_title", "working_location", "working_status", "insert_update_date"]
    df = pd.DataFrame(new_records, columns=column_names)
    pandas_gbq.to_gbq(df, table_id, project_id, if_exists='append')
  except Exception as e:
    print(f"Data could not be inserted, an error occured: {e}")

if __name__== "__main__":
    create_dataset_bigquery(client, dataset_name)
    create_table_bigquery(client, table_id)
    latest_date = get_latest_date(client, table_id)
    new_records = incremental_load(latest_date)
    insert_data_bigquery(new_records,project_id, table_id)
    print("Data uploaded to bigquery")
    


 
    
        
    




