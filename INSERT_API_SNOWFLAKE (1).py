from flask import Flask, jsonify, request
import snowflake.connector
import json

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
    conn.commit()  # Commit the transaction
    result = cursor.fetchall()
    cursor.close()
    return result

# Function to load JSON file
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to execute insert statements
def execute_inserts(data, table_name):
    for item in data:
        query = item['query'].replace('MY_TABLE', table_name)
        execute_query(query)

# API endpoint to execute insert statements from a JSON file
@app.route('/api/inserts/<table_name>', methods=['POST'])
def execute_inserts_from_api(table_name):
    file_path = r'C:\Users\vidya.angadi\POC\INSERT_API.json'  # Replace with the path to your JSON file
    try:
        data = load_json_file(file_path)
        execute_inserts(data, table_name)
        return jsonify({'message': 'Inserts executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# API endpoint to retrieve data from Snowflake table
@app.route('/api/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    query = f'SELECT * FROM {table_name}'
    try:
        result = execute_query(query)
        if result:
            column_names = [desc[0] for desc in result.cursor.description]
            data = [dict(zip(column_names, row)) for row in result]
            return jsonify(data)
        else:
            return jsonify({'message': 'No data found for the specified table.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
