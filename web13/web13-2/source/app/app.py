from flask import Flask, render_template_string, request

app = Flask(__name__)
app.secret_key = "flag{test_flag}"

def check_blacklist(name):
    blacklist = "0123456789"
    for item in blacklist:
        if item in name:
            return True
    return False

@app.get('/')
def index():
    name = request.args.get('name')
    if not name:
        name = "Guest"
    if check_blacklist(name):
        return "Invalid name!"
    greeting = f"Hello, {name}!"
    with open("./templates/index.html", "r") as f:
        template = f.read()
    template = template.replace("{{ greeting }}", greeting)
    return render_template_string(template)


if __name__ == '__main__':
    app.run(debug=True)