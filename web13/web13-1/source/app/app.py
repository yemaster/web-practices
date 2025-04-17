from flask import Flask, render_template_string, request

app = Flask(__name__)
app.secret_key = "flag{test_flag}"

@app.get('/')
def index():
    name = request.args.get('name')
    if not name:
        name = "Guest"
    greeting = f"Hello, {name}!"
    with open("./templates/index.html", "r") as f:
        template = f.read()
    template = template.replace("{{ greeting }}", greeting)
    return render_template_string(template)


if __name__ == '__main__':
    app.run(debug=True)