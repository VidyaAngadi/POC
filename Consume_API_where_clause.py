from flask import Flask, jsonify
import snowflake.connector

app = Flask(__name__)

# Snowflake connection parameters
snowflake_config = {
    'user': 'Vidya',
    'password': 'Vidya@2001',
    'account': 'ha96914.ap-south-1.aws',
    'warehouse': 'POC_WH',
    'database': 'POC',
    'schema': 'PUBLIC'
}

# Function to execute a Snowflake query
def execute_query(query):
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return cursor, result

# API endpoint to retrieve data from a Snowflake table
@app.route('/api/table/MY_TABLE', methods=['GET'])
def get_table_data():
    query = 'SELECT * FROM MY_TABLE where id = 1'
    cursor, result = execute_query(query)

    if result:
        column_names = [desc[0] for desc in cursor.description]
        data = [dict(zip(column_names, row)) for row in result]
        cursor.close()
        return jsonify(data)
    else:
        return 'No data found for the specified table.'

if __name__ == '__main__':
    app.run()

