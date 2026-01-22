from copy import error
import psycopg2

db_host = 'database-2.cfucyeaqyye6.us-east-2.rds.amazonaws.com'
db_name = 'dbresumatch'
db_user = 'postgres'
db_pass = 'Dev0g8resumatch'
connection = None
cursor = None
try:
    connection = psycopg2.connect(host = db_host, database = db_name, user = db_user, password = db_pass)

    cursor = connection.cursor()
   
    create_table_query = '''CREATE TABLE IF NOT EXISTS resumes (
    resume_id SERIAL PRIMARY KEY,
    user_id INT,
    s3_bucket VARCHAR(255),
    s3_key VARCHAR(500),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );'''
    
    cursor.execute(create_table_query)
    connection.commit()

except Exception as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()