from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response
import jwt
import datetime
import requests
from functools import wraps
import os
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_for_ctf_NOT_possible_to_Guess'
app.config['JWT_SECRET'] = 'secops'

# Simple user database
users = {
    'member': {
        'password': 'password123',
        'role': 'user'
    },
    'admin': {
        'password': 'SECOPS{SSrF_JwT_H4cK3d_MbrOuk#lik}',
        'role': 'admin'
    }
}

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            return redirect(url_for('login'))
        
        try:
            data = jwt.decode(token, app.config['JWT_SECRET'], algorithms=["HS256"])
            current_user = data['username']
            role = data['role']
        except:
            # If token is invalid, clear it and redirect to login
            response = make_response(redirect(url_for('login')))
            response.set_cookie('token', '', expires=0)
            return response
            
        return f(current_user, role, *args, **kwargs)
    
    return decorated

# Helper function to check if URL is local
def is_local_address(url):
    try:
        hostname = url.split('://')[1].split('/')[0].split(':')[0]
        ip = socket.gethostbyname(hostname)
        return ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.') or ip == 'localhost'
    except:
        return False

# Routes
@app.route('/')
def index():
    client_ip = request.remote_addr
    
    # Check if the request is from localhost
    if client_ip == '127.0.0.1' or client_ip == 'localhost':
        # Check if a file parameter was provided
        file_path = request.args.get('file')
        if file_path:
            try:
                # Make sure we only access files in the current directory
                safe_path = os.path.basename(file_path)
                file_location = os.path.join(os.getcwd(), safe_path)
                
                # Check if the file exists and read it
                if os.path.isfile(file_location):
                    with open(file_location, 'r') as f:
                        content = f.read()
                    return content
                else:
                    return f"File {safe_path} not found", 404
            except Exception as e:
                return f"Error reading file: {str(e)}", 500
    
    # Default behavior for non-localhost or no file parameter
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            token = jwt.encode({
                'username': username,
                'role': users[username]['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.config['JWT_SECRET'])
            
            # Set token as cookie and redirect
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('token', token, httponly=True)
            return response
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
@token_required
def dashboard(current_user, role):
    return render_template('dashboard.html', username=current_user, role=role)

@app.route('/admin')
@token_required
def admin(current_user, role):
    if role != 'admin':
        return redirect(url_for('dashboard'))
    
    # Hidden feature - SSRF vulnerability
    url = request.args.get('fetch')
    file = request.args.get('file')
    content = None
    
    if url:
        if is_local_address(url):
            if file:
                try:
                    response = requests.get(f"{url}?file={file}", timeout=3)
                    content = response.text
                except:
                    content = "Error fetching URL"
            else:
                content = "You need to specify the file param to fetch the file"
        else:
            content = "Only local URLs are allowed."
    
    return render_template('admin.html', username=current_user, content=content)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)