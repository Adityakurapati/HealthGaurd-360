import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate('credentials/firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://healthgaurd360-426f4-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Reference the root of the database
ref = db.reference('/')

# Sample data
doctors_data = [
    {"name": "Dr. John Doe", "specialization": "Cardiologist", "contact": "1234567890", "hospital_id": "hosp1"},
    {"name": "Dr. Jane Smith", "specialization": "Dermatologist", "contact": "0987654321", "hospital_id": "hosp2"}
]

appointments_data = [
    {"patient_name": "Alice", "doctor_id": "doc1", "appointment_date": "2024-08-15", "status": "Confirmed"},
    {"patient_name": "Bob", "doctor_id": "doc2", "appointment_date": "2024-08-16", "status": "Pending"}
]

hospitals_data = [
    {"name": "City Hospital", "location": "Downtown", "contact": "1122334455"},
    {"name": "Green Valley Clinic", "location": "Uptown", "contact": "2233445566"}
]

news_data = [
    {
        "title": "New COVID-19 Vaccine Shows Promise",
        "content": "A new vaccine candidate has shown 95% efficacy in phase 3 trials...",
        "date": "2024-08-14",
        "category": "Research"
    },
    {
        "title": "Health Ministry Announces New Wellness Program",
        "content": "The Ministry of Health has launched a nationwide wellness initiative...",
        "date": "2024-08-13",
        "category": "Public Health"
    }
]

# New: Sample diseases data
diseases_data = [
    {"name": "Asthma", "description": "A condition in which your airways narrow and swell."},
    {"name": "Bronchitis", "description": "Inflammation of the lining of bronchial tubes."},
    {"name": "Cholera", "description": "A bacterial disease causing severe diarrhea and dehydration."},
    {"name": "Diabetes", "description": "A group of diseases that result in too much sugar in the blood."},
    {"name": "Ebola", "description": "A rare and deadly disease caused by infection with a virus."}
]

# Adding sample doctors data
doctors_ref = ref.child('doctors')
for doctor in doctors_data:
    new_doctor_ref = doctors_ref.push(doctor)
    print(f"Added doctor with ID: {new_doctor_ref.key}")

# Adding sample appointments data
appointments_ref = ref.child('appointments')
for appointment in appointments_data:
    new_appointment_ref = appointments_ref.push(appointment)
    print(f"Added appointment with ID: {new_appointment_ref.key}")

# Adding sample hospitals data
hospitals_ref = ref.child('hospitals')
for hospital in hospitals_data:
    new_hospital_ref = hospitals_ref.push(hospital)
    print(f"Added hospital with ID: {new_hospital_ref.key}")

# Adding sample news data
news_ref = ref.child('news')
for news_item in news_data:
    new_news_ref = news_ref.push(news_item)
    print(f"Added news item with ID: {new_news_ref.key}")

# New: Adding sample diseases data
diseases_ref = ref.child('diseases')
for disease in diseases_data:
    new_disease_ref = diseases_ref.push(disease)
    print(f"Added disease with ID: {new_disease_ref.key}")
