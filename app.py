from flask import Flask, render_template, request, redirect, url_for, session
import aws_db as api

app = Flask(__name__)

# secret key for session
app.secret_key = api.id_generator(50)


@app.route('/')
def start_up():
    if 'UserData' in session:
        return redirect("/home")
    return render_template("pre_pages/start_up.html")

@app.route('/signup', methods=['POST','GET'])
def signup():
    if(request.method == 'POST'):
        form_details = request.form
        if(form_details['password']!=form_details['password2']):
            return render_template("pre_pages/signup.html",error="active")

        api.signup(form_details['email'],form_details['password'])

        return redirect("/login")
    if 'UserData' in session:
        return redirect("/home")
    return render_template("pre_pages/signup.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method == 'POST'):
        form_details = request.form

        result_dict = api.login(form_details['email'],form_details['password'])

        if(result_dict['correct']=="correct"):

            session['UserData'] = result_dict
            
            return redirect("/home")
        else:
            return render_template("pre_pages/login.html", wrong_credentials="wrong")
    if 'UserData' in session:
        return redirect("/home")
    return render_template("pre_pages/login.html")

@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/logout')
def logout():
    session.pop('UserData')
    return redirect("/home")

# for local 
if __name__=='__main__':
    app.run(debug=True)