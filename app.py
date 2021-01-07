from flask import Flask,render_template,request,redirect,url_for
import aws_db as api

app = Flask(__name__)


@app.route('/')
def start_up():
    return render_template("pre_pages/start_up.html")

@app.route('/signup', methods=['POST','GET'])
def signup():
    if(request.method == 'POST'):
        form_details = request.form
        if(form_details['password']!=form_details['password2']):
            return render_template("pre_pages/signup.html",error="active")

        api.signup(form_details['email'],form_details['password'])
        
        return render_template("pre_pages/login.html")
    return render_template("pre_pages/signup.html")

@app.route('/login')
def login():
    return render_template("pre_pages/login.html")

# for local 
if __name__=='__main__':
    app.run(debug=True)