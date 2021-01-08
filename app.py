from flask import Flask, render_template, request, redirect, url_for, session
import aws_db as api
import mailing as mail


app = Flask(__name__)


# secret key for session
app.secret_key = "basvbavaiyvbhcbbbcSBCbdibfbbcidbscbk"


from itsdangerous import URLSafeTimedSerializer, SignatureExpired
TimeSecureMailToken = URLSafeTimedSerializer(app.secret_key)



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

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():

    if request.method == 'POST':
        email = request.form['email']

        

        if api.UserExist(email):
            token = TimeSecureMailToken.dumps(email, salt='email-confirm')
            link = url_for('reset_password', token=token, _external=True)
            msg = 'This link will be desable in 10 Minutes. \nReset Password Link:' + str(link)
            mail.send(email,msg)

        else:
            link = url_for('signup', _external=True)
            msg.body = 'You do not have an account please sign-up '.format(link)
            mail.send(email,msg)

        return render_template('pre_pages/link_message.html')

    return render_template('pre_pages/forget_password.html')


@app.route('/reset_password/<token>')
def reset_password(token):
    try:
        email = TimeSecureMailToken.loads(token, salt='email-confirm', max_age=600)

    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'

# for local 
if __name__=='__main__':
    app.run(debug=True)