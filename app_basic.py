from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_sensor_data():
    return render_template('index.html')


@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():

    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        humidity = data.get('humidity')
        temperature = data.get('temperature')
        date_time = data.get('date_time')

        print(humidity)
        print(temperature)
        print(date_time)

        return 'Data received successfully.', 200
    else:
        return 'Invalid content type. Expected application/json.', 0
