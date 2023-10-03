from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime
from flask_pymongo import PyMongo
from api import app

# app = Flask(__name__)
#
# app.config.from_object(Config)
# app.config["MONGO_URI"] = "mongodb://mongo:4+Dee54ahcfB2-1fa2e2+EdDab1DD4Da@mongodb.railway.internal:27017"
#
# mongo = PyMongo(app)

parking_records = []

if not os.path.exists('parking_records.json'):
    with open('parking_records.json', 'w') as json_file:
        json.dump([], json_file)

with open('parking_records.json', 'r') as json_file:
    parking_records = json.load(json_file)

def save_records():
    with open('parking_records.json', 'w') as json_file:
        json.dump(parking_records, json_file, indent=4)

def validate_license_plate(plate):
    import re
    regex = r'^[A-Z]{3}-\d{4}$'
    return bool(re.match(regex, plate))

def is_plate_registered(plate):
    return any(record['plate'] == plate for record in parking_records)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/parking', methods=['GET', 'POST'])
def register_entry_page():
    if request.method == 'POST':
        data = request.form
        plate = data.get('plate')
        paid = data.get('paid')
        vehicle_id = data.get('vehicle_id')

        if not plate:
            return jsonify(error='A matricula e obrigatoria'), 400

        if not validate_license_plate(plate):
            return jsonify(error='Formato de placa invalido'), 400

        if is_plate_registered(plate):
            return jsonify(error='Placa ja registrada na entrada'), 400

        reservation_id = len(parking_records) + 1

        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        parking_record = {
            'id': reservation_id,
            'plate': plate,
            'time': entry_time,
            'paid': paid == '1',
            'left': False
        }

        parking_records.append(parking_record)
        save_records()

        # return jsonify(message='Entrada registrada com sucesso', reservation_id=reservation_id), 201
        return render_template('register_exit.html', vehicle_id=vehicle_id)

    return render_template('register_entry.html')


@app.route('/parking/<int:vehicle_id>/out', methods=['GET', 'POST'])
def register_exit_page(vehicle_id):
    if request.method == 'POST':
        paid = int(request.form.get('paid'))

        parking_record = next((record for record in parking_records if record['id'] == vehicle_id), None)

        if parking_record is None:
            return jsonify(error='veiculo nao encontrado'), 404

        parking_record['paid'] = bool(paid)

        if not parking_record['paid']:
            return jsonify(error='Saida nao permitida, o pagamento nao foi efetuado.'), 400

        parking_record['left'] = True

        return jsonify(message='Pagamento efetuado, o veiculo saiu.'), 200

    return render_template('register_exit.html', vehicle_id=vehicle_id)


@app.route('/parking/<int:id>/out', methods=['PUT', 'GET'])
def register_exit(id):
    if request.method == 'PUT':
        parking_record = next((record for record in parking_records if record['id'] == id), None)

        if parking_record is None:
            return jsonify(error='Reserva nao encontrada'), 404

        if not parking_record['paid']:
            return jsonify(error='e necessario pagar antes de sair'), 400

        plate = parking_record['plate']
        if not is_plate_registered(plate):
            return jsonify(error='Placa nao registrada na entrada'), 400

        parking_record['left'] = True
        return jsonify(message='O veiculo saiu'), 200

    return render_template('register_exit.html')

@app.route('/parking/register_exit', methods=['GET'])
def register_exit_page2():
    return render_template('register_exit.html')

# Payment: Register payment
@app.route('/parking/<int:id>/pay', methods=['PUT'])
def register_payment(id):
    parking_record = next((record for record in parking_records if record['id'] == id), None)

    if parking_record is None:
        return jsonify(error='Reserva nao encontrada'), 404

    parking_record['paid'] = True
    return jsonify(message='Pagamento efetuado'), 200

@app.route('/parking/<plate>', methods=['GET'])
def get_history(plate):
    history = []

    for record in parking_records:
        if record['plate'] == plate:
            history.append({
                'id': record['id'],
                'time': record['time'],
                'paid': record['paid'],
                'left': record['left']
            })

    return jsonify(history=history), 200

@app.route('/history', methods=['GET'])
def parking_history():
    history = []

    for record in parking_records:
        if record['left']:
            entry_time = record['time']
            exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            paid_status = 'Pago' if record['paid'] else 'Não Pago'

            history.append({
                'plate': record['plate'],
                'entry_time': entry_time,
                'exit_time': exit_time,
                'paid': paid_status
            })

    return render_template('history.html', history=history)


@app.route('/get_data', methods=['GET'])
def get_data():

    data = mongo.db.exemplo.find()

    return jsonify({"message": "Consulta ao MongoDB bem-sucedida", "data": data})
from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime
from api.config import Config
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object(Config)
app.config["MONGO_URI"] = "mongodb://mongo:4+Dee54ahcfB2-1fa2e2+EdDab1DD4Da@mongodb.railway.internal:27017"

mongo = PyMongo(app)

parking_records = []

if not os.path.exists('parking_records.json'):
    with open('parking_records.json', 'w') as json_file:
        json.dump([], json_file)

with open('parking_records.json', 'r') as json_file:
    parking_records = json.load(json_file)

def save_records():
    with open('parking_records.json', 'w') as json_file:
        json.dump(parking_records, json_file, indent=4)

def validate_license_plate(plate):
    import re
    regex = r'^[A-Z]{3}-\d{4}$'
    return bool(re.match(regex, plate))

def is_plate_registered(plate):
    return any(record['plate'] == plate for record in parking_records)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/parking', methods=['GET', 'POST'])
def register_entry_page():
    if request.method == 'POST':
        data = request.form
        plate = data.get('plate')
        paid = data.get('paid')
        vehicle_id = data.get('vehicle_id')

        if not plate:
            return jsonify(error='A matricula e obrigatoria'), 400

        if not validate_license_plate(plate):
            return jsonify(error='Formato de placa invalido'), 400

        if is_plate_registered(plate):
            return jsonify(error='Placa ja registrada na entrada'), 400

        reservation_id = len(parking_records) + 1

        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        parking_record = {
            'id': reservation_id,
            'plate': plate,
            'time': entry_time,
            'paid': paid == '1',
            'left': False
        }

        parking_records.append(parking_record)
        save_records()

        # return jsonify(message='Entrada registrada com sucesso', reservation_id=reservation_id), 201
        return render_template('register_exit.html', vehicle_id=vehicle_id)

    return render_template('register_entry.html')


@app.route('/parking/<int:vehicle_id>/out', methods=['GET', 'POST'])
def register_exit_page(vehicle_id):
    if request.method == 'POST':
        paid = int(request.form.get('paid'))

        parking_record = next((record for record in parking_records if record['id'] == vehicle_id), None)

        if parking_record is None:
            return jsonify(error='veiculo nao encontrado'), 404

        parking_record['paid'] = bool(paid)

        if not parking_record['paid']:
            return jsonify(error='Saida nao permitida, o pagamento nao foi efetuado.'), 400

        parking_record['left'] = True

        return jsonify(message='Pagamento efetuado, o veiculo saiu.'), 200

    return render_template('register_exit.html', vehicle_id=vehicle_id)


@app.route('/parking/<int:id>/out', methods=['PUT', 'GET'])
def register_exit(id):
    if request.method == 'PUT':
        parking_record = next((record for record in parking_records if record['id'] == id), None)

        if parking_record is None:
            return jsonify(error='Reserva nao encontrada'), 404

        if not parking_record['paid']:
            return jsonify(error='e necessario pagar antes de sair'), 400

        plate = parking_record['plate']
        if not is_plate_registered(plate):
            return jsonify(error='Placa nao registrada na entrada'), 400

        parking_record['left'] = True
        return jsonify(message='O veiculo saiu'), 200

    return render_template('register_exit.html')

@app.route('/parking/register_exit', methods=['GET'])
def register_exit_page2():
    return render_template('register_exit.html')

# Payment: Register payment
@app.route('/parking/<int:id>/pay', methods=['PUT'])
def register_payment(id):
    parking_record = next((record for record in parking_records if record['id'] == id), None)

    if parking_record is None:
        return jsonify(error='Reserva nao encontrada'), 404

    parking_record['paid'] = True
    return jsonify(message='Pagamento efetuado'), 200

@app.route('/parking/<plate>', methods=['GET'])
def get_history(plate):
    history = []

    for record in parking_records:
        if record['plate'] == plate:
            history.append({
                'id': record['id'],
                'time': record['time'],
                'paid': record['paid'],
                'left': record['left']
            })

    return jsonify(history=history), 200

@app.route('/history', methods=['GET'])
def parking_history():
    history = []

    for record in parking_records:
        if record['left']:
            entry_time = record['time']
            exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            paid_status = 'Pago' if record['paid'] else 'Não Pago'

            history.append({
                'plate': record['plate'],
                'entry_time': entry_time,
                'exit_time': exit_time,
                'paid': paid_status
            })

    return render_template('history.html', history=history)


@app.route('/get_data', methods=['GET'])
def get_data():

    data = mongo.db.exemplo.find()

    return jsonify({"message": "Consulta ao MongoDB bem-sucedida", "data": data})
