from flask import Flask,render_template,request,redirect
import aws_db as api

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


# for local 
if __name__=='__main__':
    app.run(debug=True)