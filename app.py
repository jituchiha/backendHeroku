from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, session
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo,MongoClient
from flask_bcrypt import Bcrypt
import configparser
from bson import ObjectId


from cmd import IDENTCHARS
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
import requests
import re
import configparser


from flask_mail import Mail,  Message

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',  
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'evenueproject@gmail.com',
    MAIL_PASSWORD = 'khwsihrbrhsvmrqx'
)

mail = Mail(app)


app = Flask(__name__)
CORS(app)
app.config["STRIPE_PUBLISHABLE_KEY"] = "pk_test_51MunMnJgTekCPjeanvf7YACP6MIm4CAwgb39a2zIN0QqjqqfJdDFyNp9RHz7r1Q7FwvL68gSRtdSHOHbWtAyHyPi00WhiTnwUr"
app.config["STRIPE_SECRET_KEY"] = "sk_test_51MunMnJgTekCPjeaF6zNG3J8a9HeFMCJ5QGQ42WxpQif3DRmMAIwYmSMKLgSf1u1iWLT7yKtuMfziryiKR6DPDFc00mJRyGt3P"

app.config["SECRET_KEY"] = "asdfghjklpoiuytrewqzxcvbnm1245789630"
app.config["MONGO_URI"] = "mongodb+srv://nipotdar:niks1234@cluster0.sfi1ax8.mongodb.net/test"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
collection = mongo.db.venues


# Configuration
config = configparser.ConfigParser()
config.read('config.cfg')
google_client_id = config.get('GOOGLE', 'GOOGLE_CLIENT_ID')
google_client_secret = config.get('GOOGLE', 'GOOGLE_CLIENT_SECRET')
# shipping_client_key = config.get('SHIPPING', 'CLIENT_KEY')
# map_key = config.get('MAP', 'MAP_KEY')

# Input credentials
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", google_client_id)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", google_client_secret)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    if user:
        return user
    
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home'))








@app.route('/voprofile',methods= ['GET'])
def voprofile():
    vo_email = session['email']
    print(vo_email)

    docs = list(mongo.db.voevent.find())

    for doc in docs:
        doc['_id'] = str(doc['_id'])

    for d in docs:
        print(docs)

    # for d in docs:
    #     d.pop('_id', None)
    #     print(d)

   

    

    print("Breaker.........................................................................."+"\n")
    #print(docs)

    filtered_data = [d for d in docs if d.get('owner') == vo_email]

    # Print filtered data
    print(filtered_data)




    json_data = jsonify(filtered_data)

    return json_data


@app.route("/voprofile/<string:event_id>", methods=["PUT"])
def update_event_status(event_id):
    events = mongo.db.voevent  # Replace 'events' with the name of your MongoDB collection
    print("eventId: ",event_id)
    # Get the updated eventStatus from the request
    event_status = request.json.get("eventStatus")
    print("event Stats: ", event_status)

    # Update the eventStatus in the MongoDB document
    events.update_one(
        {"_id": event_id},
        {"$set": {"eventStatus": event_status}}
    )

    return jsonify({"message": "Event status updated successfully"})



























@app.route('/voview', methods =['POST'])  
def voview():
    print(session['email']+" "+"Why is this not printingggg")
    owner_email = session['email']
    client = MongoClient('localhost',8080)

    db = client['test']

    collection = db['voevent']

    collectionList = mongo.db.list_collection_names()
    if "voevent" not in collectionList:
       collection = db['voevent']
    else:
        print("Ignore this collection already present in db...")

    
    # # cursor = collection.find()

    # # for doc in cursor:
    # #     print(doc)

    # venuename = request.json.get("venuename")
    # location = request.json.get("location")
    # time = request.json.get("time")
    # date = request.json.get("date")
    # eventStatus = request.json.get("eventStatus")

    
    # Define the schema
    schema = {
        "venuename": {"type": "string"},
        "location": {"type": "string"},
        "time": {"type": "string"},
        "date": {"type": "string"},
        "eventStatus": {"type": "string"},
        "owner": {"type": "string"}
    }

        # Insert document with schema
    venuename = request.json.get("venuename")
    location = request.json.get("location")
    time = request.json.get("time")
    date = request.json.get("date")
    eventStatus = request.json.get("eventStatus")
    owner_email = session['email']



    document = {
        "venuename": venuename,
        "location": location,
        "time": time,
        "date": date,
        "eventStatus": eventStatus,
        "owner_email": owner_email
    }

    print("Voview details: " + venuename + ' ' + location+' '+ time + ' '+date + ' '+eventStatus + ' '+ owner_email)

    mongo.db.voevent.insert_one(document)

    response = {
        "message": "Stored new event"
    }

    return response


    # mongo.db.voevent.insert_one({
    #     "venuename" : venuename,
    #     "location" : location,
    #     "time" : time,
    #     "date" : date,
    #     "eventStatus" :  eventStatus,
    #     "owner" : owner_email
    # })
    
    # response = {
    #     "message": "Stored new event"
    # }

    # return response

# @app.route('/home', methods = ["GET"])
# def home():
#     # sess = request.json.get("session")
#     # print(sess)
#     print(session)
#     if session:
#         if 'firstname' in session:
#             firstname = session['firstname']
#             email = session['email']
#     else:
#         firstname = ""
#         email = ""
#     print(email)
#     response = {
#         "session": session,
#         "firstname": firstname,
#         "email": email
#     }
#     return response



# @app.route("/glogin")
# def login():
#     # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)

@app.route('/login', methods=["POST"])
def login():

    # Find out what URL to hit for Google login
    # google_provider_cfg = get_google_provider_cfg()
    # authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # # Use library to construct the request for Google login and provide
    # # scopes that let you retrieve user's profile from Google
    # request_uri = client.prepare_request_uri(
    #     authorization_endpoint,
    #     redirect_uri=request.base_url + "/callback",
    #     scope=["openid", "email", "profile"],
    # )
    # return redirect(request_uri)

    usertype = request.json.get("usertype")

    if usertype == '2':

        email = request.json.get('email')
        password = request.json.get('password')
        response = {
            "email": email,
            "password": password,
            "message": "Received Details"
        }   

        found_user = mongo.db.venueowner.find_one({"email": email})
        if found_user:
            if bcrypt.check_password_hash(found_user['password'], password):
                session['firstname'] = found_user['firstname']
                session['lastname'] = found_user['lastname']
                session['email'] = found_user['email']

                response = {
                    "email": email,
                    "password": password,
                    "session": session['firstname'],
                    "message": "Login Successful"
                }   

                # return jsonify({'redirect_url':'/voview'})
            
            else:
                response = {
                "message": "Wrong Password. Try Again."
                }
        else:

            response = {
                "message": "User not found"
            }

        #commenting session as I think it's being run for every venue creation
        #print(session)
        #response.redirect_uri("http://localhost:8080/voview")
        return response


    elif usertype == '1':





        email = request.json.get('email')
        password = request.json.get('password')
        response = {
            "email": email,
            "password": password,
            "message": "Received Details"
        }   

        found_user = mongo.db.users.find_one({"email": email})
        if found_user:
            if bcrypt.check_password_hash(found_user['password'], password):
                session['firstname'] = found_user['firstname']
                session['lastname'] = found_user['lastname']
                session['email'] = found_user['email']

                response = {
                    "email": email,
                    "password": password,
                    "session": session['firstname'],
                    "message": "Login Successful"
                }   
            
            else:
                response = {
                "message": "Wrong Password. Try Again."
                }
        else:

            response = {
                "message": "User not found"
            }

        #Commenting session as I think it's running for every voview request 

        #print(session)

        return response

    else:
        response = {
            "message": "Invalid User type, Select one among user or venue Owner"
        }

        return response 
    
@app.route('/register', methods=["POST"])
def register():
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    phone = request.json.get("phone")
    email = request.json.get("email")
    password = request.json.get("password")
    usertype = request.json.get("usertype")

    print("USER DEETS: " + firstname + ' ' + lastname)

    hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')

    if usertype == '2':
        client = MongoClient('localhost', 8080)
        db = client['test']
        collection = db['venueowner']
        collectionList = mongo.db.list_collection_names()
        if "venueowner" not in collectionList:
            collection = db['venueowner']
        else:
            print("Ignore this vo collection already present in db")

        mongo.db.venueowner.insert_one({
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone,
            "usertype": usertype,
            "email": email,
            "password": hash_pass,
        })

        response = {
            "name": firstname + lastname,
            "message": "RECEIVED CREDS"
        }

        return response

    else:
        mongo.db.users.insert_one({
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone,
            "usertype": usertype,
            "email": email,
            "password": hash_pass,
        })

        response = {
            "name": firstname + lastname,
            "message": "RECEIVED CREDS"
        }

        return response


@app.route('/profile')
def profile():
    if 'email' in session:
        return {
            "session_email": session['email']
        }
    else:
        return {
            "session_email": ""
        }
    
@app.route('/logout')
def logout():
    session.clear()

    return {
        "message": "Logout successful"
    }

@app.route("/data")
def get_documents():

    name=request.args.get('name',default=None)
    location=request.args.get('location',default=None)
    capacity=request.args.get('capacity',default=None)
    search_query=request.args.get('search_query',default=None)

    print(name or location or capacity)

    query={}

    if search_query:
        regex = { '$regex': search_query, '$options': 'i' }
        query = {'$or': [{ 'name': regex },{ 'location': regex }]}
    if name:
        query['name']=name
    if location:
        query['location']=location
    if capacity:
        query['capacity']=int(capacity)
    
    documents = list(collection.find(query))
    
    # convert from BSON to JSON format by converting all the values for the keys to string
    json_docs = []
    for doc in documents:
        json_doc = {}
        for key, value in doc.items():
            if key == "availability" or key == "booked":
                json_doc[key] = list(value)
            json_doc[key] = str(value)
        json_docs.append(json_doc)

    return jsonify(json_docs)

@app.route('/getbooked')
def get_avails():
    docs = list(mongo.db.booked.find())
    # print(docs)

    json_docs = []
    for doc in docs:
        json_doc = {}
        for key, value in doc.items():
            json_doc[key] = str(value)
        json_docs.append(json_doc)

    return jsonify(json_docs)

@app.route('/book_venue', methods=["POST"])
def book_venue():
    name = request.json.get("name")
    location = request.json.get("location")
    date = request.json.get('date')
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    booked_by = request.json.get('booked_by')
    owner = request.json.get("owner")

    docs = mongo.db.booked.find()
    for doc in docs:
        if doc["name"] == name and doc["location"] == location:
            if doc["start_time"] == start_time or doc["start_time"] < start_time < doc["end_time"]:
                if doc["booked_by"] == session["email"]:
                    return{
                        "message": "Already booked. Check mail."
                    }
                else:
                    return {
                        "message": "Not available. Try a different slot."
                    }
            
    try: 
        mongo.db.booked.insert_one({
            "name": name,
            "location": location,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "booked_by": booked_by,
            "owner": owner
        })

    except Exception as e:
        print(e)

    response = {
        "message": "Booking successful"
    }

    return redirect(url_for('send_mail', name=name, location=location, start_time=start_time, end_time=end_time)), response

@app.route('/send_mail/<name>/<location>/<start_time>/<end_time>')
def send_mail(name, location, start_time, end_time):
    name1 = name
    location1 = location
    start = start_time
    end = end_time
    html_content = f'<div> Hello! </div> <div> Here are the details of your booking: </div> </br> <ul> <li> Venue: {name1} </li> <li> Location: {location1} </li> <li> Time: {start} to {end} </li> </ul>'
    msg = mail.send_message(
        subject='Venue booking confirmation!',
        sender='evenueproject@gmail.com',
        recipients=['nikita.potdar15@gmail.com'],
        html=html_content
    )

    # mail.send(msg)

    response = {
        "message": "Booking Successful!"
    }

    return response

if __name__ == '__name__':
    app.secret_key = "asdfgh"
    #app.run(debug = True)
    app.run(host="0.0.0.0",port=8080,debug=True)