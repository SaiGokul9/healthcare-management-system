from re import error
from flask_migrate import current
from app import app, db, login, conn
from flask_login import current_user, login_user, logout_user
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
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()
user = Patient(
    username='robert',
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()
user = Doctor(
    username='rao',
)
user.set_password('passwd1')
db.session.add(user)
db.session.commit()


# ------ API STARTS HERE ------
@app.route('/')
@app.route('/home')
def home():
    # return "Welcome to the API"
    try:
        for item in conn.execute("SELECT * FROM area_of_disease"):
            return str(item.disease_id)
            print(str(type(item)))
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
        for item in conn.execute("SELECT * FROM session"):
            session = {
                'session_id' : str(item.session_id),
                'patient_id' : str(item.patient_id),
                'patient_name'   : str(conn.execute("SELECT name FROM patient WHERE patient.patient_id = %s",item.patient_id).first()),
                'session_start_time' : str(item.joining_date),
                'last_updated_time' : str(item.discharge_date),
                'description' : str(conn.execute("SELECT description FROM session_disesase WHERE sd.session_id = %s",item.session_id).first())
            }
            if item.discharge_date is None:
                session['active_or_not'] = True
            else:
                session['active_or_not'] = False
            all_sessions.append(session)

        return jsonify(all_sessions)


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
    try:
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
                'session_id' : str(session.session_id),
                'patient_id' : str(session.patient_id),
                'patient_name'   : str(conn.execute("SELECT name FROM patient WHERE patient.patient_id = %s",session.patient_id).first()),
                'session_start_time' : str(sessiom.joining_date),
                'last_updated_time' : str(session.discharge_date),
                'description' : str(session.description),
                'area_of_disease': [],
                'appointments' : []
            }

            for item in conn.execute("SELECT d.name FROM session_disesase AS sd ,disease AS d WHERE sd.session_id = %s AND sd.disease_id=d.disease_id",session.session_id):
                sessions['area_of_disease'].append(item)


            for item in conn.execute("SELECT * FROM appointment WHERE appointment.session_id=%s",session.session_id):
                appointment = {
                    'appointment_time' : str(item.time),
                    'doctor_name' : str(conn.execute("SELECT name FROM doctor WHERE doctor.doctor_id = %s",item.doctor_id).first()),
                    'appointment_id' : str(item.appointment_id),
                    'description' : str(item.doctor_description),
                }
                if item.description is None:
                    appointment['active_or_not'] = True
                else:
                    appointment['active_or_not'] = False
                sessions['appointment'].apppend(appointment)

            if item.billed_amount is not None:
                sessions['bill_generation_status'] = True
            else:
                sessions['bill_generation_status'] = False

            return jsonify(sessions)


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500


@app.route('/getareaofdisease', methods=['POST'])
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
                    'disease_id'   : str(item.disease_id),
                    'disease_name' : str(item.name)
                }
                all_disease.append(disease)

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

            user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()

            if  user_type == "staff" or user_data == "doctor" or (user_data == "patient" and curr_userid == patient_data.get('patient_id')):
                ''' write here'''
                all_sessions=[]
                sql = "SELECT * FROM session WHERE session.patient_id=%s"
                for item in conn.execute(sql,patient_data.patient_data.get('patient_id')):
                    sql1 = "SELECT name FROM patient WHERE patient.patient_id = %s"
                    sql2 = "SELECT description FROM session_disesase WHERE sd.session_id = %s"
                    session = {
                        'session_id' : str(item.session_id),
                        'patient_id' : str(item.patient_id),
                        'patient_name'   : str(conn.execute(sql1,item.patient_id).first()),
                        'session_start_time' : str(item.joining_date),
                        'last_updated_time' : str(item.discharge_date),
                        'description' : str(conn.execute(sql2,item.session_id).first())
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
            user_type = conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first()

            if  user_type == "staff" or user_data == "doctor":
                ''' write here'''
                all_sessions=[]
                sql = "SELECT * FROM session WHERE session.doctor_id=%s"
                for item in conn.execute(sql,patient_data.doctor_data.get('doctor_id')):
                    sql1 = "SELECT name FROM patient WHERE patient.doctor_id = %s"
                    sql2 = "SELECT description FROM session_disesase WHERE sd.session_id = %s"
                    session = {
                        'session_id' : str(item.session_id),
                        'patient_id' : str(item.patient_id),
                        'patient_name'   : str(conn.execute(sql1,item.patient_id).first()),
                        'session_start_time' : str(item.joining_date),
                        'last_updated_time' : str(item.discharge_date),
                        'description' : str(conn.execute(sql2,item.session_id).first())
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
    try:
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
                sql = "SELECT doc.id FROM doctor AS doc,area_of_disease AS disease WHERE disease.dep_id = %s AND doc.dep_id = disease.dep_id"
                for item in conn.execute(sql,each_id):
                    if item not in all_doc_ids:
                        all_doc_ids.append(item)

            for ids in doc_id:
                sql = "SELECT * from doctor WHERE doctor.doctor_id = %s"
                sql1 = "SELECT name from department WHERE dep_id = %s"
                sql2 = "SELECT  DATEDIFF(year, joining_date, GETDATE()) FROM doctor WHERE doctor_id=%s"
                doctors = conn.execute(sql,ids)
                # experience = conn.execute(sql2,doctors.doctor_id)
                related_doctor={
                    'doctor_id' : doctors.doctor_id,
                    'doctor_name' : str(doctors.name),
                    'department' : str(conn.execute(sql1,doctors.dep_id).first()),
                    'experience' : conn.execute(sql2,doctors.doctor_id).first(),
                    'room_no' : str(doctors.room_no),
                    'appointment_fee' : doctors.consultation_fee,
                    'specialisation' : []
                }
                all_doctors.append(related_doctor)

            return jsonify(all_doctors), 200

        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500


@app.route('/createsession',methods=['POST'])
def createsession():
    try:
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


            if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first() == "staff":
                if session_data.get('patient_username') is None:
                    patient_id = conn.execute("SELECT patient_id FROM patient WHERE patient.username=%s",session_data.get('patient_newusername')).first()
                    if patient_id is not None:
                        response = {
                            'status': 'Not possible',
                            'message': 'User already exists'
                        }
                        return jsonify(response), 500
                    else:
                        data = (session_data.get('patient_newusername'),session_data.get('patient_newname'),session_data.get('patient_dob'),session_data.get('patient_gender'),session_data.get('patient_mobile'))
                        conn.execute("INSERT INTO patient (username,name,dob,gender,mobile) values (%s,%s,%s,%s,%s)",data)
                        patient_id = conn.execute("SELECT patient_id FROM patient WHERE patient.username=%s",session_data.get('patient_newusername')).first()
                        staff_id = session_data.get('staff_id')
                        description = session_data.get('description')
                        joining_date = datetime.now()
                        data = (staff_id,patient_id,description,joining_date)
                        conn.execute("INSERT INTO session (staff_id,patient_id,description,joining_date) values (%s,%s,%s,%s)",data)
                        session_id = conn.execute("SELECT session_id FROM session AS s WHERE s.patient_id=%s AND s.staff_id = %s",patient_id,staff_id)
                        for ids in session_data,get('disease_ids'):
                            conn.execute("INSERT INTO session_disesase (session_id,disease_id) values (%s,%s)",session_id,ids)

                else:
                    patient_id = conn.execute("SELECT patient_id FROM patient WHERE patient.username=%s",session_data.get('patient_username')).first()
                    staff_id = session_data.get('staff_id')
                    description = session_data.get('description')
                    joining_date = datetime.now()
                    data = (staff_id,patient_id,description,joining_date)
                    conn.execute("INSERT INTO session (staff_id,patient_id,description,joining_date) values (%s,%s,%s,%s)",data)
                    session_id = conn.execute("SELECT session_id FROM session AS s WHERE s.patient_id=%s AND s.staff_id = %s",patient_id,staff_id)
                    for ids in session_data,get('disease_ids'):
                        conn.execute("INSERT INTO session_disesase (session_id,disease_id) values (%s,%s)",session_id,ids)
            else:
                response = {"status": "No permission", "message": "User not Staff"}
                return jsonify(response), 401    
            

        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

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

            for item in conn.execute("SELECT * FROM treatment"):
                treatment={
                    'treatment_id'   : str(item.trmrt_id),
                    'treatment_name' : str(item.name)
                }
                all_treatment.append(treatment)

            return jsonify(all_treatment)


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
            all_medicine=[]

            for item in conn.execute("SELECT * FROM treatment"):
                disease={
                    'medicine_id'   : str(item.medicine_id),
                    'medicine_name' : str(item.name)
                }
                all_medicine.append(medicine)

            return jsonify(all_medicine)


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

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
                    'test_type_id'   : str(item.test_type_id),
                    'test_type_name' : str(item.name)
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

@app.route('/addtreatment',methods=['POST'])
def addtreatment():
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


            ''' write here'''
            if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first() == "doctor":
                conn.execute("INSERT INTO appointment_treatment (app_id,trmrt_id,trmrt_time) values (%s,%s)",(data.get('app_id'),data.get('trmrt_id'),datetime.now()))
                
            else:
                response = {"status": "Permission Denied", "message": "User not Doctor"}
                return jsonify(response), 401 

            


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

@app.route('/addmedicine',methods=['POST'])
def addmedicine():
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


            ''' write here'''
            if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first() == "doctor":
                conn.execute("INSERT INTO appointment_medicine (app_id,medicine_id,quantity) values (%s,%s)",(data.get('app_id'),data.get('medicine_id'),data.get('quantity')))
                
            else:
                response = {"status": "Permission Denied", "message": "User not Doctor"}
                return jsonify(response), 401 
        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500

# @app.route('/addtest',methods=['POST'])
# def addtest():
#     try:
#         data = request.json
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             auth_token = auth_header.split(" ")[1]
#         else:
#             auth_token = ''

#         if auth_token:
#             # if True:
#             curr_userid = User.decode_auth_token(auth_token)
#             if isinstance(curr_userid, str):
#                 response = {
#                     'status': 'invalid',
#                     'message': curr_userid
#                 }
#                 return jsonify(response), 403


#             ''' write here'''
#             if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first() == "doctor":
#                 conn.execute("INSERT INTO test (app_id,medicine_id,quantity) values (%s,%s)",(data.get('app_id'),data.get('medicine_id'),data.get('quantity')))
                
#             else:
#                 response = {"status": "Permission Denied", "message": "User not Doctor"}
#                 return jsonify(response), 401 
#         else:
#             response = {"status": "Invalid", "message": "User not logged in"}
#             return jsonify(response), 401

#     except:
#         response = {
#             "status": "Fail",
#             "message": "Error in accessing the database"
#         }
#     return jsonify(response), 500

@app.route('/addappointement',methods=['POST'])
def addappointment():
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


            ''' write here'''
            if conn.execute("SELECT users.type FROM users WHERE users.id = %s",curr_userid).first() == "staff":
                conn.execute("INSERT INTO appointment (session_id,doctor_id,app_time) values (%s,%s,%s)",(data.get('session_id'),data.get('doctor_id'),datetime.now()))
                
            else:
                response = {"status": "Permission Denied", "message": "User not Doctor"}
                return jsonify(response), 401 

            


        else:
            response = {"status": "Invalid", "message": "User not logged in"}
            return jsonify(response), 401

    except:
        response = {
            "status": "Fail",
            "message": "Error in accessing the database"
        }
    return jsonify(response), 500
