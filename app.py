from flask import Flask, request, render_template, jsonify
from datetime import date, datetime, timedelta
import mysql.connector
from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
            'sql3664252', 'sql3664252', 'IqYKx2ZXzW', 'sql3.freemysqlhosting.net', '3306')

    # Query the database
    query = ("SELECT * FROM sensor_data")

    # Execute the query
    cursor.execute(query)

    # Get the data
    data = cursor.fetchall()

    # Close the connection
    cursor.close()
    cnx.close()

        # Obtener los valores de x e y desde los datos
    x = [item[0] for item in data]
    y1 = [item[1] for item in data]
    y2 = [item[2] for item in data]

    # Crear la gráfica
    plt.figure(figsize=(8, 4))
    plt.plot(x, y1, label='Temperatura')
    plt.plot(x, y2, label='Humedad')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # Guardar la gráfica en un archivo temporal
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode()

    # Renderizar la plantilla HTML con la gráfica
    return render_template('index.html', img_data=img_data)

    # Return the data
    # return , 200


@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json

        humidity = data.get('humidity')
        temperature = data.get('temperature')
        gas = data.get('gas')
        humedad_tierra = data.get('hum_tierra')
        intensidad_luz = data.get('inten_luz')

        cnx, cursor = createConnection('sql3664252', 'sql3664252', 'IqYKx2ZXzW', 'sql3.freemysqlhosting.net', '3306')

        add_data = ("INSERT INTO sensor_data (humidity, temperature, gas, humit, intensidad_luz ) VALUES (%s, %s, %s, %s, %s)")
        
        cursor.execute(add_data, (humidity, temperature, gas, humedad_tierra, intensidad_luz))
        cnx.commit()
        cursor.close()
        cnx.close()

        return 'Data received successfully.', 200
    else:
        return 'Invalid content type. Expected application/json.', 400

