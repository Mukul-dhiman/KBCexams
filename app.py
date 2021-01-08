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

        exist = api.UserExist(email)

        if exist:
            token = TimeSecureMailToken.dumps(email, salt='email-confirm')
            link = url_for('reset_password', token=token, _external=True)
            msg = 'This link will be desable in 10 Minutes. \nReset Password Link:' + str(link)
            mail.send(email,msg)

        else:
            link = url_for('signup', _external=True)
            msg = 'You do not have an account please sign-up ' + str(link)
            mail.send(email,msg)

        return render_template('pre_pages/link_message.html',exist=exist)

    return render_template('pre_pages/forget_password.html')


@app.route('/reset_password/<token>')
def reset_password(token):

    try:
        email = TimeSecureMailToken.loads(token, salt='email-confirm', max_age=3600)

        return render_template('pre_pages/reset_password.html', email=email, token=token)

    except SignatureExpired:
        return render_template('pre_pages/reset_link_expire.html')

@app.route("/reset_password_confirm_api",methods=['GET','POST'])
def reset_password_confirm_api():
    
    if request.method == 'POST':
        form_details = request.form
        
        if(form_details['password']!=form_details['password2']):
            return redirect("/reset_password/error/"+str(form_details['token']))

        api.change_password(form_details['email'],form_details['password'])

        return redirect("/login")

    return redirect("/reset_password/"+str(form_details['token']))

@app.route('/reset_password/error/<token>')
def reset_password_error(token):

    try:
        email = TimeSecureMailToken.loads(token, salt='email-confirm', max_age=3600)

        return render_template('pre_pages/reset_password.html', email=email, token=token,error="on")

    except SignatureExpired:
        return render_template('pre_pages/reset_link_expire.html')


# for local 
if __name__=='__main__':
    app.run(debug=True)