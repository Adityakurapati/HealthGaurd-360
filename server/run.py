import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

# Initialize Firebase
cred = credentials.Certificate('credentials/firebase-credentials.json')

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://healthgaurd360-426f4-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

app = Flask(__name__, static_folder="../client/build")
CORS(app)  # This enables CORS for all routes

# Reference the root of the database
ref = db.reference('/')

# Helper function to add no-cache headers
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Route to serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Route for nearby hospitals
@app.route('/api/nearby_hospitals', methods=['GET'])
def get_nearby_hospitals():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        hospitals_ref = ref.child('hospitals')
        hospitals = hospitals_ref.order_by_child('lat').start_at(lat - 0.05).end_at(lat + 0.05).get()
        
        if hospitals:
            return add_no_cache_headers(jsonify(list(hospitals.values())))
        else:
            return add_no_cache_headers(jsonify([]))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add hospitals data
@app.route('/api/add-hospitals', methods=['POST'])
def add_hospitals():
    try:
        hospitals_data = request.json.get('hospitals')
        hospitals_ref = ref.child('hospitals')
        for hospital in hospitals_data:
            hospitals_ref.push(hospital)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/diseases/<letter>', methods=['GET'])
def get_diseases_by_letter(letter):
    try:
        diseases_ref = ref.child('diseases')
        diseases = diseases_ref.order_by_child('name').start_at(letter).end_at(letter + "\uf8ff").get()
        diseases_list = [disease for disease in diseases.values()] if diseases else []
        return add_no_cache_headers(jsonify(diseases_list))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for doctors (includes doctor IDs)
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        doctors_ref = ref.child('doctors')
        doctors = doctors_ref.get()
        doctors_list = []
        if doctors:
            for doc_id, doc_data in doctors.items():
                doc_data['id'] = doc_id
                doctors_list.append(doc_data)
        return jsonify(doctors_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for news
@app.route('/api/news', methods=['GET'])
def get_news():
    try:
        news_ref = ref.child('news')
        news = news_ref.get()
        return add_no_cache_headers(jsonify(list(news.values()) if news else []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add doctor data
@app.route('/api/add-doctor', methods=['POST'])
def add_doctor():
    try:
        doctor_data = request.json
        doctors_ref = ref.child('doctors')
        new_doctor_ref = doctors_ref.push(doctor_data)
        return jsonify({"success": True, "id": new_doctor_ref.key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to add appointment data
@app.route('/api/add-appointment', methods=['POST'])
def add_appointment():
    try:
        appointment_data = request.json
        appointments_ref = ref.child('appointments')
        
        # Validate that the doctor exists
        doctors_ref = ref.child('doctors')
        if not doctors_ref.child(appointment_data['doctor_id']).get():
            return jsonify({"error": "Doctor not found"}), 400
        
        new_appointment_ref = appointments_ref.push(appointment_data)
        return jsonify({"success": True, "id": new_appointment_ref.key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to store sensor data
@app.route('/api/sensor_data', methods=['GET'])
def store_sensor_data():
    try:
        heartrate = request.args.get('heartrate')
        blood_oxygen = request.args.get('blood_oxygen')

        sensor_data = {
            'heartrate': heartrate,
            'blood_oxygen': blood_oxygen
        }

        ref.child('sensor_data').set(sensor_data)

        return jsonify({"success": True, "sensor_data": sensor_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
            # Change the port to 5000 explicitly
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)