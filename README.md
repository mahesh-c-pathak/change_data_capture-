# Change_Data_Capture (CDC)

The project is going to explore change_data_capture technique to incrementally load data from  Transactional processing system to Analytical processing system.  
Any new transactions or changes in the earlier transactions in an RDBMS transactional processing system are called incremental records.  
To perform incremental data load, synchronize new/changed data from RDBMS (here MYSQL) to analytical processing system(here BigQuery).

## Problem Statement:
A company wants to maintain its employees' details in an RDBMS system’s MySQL table on a daily basis. And this data needs to be incrementally imported into the BigQuery table on a daily basis for analytical purposes.

Employee details are added to the MySQL table as a record of their present working status. If they are new or are presently working in the company, the working status is marked as ‘Working’ in the column working_status.

If an employee has left the company or is not working actively, the record would be updated with the change to the column working_status value to ‘Not Working’. Other changes to the employee column info are also updated in the table.

 MySQL table Details where employees’ info will be stored on a daily basis is as below
 
```
 CREATE TABLE IF NOT EXISTS organization_info_tables. Employee_info
(
id int,
name varchar(255),
job_title varchar(255),
working_location varchar(255),
working_status varchar(255),
insert_update_date date,
PRIMARY KEY (ID)
); 
```

Any of the additions or updates in the records are identified with a date type column insert_update_date, so we can choose this column for incrementally loading data.

Target BigQuery details →

Target table schema:

```
CREATE TABLE organization_info_raw_tables.employee_info_raw (
id INT64,
name STRING,
job_title STRING,
working_location STRING,
working_status STRING,
insert_update_date DATE)
PARTITION BY insert_update_date
OPTIONS(
description=”Bq Table to Store MySql Employee Table data”
);  
```

## Setup  

Here we are going to use containerized MySQL.  
1. Clone the repository:
   
   ```
   git clone https://github.com/mahesh-c-pathak/change_data_capture-.git
   ```
2. Install the requiered python libraries
    
   ```
   pip install -r requirements.txt
   ```
3. Navigate to the project directory:
    
   ```
   cd mysql 
   ```
4. Run Docker Compose to spin up the services:
   
   ```
   docker-compose up
   ```
5. Run mysql_insert_data.py to insert records in the MySQL instance
    
   ```
   python3 mysql_insert_data.py
   ```
6. Enable “BigQuery Connection API”, “BigQuery Data Transfer API” and grant bigquery.admin role:

7. Run the bigquery_setup.py.
    * create datset
    * create table
    * Insert an initial (first time) lower limit date to the BigQuery table to start the first and subsequent dates incremental loads from source MySQL table to BigQuery table.
  
   ```
   python3 bigquery_setup.py
   ```

## Solution for implementing this incremental load problem:
Run the mysql_to_bigquery_incremental_upload.py. The Python Script 
 * Query the bigquery table for max uploaded date
 * Then Query the mysql table for incremental rows, viz rows greater than max uploaded date in bigquery
 * Then inserts incremental rows in the bigquery table. 

 ```
 python3 mysql_to_bigquery_incremental_upload.py
 ```
   This python file uses pandas to create a dataframe using incremental rows from MySQL. Then uses 'pandas-gbq' module to upload the data to bigquery table.
   This task can be automated and scheduled by airflow or cron-job to run at specified inteerval.


