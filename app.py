from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import aws_db as api
import mailing as mail
import secret_map
from datetime import datetime


app = Flask(__name__)


# secret key for session
app.secret_key = "basvbavaiyvbhcbbbcSBCbdibfbbcidbscbk"


from itsdangerous import URLSafeTimedSerializer, SignatureExpired
TimeSecureMailToken = URLSafeTimedSerializer(app.secret_key)



@app.route('/startup')
def start_up():
    if 'UserData' in session:
        return redirect("/")
    return render_template("pre_pages/start_up.html")

@app.route('/signup', methods=['POST','GET'])
def signup():
    if(request.method == 'POST'):
        form_details = request.form
        if(form_details['password']!=form_details['password2']):
            return render_template("pre_pages/signup.html",error="active")

        api.signup(form_details['email'],form_details['password'])
        result_dict = api.login(form_details['email'],form_details['password'])
        session['UserData'] = result_dict
        return redirect("/")


    if 'UserData' in session:
        return redirect("/")
    return render_template("pre_pages/signup.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method == 'POST'):
        form_details = request.form


        result_dict = api.login(form_details['email'],form_details['password'])

        if(result_dict['correct']=="correct"):

            session['UserData'] = result_dict
            
            return redirect("/")
        else:
            return render_template("pre_pages/login.html", wrong_credentials="wrong")
    if 'UserData' in session:
        return redirect("/")
    return render_template("pre_pages/login.html")

@app.route('/')
def home():
    if 'UserData' in session:
        contestList = api.contestList()
        return render_template("home_pages/main-content/LiveContests.html", contestList = contestList)
    return redirect("/startup")

@app.route('/ContactUs')
def ContactUs():
    return render_template("home_pages/main-content/ContactUs.html")

@app.route('/MyActivity')
def MyActivity():
    if 'UserData' in session:
        return render_template("home_pages/main-content/MyActivity.html")
    return redirect("/startup")
    

@app.route('/MyProfile')
def MyProfile():
    if 'UserData' in session:
        return render_template("home_pages/main-content/MyProfile.html")
    return redirect("/startup")

@app.route('/Wallet')
def Wallet():
    if 'UserData' in session:
        return render_template("home_pages/main-content/Wallet.html")
    return redirect("/startup")
    

@app.route('/logout')
def logout():
    if 'UserData' in session:
        session.pop('UserData')
    return redirect("/")

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():

    if request.method == 'POST':
        email = request.form['email']

        exist = api.UserExist(email)

        if (exist==1):
            token = TimeSecureMailToken.dumps(email, salt='email-confirm')
            link = url_for('reset_password', token=token, _external=True)
            msg = 'This link will be desable in 10 Minutes. \nReset Password Link:' + str(link)
            mail.send(email,msg)

            return render_template('pre_pages/link_message.html')

        else:
            link = url_for('signup', _external=True)
            msg = 'You do not have an account please sign-up ' + str(link)
            mail.send(email,msg)
            return render_template('pre_pages/link_message.html',exist="on")

    return render_template('pre_pages/forget_password.html')


@app.route('/reset_password/<token>')
def reset_password(token):

    try:
        email = TimeSecureMailToken.loads(token, salt='email-confirm', max_age=600)

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
        email = TimeSecureMailToken.loads(token, salt='email-confirm', max_age=600)

        return render_template('pre_pages/reset_password.html', email=email, token=token,error="on")

    except SignatureExpired:
        return render_template('pre_pages/reset_link_expire.html')


# contest pages
@app.route('/contest/<contestID>')
def contest_details(contestID):

    contest_data = api.get_contest_details(contestID)

    if contest_data:
        return render_template('home_pages/main-content/contest_pages/contest_details.html',contest_data = contest_data)

    else:
        return "<h1>something wrong</h1>"


@app.route('/contest/<contestID>/ticket')
def ticket(contestID):
    if 'UserData' not in session:
        return redirect("/startup")
    return render_template('home_pages/main-content/contest_pages/Payment_options.html',contestID = contestID)


@app.route('/get_contest_pay/<contestid>',methods=['POST'])
def get_contest_pay(contestid):
    data = api.get_contest_pay(contestid)
    if data == "error":
        return jsonify({'error' : 'Missing data!'})
    x = {"value":data[0][0]}
    return jsonify(x)
    

@app.route('/get_Current_Wallet_Balance/<userid>',methods=['POST'])
def get_Current_Wallet_Balance(userid):
    data = api.get_Current_Wallet_Balance(userid)
    if data == "error":
        return jsonify({'error' : 'Missing data!'})
    x = {"value":data[0][0]}
    return jsonify(x)


@app.route('/get_ticket/<contestID>/<UserID>',methods=['Post'])
def get_ticket(contestID,UserID):

    isspotsLeft = api.isspotsLeft(contestID)

    if(isspotsLeft==False):
        return jysonify({'success' : "false"})


    result = api.get_ticket(contestID,UserID)

    if result == "error":
        return jsonify({'error' : 'Missing data!'})  
    return jsonify({'success' : "complete", 'ticketID': result})


@app.route('/get_ticket_history/<UserID>/<contestID>',methods=['POST'])
def get_ticket_history(UserID,contestID):

    ticket_history = api.ticket_history(UserID,contestID)

    if ticket_history == "error":
        return jsonify({'error' : 'error in getting history!'})   
    return jsonify({'success' : ticket_history})



@app.route('/ticket/<ticketID>')
def contest_env(ticketID):

    if 'UserData' not in session:
        return redirect("/startup")

    ticket_info = api.ticket_info(ticketID)

    if session['UserData']['UserID'] != ticket_info[1]:
        return redirect("/")

    ticket_key = secret_map.map(ticketID)

    return render_template('home_pages/main-content/contest_pages/contest_env.html',ticket_key=ticket_key,ticket_info=ticket_info)


@app.route('/<secret_key>')
def ticket_secret_key(secret_key):
    
    ticketID = secret_map.get(secret_key)
     
    ticketstate = api.ticket_state(ticketID)


    if(ticketstate!=0):
        return redirect('/ticket/'+ticketID)

    ticketDate = api.ticket_start_time(ticketID)

    return render_template('home_pages/main-content/contest_pages/contest_ques_page.html',ticketDate=ticketDate,ticketID=ticketID)
    

@app.route('/get_random_questions/<ticketid>',methods=['POST'])
def get_random_questions(ticketid):

    questions = api.get_random_questions(ticketid)


    if questions == "error":
        return jsonify({'error' : 'error in getting questions!'})   
    return jsonify({'success' : questions})


@app.route('/use_ticket/<ticketid>',methods=['POST'])
def use_ticket(ticketid):

    data = request.get_data().decode("utf-8");
    startdate = data.split('&')[0].split('=')[1]
    starth = data.split('&')[1].split('=')[1]
    startm = data.split('&')[2].split('=')[1]
    starts = data.split('&')[3].split('=')[1]
    starttime = startdate + " " + starth + ":" + startm + ":" + starts 

    starttime = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')


    done = api.use_ticket(starttime, ticketid)


    if done == "error":
        return jsonify({'error' : 'error in using ticket!'})   
    return jsonify({'success' : done})



@app.route('/finish_ticket/<ticketid>',methods=['POST'])
def finish_ticket(ticketid):

    data = request.get_data().decode("utf-8");

    dic,q_response_dic={},{}

    for key, value in request.form.items():

        if key not in ['start_date','start_h','start_m','start_s']:
            q_response_dic[key.split("[")[1].split("]")[0]]=value
        else:
            dic[key]=value


    starttime = dic['start_date'] + " " + dic['start_h'] + ":" + dic['start_m'] + ":" + dic['start_s'] 



    starttime = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')

    done = api.finish_ticket(starttime, ticketid, q_response_dic)


    if done == "error":
        return jsonify({'error' : 'error in using ticket!'})   
    return jsonify({'success' : done})




# for local 
if __name__=='__main__':
    app.run(debug=True)