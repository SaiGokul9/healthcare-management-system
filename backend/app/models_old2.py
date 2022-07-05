from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login, app
from flask_login import UserMixin
import jwt
import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # email = db.Column(db.String(128), unique=True)
    hash_password = db.Column(db.String(128))
    # description = db.Column(db.Text)

    type = db.Column(db.String(64))

    __mapper_args__ = {'polymorphic_identity': 'users', 'polymorphic_on': type}

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    # """
    # Generates the Auth Token
    # :return: string
    # """
    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() +
                datetime.timedelta(hours=2, seconds=0),
                'iat':
                datetime.datetime.utcnow(),
                'sub':
                user_id
            }
            return jwt.encode(payload,
                              app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, 
                                 app.config.get('SECRET_KEY'),
                                 algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class Patient(User):
    __tablename__="patient"
    patient_id=db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.Boolean)
    mobile = db.Column(db.Unicode(10))
    date_of_birth = db.Column(db.DateTime)
    sessions = db.relationship('Session',
                                backref='patient',
                                foreign_keys='Session.patient_id',
                                lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'patient'}

    def __repr__(self):
        return f'<Patient {self.username}>'

class Doctor(User):
    __tablename__="doctor"
    doctor_id=db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # doctor_id=db.Column(db.String(64),unique=True)
    name = db.Column(db.String(64))
    qualification=db.Column(db.String(64))
    room_no=db.Column(db.String(64))
    mobile = db.Column(db.Unicode(10))
    present_status=db.Column(db.Boolean)
    consultation_fee=db.Column(db.Integer)
    dep_id=db.Column(db.Integer,db.ForeignKey('department.dep_id'))

    appointments = db.relationship('Appointment',
                                   backref='doctor',
                                   foreign_keys='Appointment.doctor_id',
                                   lazy='dynamic')

    tests = db.relationship('Test',
                            backref='doctor',
                            foreign_keys='Test.doctor_id',
                            lazy='dynamic')

    specialisations = db.relationship('Doctor_Specialisation',
                                       backref='doctor',
                                       foreign_keys='Doctor_Specialisation.doctor_id',
                                       lazy='dynamic')

    __mapper_args__ = {'polymorphic_identity': 'doctor'}
    def __repr__(self):
        return f'<Doctor {self.username}>'

class Staff(User):
    __tablename__="staff"
    staff_id=db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # staff_id=db.Column(db.String(64),unique=True)
    name = db.Column(db.String(64))
    sessions = db.relationship('Session',
                            backref='doctor',
                            foreign_keys='Session.staff_id',
                            lazy='dynamic')
    __mapper_args__ = {'polymorphic_identity': 'staff'}
    def __repr__(self):
        return f'<Staff {self.username}>'

class Lab(User):
    __tablename__="lab"
    lab_id=db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # lab_id=db.Column(db.String(64),unique=True)
    name = db.Column(db.String(64))
    tests = db.relationship('Test',
                            backref='lab',
                            foreign_keys='Test.lab_id',
                            lazy='dynamic')
    types = db.relationship('Lab_Test_Type',
                            backref='Lab',
                            foreign_keys='Lab_Test_Type.lab_id',
                            lazy='dynamic')
    __mapper_args__ = {'polymorphic_identity': 'lab'}
    def __repr__(self):
        return f'<Lab {self.username}>'

class Session(db.Model):
    __tablename__ = 'session'
    session_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    joining_date = db.Column(db.DateTime)
    discharge_date = db.Column(db.DateTime)
    billed_amount=db.Column(db.Integer)
    description = db.Column(db.Text)
    appointments = db.relationship('Appointment',
                                    backref='session',
                                    foreign_keys='Appointment.session_id',
                                    lazy='dynamic')
    session_diseases = db.relationship('Session_Disease',
                                        backref='session',
                                        foreign_keys='Session_Disease.session_id',
                                        lazy='dynamic')

class Disease(db.Model):
    __tablename__ = 'area_of_disease'
    disease_id = db.Column(db.Integer, primary_key=True)
    dep_id = db.Column(db.Integer, db.ForeignKey('department.dep_id'))
    disease_sessions = db.relationship('Session_Disease',
                                        backref='disease',
                                        foreign_keys='Session_Disease.disease_id',
                                        lazy='dynamic')
   
class Session_Disease(db.Model):
    __tablename__ = 'session_disease'
    disease_id = db.Column(db.Integer, db.ForeignKey('area_of_disease.disease_id'), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), primary_key=True)

class Test(db.Model):
    __tablename__='test'
    test_id = db.Column(db.Integer,unique=True,primary_key=True)
    time = db.Column(db.DateTime)
    result = db.Column(db.String(64))
    feedback = db.Column(db.Text)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.doctor_id'))
    test_type_id = db.Column(db.Integer,db.ForeignKey('test_type.test_type_id'))
    lab_id = db.Column(db.Integer,db.ForeignKey('lab.lab_id'))

class Test_type(db.Model):
    __tablename__='test_type'
    test_type_id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(64))
    cost = db.Column(db.Integer)
    tests = db.relationship('Test',
                            backref='test_type',
                            foreign_keys='Test.test_type_id',
                            lazy='dynamic')
    labs = db.relationship('Lab_Test_Type',
                            backref='test_type',
                            foreign_keys='Lab_Test_Type.test_type_id',
                            lazy='dynamic')

class Lab_Test_Type(db.Model):
    __tablename__='lab_test_type'
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.lab_id'), primary_key=True)
    test_type_id = db.Column(db.Integer, db.ForeignKey('test_type.test_type_id'), primary_key=True)


class Appointment(db.Model):
    __tablename__='appointment'
    app_id = db.Column(db.Integer,unique=True,primary_key=True)
    doctor_description = db.Column(db.Text)
    time = db.Column(db.DateTime)
    feedback_rating = db.Column(db.Float)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))

    medicines = db.relationship('Appointment_Medicine',
                                 backref='appointment',
                                 foreign_keys='Appointment_Medicine.app_id',
                                 lazy='dynamic')
    treatments = db.relationship('Appointment_Treatment',
                                 backref='appointment',
                                 foreign_keys='Appointment_Treatment.app_id',
                                 lazy='dynamic')

class Medicine(db.Model):
    __tablename__='medicine'
    medicine_id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(64))
    cost = db.Column(db.Integer)
    appointments = db.relationship('Appointment_Medicine',
                                 backref='medicine',
                                 foreign_keys='Appointment_Medicine.medicine_id',
                                 lazy='dynamic')

class Appointment_Medicine(db.Model):
    __tablename__='appointment_medicine'
    app_id = db.Column(db.Integer,db.ForeignKey('appointment.app_id'),primary_key=True)
    medicine_id = db.Column(db.Integer,db.ForeignKey('medicine.medicine_id'),primary_key=True)
    quantity = db.Column(db.Integer)

class Treatment(db.Model):
    __tablename__='treatment'
    trmrt_id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(64))
    cost = db.Column(db.Integer)
    appointments = db.relationship('Appointment_Treatment',
                                 backref='treatment',
                                 foreign_keys='Appointment_Treatment.trmrt_id',
                                 lazy='dynamic')

class Appointment_Treatment(db.Model):
    __tablename__='appointment_treatment'
    app_id = db.Column(db.Integer,db.ForeignKey('appointment.app_id'),primary_key=True)
    trmrt_id = db.Column(db.Integer,db.ForeignKey('treatment.trmrt_id'),primary_key=True)
    time = db.Column(db.DateTime)

class Specialisation(db.Model):
    __tablename__='specialisation'
    spec_id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(64))

    doctors =  db.relationship('Doctor_Specialisation',
                                backref='specialisation',
                                foreign_keys='Doctor_Specialisation.spec_id',
                                lazy='dynamic')

class Doctor_Specialisation(db.Model):
    __tablename__='doctor_specialisation'
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.doctor_id'),primary_key=True)
    spec_id = db.Column(db.Integer,db.ForeignKey('specialisation.spec_id'),primary_key=True)

class Department(db.Model):
    __tablename__='department'
    dep_id = db.Column(db.Integer,unique=True,primary_key=True)
    name = db.Column(db.String(64))

    doctors =  db.relationship('Doctor',
                                backref='department',
                                foreign_keys='Doctor.dep_id',
                                lazy='dynamic')


 
@login.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None
