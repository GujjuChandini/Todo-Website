from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Second Application</p>"

# without the below lines if we run code will not output anything
# with these lines included it will do as i coded
if __name__ == "__main__":
    #app.run(debug=True) # if any error show in debug terminal
    app.run(debug=True, port=5000) # if we want to run on port 8000