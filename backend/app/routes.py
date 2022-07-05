from re import error
from flask_migrate import current
from app import app, db, login, conn
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import *
from flask import jsonify, request
import time
import datetime
import sys
import os

db.drop_all()
db.create_all()


user = Staff(
    username='ravisrc',
    name="Sriram"
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()
user = Staff(
    username='vgokul',
    name="Gokul V"
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()

user = Patient(
    username='robert',
    name="Robert S"
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()

obj = Department(
    name="Ortho")
db.session.add(obj)
db.session.commit()
obj = Department(
    name="Dental")
db.session.add(obj)
db.session.commit()
obj = Department(
    name="Cardio")
db.session.add(obj)
db.session.commit()

obj = Disease(
    dep_id=1,
    name="Fractures"
)
db.session.add(obj)
db.session.commit()
obj = Disease(
    dep_id=1,
    name="Joint Pains"
)
db.session.add(obj)
db.session.commit()
obj = Disease(
    dep_id=2,
    name="Cavities"
)
db.session.add(obj)
db.session.commit()
obj = Disease(
    dep_id=2,
    name="Alignment Tooth"
)
db.session.add(obj)
db.session.commit()
obj = Disease(
    dep_id=3,
    name="Chest Pain"
)
db.session.add(obj)
db.session.commit()
obj = Disease(
    dep_id=3,
    name="Cardiac Arrest"
)
db.session.add(obj)
db.session.commit()


user = Doctor(
    username='rao',
    name='Dr. Rao',
    consultation_fee=300,
    dep_id=3
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()
user = Doctor(
    username='siraz',
    name='Dr. Siraz',
    consultation_fee=400,
    dep_id=1
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()
user = Doctor(
    username='varun',
    name='Dr. Varun',
    consultation_fee=500,
    dep_id=2
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()

obj = Medicine(
    name='Med 1',
    cost=100
)
db.session.add(obj)
db.session.commit()
obj = Medicine(
    name='Med 2',
    cost=200
)
db.session.add(obj)
db.session.commit()
obj = Medicine(
    name='Med 3',
    cost=300
)
db.session.add(obj)
db.session.commit()
obj = Medicine(
    name='Med 4',
    cost=400
)
db.session.add(obj)
db.session.commit()
obj = Medicine(
    name='Med 5',
    cost=500
)
db.session.add(obj)
db.session.commit()
obj = Medicine(
    name='Med 6',
    cost=600
)
db.session.add(obj)
db.session.commit()

obj = Treatment(
    name='Trtmt 1',
    cost=1000
)
db.session.add(obj)
db.session.commit()
obj = Treatment(
    name='Trtmt 2',
    cost=2000
)
db.session.add(obj)
db.session.commit()
obj = Treatment(
    name='Trtmt 3',
    cost=3000
)
db.session.add(obj)
db.session.commit()
obj = Treatment(
    name='Trtmt 4',
    cost=4000
)
db.session.add(obj)
db.session.commit()
obj = Treatment(
    name='Trtmt 5',
    cost=5000
)
db.session.add(obj)
db.session.commit()
obj = Treatment(
    name='Trtmt 6',
    cost=6000
)
db.session.add(obj)
db.session.commit()

# ------ API STARTS HERE ------
@app.route('/')
@app.route('/home')
def home():
    # return "Welcome to the API"
    try:
        for item in conn.execute("SELECT * FROM area_of_disease"):
            return item.disease_id
            # print(str(type(item)))
            return "No"
        return "No links"
    except:
        return sys.exc_info()


@app.route('/login', methods=['GET', 'POST'])
def login():
    # try:
        # get the data from the frontend
    user_data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    # check if user is already logged in

    if auth_token:
        curr_userid = User.decode_auth_token(auth_token)

        if not isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': 'User already logged in'
            }
            return jsonify(response), 403

        #    Fetch the user with the given user id
        # present_user = User.query.get(curr_userid)
        # if present_user is not None:
        #     response = {
        #         'status': 'invalid',
        #         'message': 'User already logged in'
        #     }
        #     return jsonify(response), 403

    # user = User.query.filter_by(username=user_data.get('username')).first()#query
    user = conn.execute(
        "SELECT * FROM users AS U WHERE U.username=%s",user_data.get('username')).first()

    if user is None:
        response = {'status': 'invalid', 'message': 'User does not exist'}
        return jsonify(response), 404

    if check_password_hash(user.hash_password, user_data.get('password')):
        token = User.encode_auth_token(user.id)

        if token:
            response = {
                'user_id': user.id,
                'username': user.username,
                'auth_token': token,
                'user_type': user.type,
                'message': 'User succesfully logged in.',
                'status': 'success'
            }
            if user.type == "patient":
                user = conn.execute(
                    "SELECT * FROM patient AS U WHERE U.patient_id=%s",user.id).first()
                profile = {
                    'name': user.name,
                    'gender': user.gender,
                    'date_of_birth': user.date_of_birth,
                    'mobile': user.mobile,
                }
                response['profile'] = profile
            elif user.type == "doctor":
                user = conn.execute(
                    "SELECT * FROM doctor AS U WHERE U.doctor_id=%s",user.id).first()
                profile = {
                    'name': user.name,
                    'qualification': user.qualification,
                    'room_no': user.room_no,
                    'mobile': user.mobile,
                    'present_status': user.present_status,
                    'consultation_fee': user.consultation_fee,
                    'dep_id': user.dep_id,
                }
                response['profile'] = profile
            elif user.type == "lab":
                user = conn.execute(
                    "SELECT * FROM lab AS U WHERE U.lab_id=%s",user.id).first()
                profile = {
                    'name': user.name
                }
                response['profile'] = profile
            elif user.type == "staff":
                user = conn.execute(
                    "SELECT * FROM staff AS U WHERE U.staff_id=%s",user.id).first()
                profile = {
                    'name': user.name
                }
                response['profile'] = profile
            return jsonify(response), 200

    else:
        response = {
            'status': 'fail',
            'message': 'Incorrect password entered'
        }
        return jsonify(response), 401

    # except:
    #     response = {
    #         'status': 'fail',
    #         'message': 'Unable to login, please try again',
    #     }
    #     return jsonify(response), 500


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403
        present_user = User.query.get(curr_userid)
        logout_user()
        response = {
            'status': 'success',
            'message': 'Succesfully logged out of the account'
        }
        return jsonify(response), 200
    else:
        response = {'status': 'invalid', 'message': 'User not logged in'}
        return jsonify(response), 401


@app.route('/getuserdetails', methods=['POST'])
def getuserdetails():
   # try:
    auth_token = (request.json)['auth_token']
    userid = User.decode_auth_token(auth_token)
    # return jsonify(userid), 500
    #    If the decode_auth_token is returning a non string object
    #    If it is a tring that measn token has expired or is invalid
    if not isinstance(userid, str):
        #    Fetch the user with the given user id
        user = conn.execute("SELECT * FROM users AS U WHERE U.id=%s", userid).first()
        if user is not None:
            #    User found
            response = {
                'user_id': user.id,
                'username': user.username,
                'user_type': user.type,
                'message': 'User succesfully logged in.',
                'status': 'success'
            }
            if user.type == "patient":
                user = conn.execute(
                    "SELECT * FROM patient AS U WHERE U.patient_id=%s",user.id).first()
                profile = {
                    'name': user.name,
                    'gender': user.gender,
                    'date_of_birth': user.date_of_birth,
                    'mobile': user.mobile,
                }
                response['profile'] = profile
            elif user.type == "doctor":
                user = conn.execute(
                    "SELECT * FROM doctor AS U WHERE U.doctor_id=%s",user.id).first()
                profile = {
                    'name': user.name,
                    'qualification': user.qualification,
                    'room_no': user.room_no,
                    'mobile': user.mobile,
                    'present_status': user.present_status,
                    'consultation_fee': user.consultation_fee,
                    'dep_id': user.dep_id,
                }
                response['profile'] = profile
            elif user.type == "lab":
                user = conn.execute(
                    "SELECT * FROM lab AS U WHERE U.lab_id=%s",user.id).first()
                profile = {
                    'name': user.name
                }
                response['profile'] = profile
            elif user.type == "staff":
                user = conn.execute(
                    "SELECT * FROM staff AS U WHERE U.staff_id=%s",user.id).first()
                profile = {
                    'name': user.name
                }
                response['profile'] = profile
            return jsonify(response), 200
        else:
            #    User not found with the id
            response_obj = {
                'message': "Invalid Token found.",
                'status': 'invalid'
            }
            return jsonify(response_obj), 401

    else:
        #    userid has got a string from decode_auth_token functions
        #    and hence some expiration status in token
        response_obj = {'message': userid, 'status': 'fail'}
    return jsonify(response_obj), 403
   # except:
   #      response_obj = {
   #          'status': 'fail',
   #          'message': 'Unable to access user details from the token',
   #          "error": sys.exc_info()
   #      }
   #      return jsonify(response_obj), 500

@app.route('/getallsessions', methods=['POST'])
def getallsessions():
    # try:
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        ''' write here'''
        all_sessions = []
        # conn.nextset()
        for item in conn.execute("SELECT * FROM session;"):
            patient_name = conn.execute("SELECT name FROM patient WHERE patient.patient_id = %s",item.patient_id).first()
            if patient_name is None:
                response = {"status": "Invalid", "message": "Patient not found for this session."}
                return jsonify(response), 402
            session = {
                'session_id' : item.session_id,
                'patient_id' : item.patient_id,
                'patient_name'   : patient_name[0],
                'session_start_time' : item.joining_date,
                'last_updated_time' : item.discharge_date,
                'billed_amount' : item.billed_amount,
                'description' : item.description
            }
            if item.discharge_date is None:
                session['active_or_not'] = True
            else:
                session['active_or_not'] = False
            all_sessions.append(session)

        return jsonify({"sessions": all_sessions}), 200


    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/getsessiondetails', methods=['POST'])
def getsessiondetails():
    # try:
    session_data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        ''' write here'''
        session = conn.execute("SELECT * FROM session WHERE session.session_id=%s",session_data.get('session_id')).first()

        if session is None:
            response = {
                'status': "Invalid",
                'message': "Session with session_id sent not exist"
            }
            return jsonify(response), 404

        sessions = {
            'session_id' : session.session_id,
            'patient_id' : session.patient_id,
            'patient_name'   : conn.execute("SELECT name FROM patient WHERE patient.patient_id = %s",session.patient_id).first()[0],
            'staff_name'   : conn.execute("SELECT name FROM staff WHERE staff.staff_id = %s",session.staff_id).first()[0],
            'session_start_time' : session.joining_date,
            'last_updated_time' : session.discharge_date,
            'description' : session.description,
            'billed_amount' : session.billed_amount,
            'area_of_disease': [],
            'appointments' : []
        }

        for item in conn.execute("SELECT d.name FROM session_disease AS sd ,area_of_disease AS d WHERE sd.session_id = %s AND sd.disease_id=d.disease_id",session.session_id):
            sessions['area_of_disease'].append(item.name)


        for item1 in conn.execute("SELECT * FROM appointment WHERE appointment.session_id=%s",session.session_id):
            appointment = {
                'appointment_time' : item1.app_time,
                'doctor_name' : conn.execute("SELECT name FROM doctor WHERE doctor.doctor_id = %s",item1.doctor_id).first()[0],
                'appointment_id' : item1.app_id,
                'description' : item1.doctor_description,
            }
            if session.discharge_date is None:
                appointment['active_or_not'] = True
            else:
                appointment['active_or_not'] = False
            sessions['appointments'].append(appointment)

        if session.billed_amount is not None:
            sessions['bill_generation_status'] = True
        else:
            sessions['bill_generation_status'] = False

        return jsonify({"session_details":sessions}), 200


    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500


@app.route('/getareaofdiseases', methods=['POST'])
def getareaofdisease():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403


            ''' write here'''
            all_disease=[]

            for item in conn.execute("SELECT * FROM area_of_disease"):
                disease={
                    'disease_id'   : item.disease_id,
                    'disease_name' : item.name
                }
                all_disease.append(disease)
            all_disease = {"area_of_diseases": all_disease}
            return jsonify(all_disease)


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500


@app.route('/getmysessions',methods=['POST'])
def getmysessions():
     try:
        patient_data = request.json
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403

            user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

            if  user_type == "staff" or user_data == "doctor" or (user_data == "patient" and curr_userid == patient_data.get('patient_id')):
                ''' write here'''
                all_sessions=[]
                sql = "SELECT * FROM session WHERE session.patient_id=%s"
                for item in conn.execute(sql,patient_data.patient_data.get('patient_id')):
                    sql1 = "SELECT name FROM patient WHERE patient.patient_id = %s"
                    sql2 = "SELECT description FROM session_disease WHERE sd.session_id = %s"
                    session = {
                        'session_id' : item.session_id,
                        'patient_id' : item.patient_id,
                        'patient_name'   : conn.execute(sql1,item.patient_id).first(),
                        'session_start_time' : item.joining_date,
                        'last_updated_time' : item.discharge_date,
                        'description' : conn.execute(sql2,item.session_id).first()
                    }
                    if item.discharge_date is None:
                        session['active_or_not'] = True
                    else:
                        session['active_or_not'] = False
                    all_sessions.append(session)

                return jsonify(all_sessions), 200

        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

     except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
     return jsonify(response), 500

@app.route('/getmyappointedsessions',methods=['POST'])
def getmyappointedsessions():
     try:
        doctor_data = request.json
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403
            user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

            if  user_type == "staff" or user_data == "doctor":
                ''' write here'''
                all_sessions=[]
                sql = "SELECT * FROM session WHERE session.doctor_id=%s"
                for item in conn.execute(sql,patient_data.doctor_data.get('doctor_id')):
                    sql1 = "SELECT name FROM patient WHERE patient.doctor_id = %s"
                    sql2 = "SELECT description FROM session_disease WHERE sd.session_id = %s"
                    session = {
                        'session_id' : item.session_id,
                        'patient_id' : item.patient_id,
                        'patient_name'   : conn.execute(sql1,item.patient_id).first(),
                        'session_start_time' : item.joining_date,
                        'last_updated_time' : item.discharge_date,
                        'description' : item.description
                    }
                    if item.discharge_date is None:
                        session['active_or_not'] = True
                    else:
                        session['active_or_not'] = False
                    all_sessions.append(session)

                return jsonify(all_sessions), 200

        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

     except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
     return jsonify(response), 500

@app.route('/getrelateddoctors',methods=['POST'])
def getrelateddoctors():
    # try:
    disease_data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403


        ''' write here'''
        disease_ids = disease_data.get('disease_ids')

        all_doctors=[]
        all_doc_ids=[]

        for each_id in disease_ids:
            sql = "SELECT doc.doctor_id FROM doctor AS doc,area_of_disease AS disease WHERE disease.dep_id = %s AND doc.dep_id = disease.dep_id"
            for item in conn.execute(sql,each_id):
                if item not in all_doc_ids:
                    all_doc_ids.append(item)

        for ids in all_doc_ids:
            sql = "SELECT * from doctor WHERE doctor.doctor_id = %s"
            sql1 = "SELECT name from department WHERE dep_id = %s"
            sql2 = "SELECT  DATEDIFF(joining_date, NOW()) FROM doctor WHERE doctor_id=%s"
            doctors = conn.execute(sql,ids).first()
            # experience = conn.execute(sql2,doctors.doctor_id)
            related_doctor={
                'doctor_id' : doctors.doctor_id,
                'doctor_name' : doctors.name,
                'department' : conn.execute(sql1,doctors.dep_id).first()[0],
                'experience' : conn.execute(sql2,doctors.doctor_id).first()[0],
                'room_no' : doctors.room_no,
                'appointment_fee' : doctors.consultation_fee,
                'specialisation' : []
            }
            all_doctors.append(related_doctor)

        return jsonify({"related_doctors" : all_doctors}), 200

    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500


@app.route('/createsession',methods=['POST'])
def createsession():
    # try:
    session_data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403


        if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0] == "staff":
            if session_data.get('patient_username') == "":
                patient_id = conn.execute("SELECT id FROM users WHERE users.username=%s",session_data.get('patient_newusername')).first()
                if patient_id is not None:
                    response = {
                        'status': 'Not possible',
                        'message': 'User already exists'
                    }
                    return jsonify(response), 500
                else:
                    # user creation
                    conn.execute("INSERT INTO users (username,hash_password,type) values (%s,%s,%s)",(session_data.get('patient_newusername'),generate_password_hash(session_data.get('patient_newusername') + "123"),'patient'))
                    patient_id_new = conn.execute("SELECT * from users WHERE users.username = %s",session_data.get('patient_newusername')).first()[0]
                    # patient creation
                    data = (patient_id_new,session_data.get('patient_newname'),session_data.get('patient_dob'),session_data.get('patient_gender'),session_data.get('patient_mobile'))
                    conn.execute("INSERT INTO patient (patient_id,name,date_of_birth,gender,mobile) values (%s,%s,%s,%s,%s)",data)
                    staff_id = session_data.get('staff_id')
                    description = session_data.get('description')
                    joining_date = datetime.datetime.now()
                    # session creation
                    data = (staff_id,patient_id_new,description,joining_date)
                    conn.execute("INSERT INTO session (staff_id,patient_id,description,joining_date) values (%s,%s,%s,%s)",data)
                    session_id = conn.execute("SELECT LAST_INSERT_ID();").first()[0]
                    for ids in session_data.get('disease_ids'):
                        conn.execute("INSERT INTO session_disease (session_id,disease_id) values (%s,%s)",session_id,ids)
                    conn.execute("INSERT INTO appointment (session_id,doctor_id,app_time,doctor_description) values (%s,%s,%s,%s)",(session_id,session_data.get('primary_doctor_id'),datetime.datetime.now()," "))
                    response = {
                        'status': 'success',
                        'message': 'created a new session'
                    }
                    return jsonify(response), 200

            else:
                patient_id = conn.execute("SELECT patient_id FROM patient JOIN users ON patient.patient_id=users.id WHERE users.username=%s",session_data.get('patient_username')).first()[0]
                staff_id = session_data.get('staff_id')
                description = session_data.get('description')
                joining_date = datetime.datetime.now()
                data = (staff_id,patient_id,description,joining_date)
                conn.execute("INSERT INTO session (staff_id,patient_id,description,joining_date) values (%s,%s,%s,%s)",data)
                # session_id = conn.execute("SELECT session_id FROM session AS s WHERE s.patient_id=%s AND s.staff_id = %s",patient_id,staff_id).first()[0]
                session_id = conn.execute("SELECT LAST_INSERT_ID();").first()[0]
                for ids in session_data.get('disease_ids'):
                    conn.execute("INSERT INTO session_disease (session_id,disease_id) values (%s,%s)",(session_id,ids))
                conn.execute("INSERT INTO appointment (session_id,doctor_id,app_time,doctor_description) values (%s,%s,%s,%s)",(session_id,session_data.get('primary_doctor_id'),datetime.datetime.now()," "))
                response = {
                    'status': 'success',
                    'message': 'created a new session'
                }
                return jsonify(response), 200
        else:
            response = {"status": "No permission", "message": "User not Staff"}
            return jsonify(response), 401    
        

    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/getalltreatment', methods=['POST'])
def getalltreatment():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403


            ''' write here'''
            all_treatment=[]

            for item in conn.execute("SELECT * FROM treatment;"):
                treatment={
                    'treatment_id'   : item.trmrt_id,
                    'treatment_name' : item.name
                }
                all_treatment.append(treatment)

            return jsonify({"all_treatments" : all_treatment}), 200


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

@app.route('/getallmedicine', methods=['POST'])
def getallmedicine():
    # try:
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403


        ''' write here'''
        all_medicine=[]

        for item in conn.execute("SELECT * FROM medicine;"):
            medicine={
                'medicine_id'   : item.medicine_id,
                'medicine_name' : item.name
            }
            all_medicine.append(medicine)

        return jsonify({"all_medicines": all_medicine}), 200


    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/getalltesttype', methods=['POST'])
def getalltesttype():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403


            ''' write here'''
            all_test_type=[]

            for item in conn.execute("SELECT * FROM test_type"):
                test_type={
                    'test_type_id'   : item.test_type_id,
                    'test_type_name' : item.name
                }
                all_test_type.append(test_type)

            return jsonify(all_test_type)


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

@app.route('/getalldoctors',methods=['POST'])
def getalldoctors():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403


        ''' write here'''
        all_doctors=[]

        for item in conn.execute("SELECT * from doctor;"):
            doctor={
                'doctor_id' : item.doctor_id,
                'doctor_name' : item.name,
                'department' : conn.execute("SELECT name from department WHERE dep_id = %s",item.dep_id).first()[0],
                'room_no' : item.room_no,
                'appointment_fee' : item.consultation_fee,
                'specialisation' : []
            }
            sql = "SELECT s.name FROM specialisation AS s,doctor_specialisation AS ds WHERE ds.doctor_id = %s AND s.spec_id = ds.spec_id"
            for item1 in conn.execute(sql,item.doctor_id):
                doctor['specialisation'].append(item1.name)
            all_doctors.append(doctor)

        return jsonify({"all_doctors" : all_doctors}), 200

    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/addtreatment',methods=['POST'])
def addtreatment():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403


        ''' write here'''
        if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0] == "doctor":
            conn.execute("INSERT INTO appointment_treatment (app_id,trmrt_id,trmrt_time) values (%s,%s,%s)",(data.get('app_id'),data.get('trmrt_id'),datetime.datetime.now()))

            response = {"status": "success", "message": "added a new treatment"}
            return jsonify(response), 200
            
        else:
            response = {"status": "Permission Denied", "message": "User not Doctor"}
            return jsonify(response), 401 

        


    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/getappointmentdetails', methods=['POST'])
def getappointmentdetails():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        ''' write here'''
        appointment = conn.execute("SELECT * FROM appointment WHERE appointment.app_id=%s",data.get('app_id')).first()
        patient = conn.execute("SELECT * FROM patient NATURAL JOIN session WHERE session.session_id = %s",appointment.session_id).first()
        if appointment is None:
            response = {
                'status': "Invalid",
                'message': "appointment with app_id sent not exist"
            }
            return jsonify(response), 404

        appointment_details = {
            'app_id' : appointment.app_id,
            'appointment_time'   : appointment.app_time,
            'doctor_name'   : conn.execute("SELECT name FROM doctor WHERE doctor.doctor_id = %s",appointment.doctor_id).first()[0],
            'patient_id' : patient.patient_id,
            'patient_name' : patient.name,
            'session_id' : appointment.session_id,
            'doctor_description' : appointment.doctor_description,
            'treatments': [],
            'medicines' : []
        }

        for item in conn.execute("SELECT * FROM appointment_treatment AS at ,treatment AS t WHERE at.app_id = %s AND t.trmrt_id=at.trmrt_id",appointment.app_id):
            appointment_details['treatments'].append({"trmrt_name": item.name, "trmrt_time": item.trmrt_time})

        for item in conn.execute("SELECT * FROM appointment_medicine AS at ,medicine AS t WHERE at.app_id = %s AND t.medicine_id=at.medicine_id",appointment.app_id):
            appointment_details['medicines'].append({"trmrt_name": item.name, "quantity": item.quantity})

        return jsonify({"appointment_details" : appointment_details})

    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/addmedicine',methods=['POST'])
def addmedicine():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403


        ''' write here'''
        if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0] == "doctor":
            conn.execute("INSERT INTO appointment_medicine (app_id,medicine_id,quantity) values (%s,%s, %s)",(data.get('app_id'),data.get('medicine_id'),data.get('quantity')))

            response = {"status": "success", "message": "added a new medicine"}
            return jsonify(response), 200
            
        else:
            response = {"status": "Permission Denied", "message": "User not Doctor"}
            return jsonify(response), 401 
    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/addappointment',methods=['POST'])
def addappointment():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

        ''' write here'''
        if  user_type == "staff" or user_type == "doctor":
            conn.execute("INSERT INTO appointment (session_id,doctor_id,app_time,doctor_description) values (%s,%s,%s,%s)",(data.get('session_id'),data.get('doctor_id'),datetime.datetime.now()," "))

            response = {"status": "success", "message": "added a new appointment"}
            return jsonify(response), 200
            
        else:
            response = {"status": "Permission Denied", "message": "User neither Doctor nor Staff"}
            return jsonify(response), 401 
    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/editdescription',methods=['POST'])
def editdescription():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

        ''' write here'''
        if  user_type == "doctor":
            conn.execute("UPDATE appointment SET doctor_description = %s WHERE app_id = %s",data.get('description'),data.get('app_id'))

            response = {"status": "success", "message": "added description"}
            return jsonify(response), 200
            
        else:
            response = {"status": "Permission Denied", "message": "User neither Doctor nor Staff"}
            return jsonify(response), 402 
    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500


@app.route('/marksessioncomplete',methods=['POST'])
def marksessioncomplete():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403

            user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

            ''' write here'''
            if  user_type == "staff":

                response = {"status": "success", "message": "added discharge_date"}
                return jsonify(response), 200
                
            else:
                response = {"status": "Permission Denied", "message": "User not Staff"}
                return jsonify(response), 402 
        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

@app.route('/marksessionpaid',methods=['POST'])
def marksessionpaid():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

        ''' write here'''
        if  user_type == "staff":
            conn.execute("UPDATE session SET bill_payment_status = %s WHERE session_id = %s",True,data.get('session_id'))
            conn.execute("UPDATE session SET discharge_date = %s WHERE session_id = %s",datetime.datetime.now(),data.get('session_id'))
            response = {"status": "success", "message": "updated bill_payment_status"}
            return jsonify(response), 200
            
        else:
            response = {"status": "Permission Denied", "message": "User not Staff"}
            return jsonify(response), 402 
    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/generatebill',methods=['POST'])
def generatebill():
    # try:
    data = request.json
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        # if True:
        curr_userid = User.decode_auth_token(auth_token)
        if isinstance(curr_userid, str):
            response = {
                'status': 'invalid',
                'message': curr_userid
            }
            return jsonify(response), 403

        user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()[0]

        ''' write here'''
        if  user_type == "staff":
            consultation_amount = conn.execute("SELECT SUM(consultation_fee),session_id FROM doctor as d,appointment as a WHERE a.session_id=%s AND d.doctor_id=a.doctor_id",data.get('session_id')).first()[0]
            treatment_amount = conn.execute("SELECT SUM(cost),session_id FROM treatment as t,appointment_treatment as at,appointment as a WHERE a.session_id=%s AND at.app_id=a.app_id AND t.trmrt_id=at.trmrt_id GROUP BY session_id",data.get('session_id')).first()[0]
            medicine_amount = conn.execute("SELECT SUM(cost*quantity),session_id FROM medicine as t,appointment_medicine as at,appointment as a WHERE a.session_id=%s AND at.app_id=a.app_id AND t.medicine_id=at.medicine_id GROUP BY session_id",data.get('session_id')).first()[0]
            total_amount = 0
            if consultation_amount is not None:
                total_amount = total_amount + consultation_amount
            if treatment_amount is not None:
                total_amount = total_amount + treatment_amount
            if medicine_amount is not None:
                total_amount = total_amount + medicine_amount
            conn.execute("UPDATE session SET billed_amount = %s WHERE session_id = %s",total_amount,data.get('session_id'))

            response = {"status": "success", "message": "updated bill amount"}
            return jsonify(response), 200
            
        else:
            response = {"status": "Permission Denied", "message": "User neither Staff"}
            return jsonify(response), 402 
    else:
        response = {"status": "Invalid", "message": "User not logged in"}
        return jsonify(response), 401

    # except:
    #     response = {
    #         "status": "Fail",
    #         "message": "Error in accessing the database"
    #     }
    # return jsonify(response), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        data = request.json
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            # if True:
            curr_userid = User.decode_auth_token(auth_token)
            if isinstance(curr_userid, str):
                response = {
                    'status': 'invalid',
                    'message': curr_userid
                }
                return jsonify(response), 403

            user = conn.execute("SELECT * FROM users WHERE users.id = %s",curr_userid).first()

            if user.type == "staff" and user.username == "admin":
                ids = conn.execute("SELECT id FROM users WHERE users.username=%s",data.get('username')).first()[0]
                if ids is not None:
                    response = {
                        'status': 'Not possible',
                        'message': 'User already exists'
                    }
                    return jsonify(response), 500
                else:
                    conn.execute("INSERT INTO users (username,hash_password,type) values (%s,%s,%s)",(data.get('username'),generate_password_hash(data.get('password')),data.get('type')))
                    id_new = conn.execute("SELECT id FROM users WHERE users.username=%s",data.get('username')).first()[0]
                    if data.get('type') == "patient":
                        data = (id_new,data.get('patient_newname'),data.get('patient_dob'),data.get('patient_gender'),data.get('patient_mobile'))
                        conn.execute("INSERT INTO patient (patient_id,name,date_of_birth,gender,mobile) values (%s,%s,%s,%s,%s)",data)
                    elif data.get('type') == "doctor":
                        data = (id_new,data.get('doctor_name'),data.get('qualification'),data.get('room_no'),data.get('doctor_mobile'),data.get('consultation_fee'),data.get('dep_id'))
                        conn.execute("INSERT INTO doctor (doctor_id,name,qualification,room_no,mobile,consultation_fee,dep_id) values (%s,%s,%s,%s,%s,%s,%s)",data)
                    elif data.get('type') == "staff":
                        data = (id_new,data.get('doctor_name'))
                        conn.execute("INSERT INTO staff (staff_id,name) values (%s,%s)",data)
                    elif data.get('type') == "lab":
                        data = (id_new,data.get('lab_name'))
                        conn.execute("INSERT INTO staff (lab_id,name) values (%s,%s)",data)
                    response = {
                        'status': 'success',
                        'message': 'created a new user'
                    }
                    return jsonify(response), 200
                
            else:
                response = {
                    'status': 'Permission denied',
                    'message': 'cannot register new user'
                }
                return jsonify(response), 403
        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500







