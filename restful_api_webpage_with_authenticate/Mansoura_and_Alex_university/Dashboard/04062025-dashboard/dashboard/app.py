#sudo apt install python3-flask
#pip3 install flask
#pip3 install flask-cors

import sqlite3
from flask import Flask, render_template, request, jsonify ,  abort ,redirect, url_for , session
from db import create_db
import jwt
import hashlib
from datetime import timedelta
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import json 
import time 

app = Flask(__name__)
CORS(app)

app.secret_key = b'SECRET_KEY'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

create_db()


# # A secret key that will be used to sign the JWT token
app.config['SECRET_KEY'] = 'SECRET_KEY'

# A route that returns the HTML login page
@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# A route that handles the login request
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)
    # connect to the database and check the credentials
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    if user:
        session['authenticated'] = True
        return redirect(url_for('firewall'))
    else:
        return jsonify({'success': False})

    # and generate a JWT token if the authentication succeeds

    # Generate a JWT token with the user's username as the payload
    # payload = {'username': username}
    # token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    # # Return the JWT token as a JSON response
    # return jsonify({'token': token.decode('UTF-8')})


@app.route('/register', methods=['GET'])

def register_get():
    if request.remote_addr == '127.0.0.1' :
       return render_template('register.html')
    else :
        return abort(403)
@app.route('/register', methods=['POST'])
def register():
    if request.remote_addr == '127.0.0.1' :
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result:
        # if the username already exists, return an error message
            return jsonify({'message': 'Username already exists'}), 409
    
    # insert the username and hashed password into the database
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
    # return a success message
        return jsonify({'message': 'User created successfully'}), 201
    else :
        return abort(403)


@app.route('/firewall')
def firewall():
    # check if the user is authenticated
    print("I am at line 106")
    if not session.get('authenticated'):
        print("not authenticated")
        return redirect(url_for('login')) 
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    # clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login'))


@app.route('/send', methods=['POST'])
def send():
    print("I am at line 120")
    if not session.get('authenticated'):
        return redirect(url_for('login')) 
    data = request.get_json()
    payload = {'Authenticated' : True, 'exp': datetime.utcnow() + timedelta(seconds=1)  }
    data["Auth"] = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    query = request.args.get('api_url')
    r=  requests.post(query,json=data)
    print(data['Auth'])
    return r.text 

@app.route('/send', methods=['GET'])
def send2():
    if not session.get('authenticated'):
        return redirect(url_for('login')) 
    url = request.args.get('api_url')
    r=  requests.get(url)
    return r.text 

@app.route('/send', methods=['PUT'])
def send3():
    if not session.get('authenticated'):
        return redirect(url_for('login')) 
    url = request.args.get('api_url')
    r=  requests.put(url)
    return r.text 


@app.route('/send', methods=['DELETE'])
def send4():
    if not session.get('authenticated'):
        return redirect(url_for('login')) 
    data = request.get_json()
    payload = {'Authenticated' : True, 'exp': datetime.utcnow() + timedelta(minutes=1)  }
    data["Auth"] = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    query = request.args.get('api_url')
    r=  requests.delete(query,json=data)
    print(data['Auth'])
    return r.text 

@app.route('/vpn_status')
def vpn_status():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    # Retrieve the JSON data from a file or API
    # with open('data.json') as file:
    #     data = json.load(file)

    auth_token = "SECRET_AUTH"
    network_id = "c7c8172af142f61e"
    headers = {
    "Authorization": "token " + auth_token,}
    url = f"https://api.zerotier.com/api/v1/network/{network_id}/member"
    data = requests.get(url, headers=headers).json()
    
    # Process the data and determine the image and opacity for each object
    images = []
    for obj in data:
        # Determine the image and opacity based on your conditions
        image = 'static/img/computer_image.jpg'
        
        # Create a dictionary with the image and opacity for each object
        images.append({
            'image': image,
            'status':within_range(obj['lastSeen']) , 
            'ip_address': obj['config']['ipAssignments'][0] ,
            'type' : obj['type'] ,
            'networkId' : obj['networkId'] ,
            'nodeId' : obj['nodeId'] ,
            'controllerId' : obj['controllerId'] ,
            'machine' : obj['name']
        })
        print(images)
    # Render the template and pass the images variable to the context
    return render_template('vpn_status.html', images=images, count=len(data))

def within_range(last_online):
    current_time = int(time.time())  # Get the current Unix timestamp
    margin = current_time - last_online//1000 
    print(margin)
    if margin <= 50 and margin > 0:
        return "online"
    return "offline"


@app.route('/monitor')
def traffic_monitor():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('monitor.html')
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
