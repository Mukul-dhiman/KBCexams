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

        return redirect("/login")
    return render_template("pre_pages/signup.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method == 'POST'):
        form_details = request.form

        result_dict = api.login(form_details['email'],form_details['password'])

        if(result_dict['correct']=="correct"):

            # make sesson here in future
            return redirect("/home")
        else:
            return render_template("pre_pages/login.html", wrong_credentials="wrong")

    return render_template("pre_pages/login.html")

@app.route('/home')
def home():
    return render_template("home.html")


# for local 
if __name__=='__main__':
    app.run(debug=True)