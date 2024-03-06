# pip install -r requirements.txt
# # in requerements.txt
# # line1: mysql-connector-python
# # line2: 
import mysql.connector as mysql

def main():
    cnx = mysql.connect(
        user='user', 
        password='password', 
        database='mysql',
        host='127.0.0.1', 
        port=3306
    )
    cursor = cnx.cursor()

    # cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

    cursor.execute("CREATE TABLE IF NOT EXISTS Employee_info(id int, name varchar(255), job_title varchar(255), working_location varchar(255), working_status varchar(255),insert_update_date date, PRIMARY KEY (ID))")

    cursor.execute("INSERT INTO Employee_info VALUES (1, 'bla', 'SE', 'pune, India', 'working', '2023-12-01')")
    cursor.execute("INSERT INTO Employee_info VALUES (2, 'blabla', 'SE', 'pune, India', 'working', '2023-12-02')")

    cursor.execute("SELECT * FROM Employee_info")
    for row in cursor.fetchall():
        print(row)
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
