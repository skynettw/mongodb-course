from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<center><h1>Hello, World!</h1></center>"

@app.route("/about")
def about():
    return "<center><h1>About Page</h1></center>"

if __name__ == "__main__":
    app.run(debug=True)