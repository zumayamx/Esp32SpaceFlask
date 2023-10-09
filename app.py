from flask import Flask, request, render_template, jsonify
from datetime import date, datetime, timedelta
import mysql.connector

app = Flask(__name__)


def createConnection(user_name, database_name, user_password, host, port):
    cnx = mysql.connector.connect(
        user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)


@app.route('/', methods=['GET'])
def get_sensor_data():
    # Create a connection to the database
    cnx, cursor = createConnection(
            '..', '..', '..', 'localhost', '3306')

    # Query the database
    query = ("SELECT * FROM dht_sensor_data")

    # Execute the query
    cursor.execute(query)

    # Get the data
    data = cursor.fetchall()

    # Close the connection
    cursor.close()
    cnx.close()

    # Return the data
    return jsonify(data), 200


@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json

        humidity = data.get('humidity')
        temperature = data.get('temperature')
        date_time = data.get('date_time')
        ESP_name = data.get('ESP_name')

        cnx, cursor = createConnection(
            'sql10651035', 'sql10651035', 'tkQyMRXggg', 'sql10.freemysqlhosting.net', '3306')

        add_data = (
            "INSERT INTO dht_sensor_data (humidity, temperature, date_time, ESP_name) VALUES (%s, %s, %s, %s)")
        cursor.execute(add_data, (humidity, temperature, date_time, ESP_name))
        cnx.commit()
        cursor.close()
        cnx.close()

        return 'Data received successfully.', 200
    else:
        return 'Invalid content type. Expected application/json.', 400
