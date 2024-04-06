from flask import Flask, abort, flash, redirect, render_template, request, url_for, session
from flask_session import Session
from flask_mysqldb import MySQL
from sdmail import sendmail
from datetime import date, datetime
from key import *
from stoken1 import token1
from itsdangerous import URLSafeTimedSerializer
from tokenreset import token

project = Flask(__name__ , template_folder='layout')
project.secret_key='Batch No:-5'
project.config['SESSION_TYPE'] = 'filesystem'
project.config['MYSQL_HOST'] ='localhost'
project.config['MYSQL_USER'] = 'Tejaswi_pratap'
project.config['MYSQL_PASSWORD']='Tejaswi@15-05-2003'
project.config['MYSQL_DB']='LeaveEase'
mysql=MySQL(project)
Session(project)



@project.route('/')
def index():    
    return render_template('index.html')

@project.route('/higherofficials', methods=['POST', 'GET'])
def higherofficials():
    if session.get('higherofficial'):
        return redirect(url_for('higher_official_dashboard'))
    if request.method=='POST':
        admincode=request.form['admincode']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT count(*) from ho_details where admincode=%s and password=%s',[admincode,password])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.execute('select fullname from ho_details where admincode=%s',[admincode])
            adminname = cursor.fetchone()[0]
            session['higherofficial'] = adminname
            return redirect(url_for("higher_official_dashboard"))
        else:
            flash('Invalid ID or password')
            return render_template('higherofficials.html')
    return render_template('higherofficials.html')
 
@project.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        admincode = request.form['admincode']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        acode = request.form['acode']
        Code = 'AdminGECG'
        if Code == acode:
            if  password == confirmpassword:
                cursor=mysql.connection.cursor()
                cursor.execute('select count(*) from ho_details where AdminCode=%s',[admincode])
                count=cursor.fetchone()[0]
                cursor.execute('select count(*) from ho_details where Email=%s',[email])
                count1=cursor.fetchone()[0]
                cursor.execute('select count(*) from ho_details where fullname=%s',[fullname])
                count2=cursor.fetchone()[0]
                cursor.close()
                if count==1:
                    flash('AdminCode is in use')
                    return render_template('HO_signup.html')
                elif count1==1:
                    flash('Email already in use')
                    return render_template('HO_Signup.html')
                elif count2==1:
                    flash('Fullname already in use')
                    return render_template('HO_Signup.html')
                adata={'admincode':admincode,'fullname':fullname,'password':password,'email':email}
                subject='Email Confirmation'
                body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('higherofficialconfirm',token=token(adata,salt),_external=True)}"
                sendmail(to=email,subject=subject,body=body)
                flash('Confirmation link sent to mail')
                return redirect(url_for('signup'))
            else:
                flash('Passwords does not match. Please check them')
                return render_template('Ho_signup.html')
        else:
            flash("ACODE does not match. Please check")
            return redirect(url_for('signup'))
    return render_template('HO_signup.html')

@project.route('/higherofficialconfirm/<token>')
def higherofficialconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        adata=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor()
        id1=adata['admincode']
        cursor.execute('select count(*) from ho_details where admincode=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('higherofficials'))
        else:
            cursor.execute('INSERT INTO ho_details (admincode,fullname, password, email) VALUES (%s,%s,%s,%s)',[adata['admincode'],adata['fullname'], adata['password'], adata['email']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('higherofficials'))

@project.route('/higherofficialslogout', methods=['POST', 'GET'])
def higherofficialslogout():
    if session.get('higherofficial'):
        session.pop('higherofficial')
        flash('Successfully logged out')
        return redirect(url_for('higherofficials'))
    else:
        return redirect(url_for('higherofficials'))

@project.route('/facultylogin', methods=['POST', 'GET'])
def facultylogin():
    if session.get('faculty'):
        return redirect(url_for('fdashboard'))
    if request.method=='POST':
        username=request.form['facultyid']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT count(*) from faculty_details where faculty_id=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['faculty']=username
            return redirect(url_for("fdashboard"))
        else:
            flash('Invalid ID or password')
            return render_template('FL.html')
    return render_template('FL.html')

@project.route('/flogout')
def flogout():
    if session.get('faculty'):
        session.pop('faculty')
        flash('Successfully logged out')
        return redirect(url_for('facultylogin'))
    else:
        return redirect(url_for('facultylogin'))

@project.route('/facultysignup', methods=['POST', 'GET'])
def facultysignup():
    if request.method == 'POST':
        facultyid=request.form['facultyid']
        username = request.form['username']
        password=request.form['password']
        email=request.form['email']
        phonenumber=request.form['phone_number']
        address=request.form['address']
        role=request.form['role']
        ccode=request.form['ccode']
        code="GECG"
        if code == ccode:
            cursor=mysql.connection.cursor()
            cursor.execute('select count(*) from faculty_details where faculty_id=%s',[facultyid])
            count=cursor.fetchone()[0]
            cursor.execute('select count(*) from faculty_details where email=%s',[email])
            count1=cursor.fetchone()[0]
            cursor.close()
            if count==1:
                flash('username already in use')
                return render_template('FR.html')
            elif count1==1:
                flash('Email already in use')
                return render_template('FR.html')
            data={'faculty_id':facultyid,'username':username,'password':password,'email':email,'phone_number':phonenumber,'address':address,'role':role}
            subject='Email Confirmation'
            body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('frconfirm',token=token(data,salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Confirmation link sent to mail')
            return redirect(url_for('facultysignup'))
        else:
            flash("ccode is wrong unauthorized access!")
            return redirect(url_for('facultysignup'))
            
    return render_template('FR.html')

@project.route('/frconfirm/<token>')
def fconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor()
        id1=data['faculty_id']
        cursor.execute('select count(*) from faculty_details where faculty_id=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('facultylogin'))
        else:
            cursor.execute('INSERT INTO faculty_details (faculty_id,username, password, email, phone_number, address,role) VALUES (%s,%s,%s, %s, %s, %s, %s)',[data['faculty_id'],data['username'], data['password'], data['email'], data['phone_number'], data['address'],data['role']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('facultylogin'))

@project.route('/facultyforgotpassword', methods=['POST', 'GET'])
def f_forgotpassword():
    if request.method=='POST':
        Email=request.form['email']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from faculty_details where email=%s',[Email])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT email  from faculty_details where email=%s',[Email])
            email=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(Email,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('facultylogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot_password.html')
    return render_template('forgot_password.html')

@project.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['password']
            confirmpassword=request.form['confirmpassword']
            if newpassword==confirmpassword:
                cursor=mysql.connection.cursor()
                cursor.execute('update  faculty_details set password=%s where email=%s',[newpassword,id1])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('facultylogin'))
            else:
                flash('Passwords mismatched')
                return render_template('new_password.html')
        return render_template('new_password.html')

@project.route('/fdashboard', methods=['GET', 'POST'])
def fdashboard():
    if session.get('faculty'):
        username = session.get('faculty')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username FROM faculty_details WHERE faculty_id = %s', (username,))
        name = cursor.fetchone()[0] 
        cursor.execute('SELECT Email FROM faculty_details WHERE faculty_id = %s', (username,))
        email_row = cursor.fetchone()
        email = email_row[0] if email_row else None
        cursor.execute('SELECT address FROM faculty_details WHERE faculty_id = %s', (username,))
        address = cursor.fetchone()[0]
        cursor.execute('SELECT role FROM faculty_details WHERE faculty_id = %s', (username,))
        role = cursor.fetchone()[0]
        cursor.execute('SELECT phone_number FROM faculty_details WHERE faculty_id = %s', (username,))
        phonenumber = cursor.fetchone()[0]
        cursor.execute('SELECT sum(leaves_taken) FROM leaveapplications WHERE faculty_id = %s', (username,))
        leaves_taken_row = cursor.fetchone()
        leaves_taken = leaves_taken_row[0] if leaves_taken_row else None 
        cursor.close()
        data = {
        'username': name,
        'email': email,
        'address': address,
        'role': role,
        'phonenumber': phonenumber,
        'college': 'Guntur Engineering college',
        'AllocatedLeaves': 12,
        'LeavesTaken': leaves_taken
        }
        return render_template('fdashboard.html', data=data)
    return redirect(url_for('facultylogin'))

@project.route('/facultyworkload', methods=['GET', 'POST'])
def facultyworkload():
    if session.get('faculty'):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT workload_id, workload_description, submission_date, status, acceptance_date FROM workload WHERE faculty_id = %s', (session.get('faculty'),))
        workloads = cursor.fetchall()
        count = 0
        ncount = 0
        for workload in workloads:
            if workload[3] == 'completed':
                count += 1 
            elif workload[3] in ('pending', 'urgent'):
                ncount += 1
        total_value = len(workloads)
        countper = (count / total_value) * 100 if total_value != 0 else 0
        ncountper = (ncount / total_value) * 100 if total_value != 0 else 0
        cursor.close()
        return render_template('faculty_workload.html', workloads=workloads, ncount=ncountper, count=countper)
    return redirect(url_for('facultylogin'))

@project.route('/updateworkload', methods=['POST','GET'])
def updateworkload():
    if session.get('faculty'):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT workload_description FROM workload WHERE faculty_id = %s AND status != %s', (session.get('faculty'), 'completed'))
        workloads = cursor.fetchall()
        cursor.close()
        if request.method == 'POST':
            status = request.form['status']
            workload_description = request.form['workload_description']
            cursor = mysql.connection.cursor()
            cursor.execute('update workload set status=%s where workload_description=%s and faculty_id = %s  ',(status,workload_description, session.get('faculty'),))
            mysql.connection.commit()
            cursor.close()
            flash('Successfully updated workload')
            return redirect(url_for('fdashboard'))
    return render_template('update_workload.html', workloads=workloads)

@project.route('/higher_official_dashboard', methods=['GET', 'POST'])
def higher_official_dashboard():
    if session.get('higherofficial'):
        username = session.get('higherofficial')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT fullname FROM ho_details WHERE fullname = %s', (username,))
        Fullname = cursor.fetchone()[0] 
        cursor.execute('SELECT Email FROM ho_details WHERE fullname = %s', (username,))
        email_row = cursor.fetchone()
        email = email_row[0] if email_row else None
        cursor.execute('SELECT admincode FROM ho_details WHERE fullname = %s', (username,))
        admincode = cursor.fetchone()[0]
        cursor.close()           
        data = {
        'Fullname': Fullname,
        'email': email,
        'admincode': admincode,
        'Designation': 'Higher Official',
        'college': 'Guntur Engineering college'
        }
        return render_template('higher_official_dashboard.html', data=data)            
    return redirect(url_for('higherofficials'))

@project.route('/addworkload', methods=['GET', 'POST'])
def addworkload():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT faculty_id FROM faculty_details')
    options = cursor.fetchall()
    cursor.close()
    if session.get('higherofficial'):
        if request.method == 'POST':
            workload_description = request.form['workload_description']
            submission_date = request.form['submission_date']
            status = request.form['status']
            acceptance_date = request.form['acceptance_date']
            faculty_id = request.form['faculty_id'] 
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO workload (faculty_id, workload_description, submission_date, status, acceptance_date) VALUES (%s, %s, %s, %s, %s)',(faculty_id, workload_description, submission_date, status, acceptance_date))
            mysql.connection.commit()
            cursor.close()
            return render_template('add_workload.html', options=options)
    return render_template('add_workload.html', options=options)

@project.route('/applyleave', methods=['POST', 'GET'])
def applyleave():
    if session.get('faculty'):
        if request.method == 'POST':
            fromdate = request.form['from']
            todate = request.form['to']
            reason = request.form['Reason']
            cursor = mysql.connection.cursor()
            cursor.execute('select count(status) from leaveapplications where faculty_id=%s and status =%s', (session.get('faculty'),'pending'))
            count = cursor.fetchone()[0]
            cursor.close()
            if count > 0:
                flash('You have already one leave request in process')
                return redirect(url_for('fdashboard'))
            else:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO leaveapplications (faculty_id, `from`, `to`, reason) VALUES (%s, %s, %s, %s)', (session.get('faculty'), fromdate, todate, reason))
                mysql.connection.commit()
                cursor.close()
                flash('Applied successfully')
                return redirect(url_for('fdashboard'))
    return render_template('applyleave.html')

@project.route('/hoseeingworkload', methods=['POST', 'GET'])
def hoseeingworkload():
    if session.get('higherofficial'):
        cursor = mysql.connection.cursor()
        cursor.execute('select faculty_id,username from faculty_details')
        workload1 = cursor.fetchall()
        if request.method == 'POST':
            facultyid = request.form['facultyidname']
            cursor = mysql.connection.cursor()
            cursor.execute('select workload_id,faculty_id,workload_description,status from workload where faculty_id = %s',(facultyid,))
            workload = cursor.fetchall()
            cursor.close()
            return render_template('workloadseeing.html', workloads = workload)
    return render_template('ho_workload_seeing.html',options=workload1)

@project.route('/workloadseeing')
def workloadseeing():
    return render_template('workload_seeing.html')

@project.route('/manageleaves', methods=['GET','POST'])
def manageleaves():
    if session.get('higherofficial'):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT w.workload_id, w.faculty_id, f.username, w.workload_description, w.status FROM workload w INNER JOIN faculty_details f ON w.faculty_id = f.faculty_id WHERE w.status = %s', ('completed',))
        workloads = cursor.fetchall()
        cursor.execute('''SELECT w.workload_id, w.faculty_id, f.username, w.workload_description, w.status FROM workload w INNER JOIN faculty_details f ON w.faculty_id = f.faculty_id WHERE w.status IN ('pending', 'urgent')''')
        notWorkloads = cursor.fetchall()
        cursor.execute('SELECT leaveapplications.leave_id, leaveapplications.faculty_id, faculty_details.username, leaveapplications.`from`, leaveapplications.`to`, leaveapplications.reason, leaveapplications.status FROM leaveapplications INNER JOIN faculty_details ON leaveapplications.faculty_id = faculty_details.faculty_id WHERE leaveapplications.status =%s',('pending',))
        applications = cursor.fetchall()
        cursor.execute('select leaveapplications.faculty_id, faculty_details.username,leaveapplications.leave_id from leaveapplications inner join faculty_details ON leaveapplications.faculty_id = faculty_details.faculty_id where leaveapplications.status =%s',('pending',))
        options = cursor.fetchall()
        cursor.close()
        if request.method == 'POST':
            leaveid = request.form['facultyidname']
            status = request.form['status']
            if status == 'approved':
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE leaveapplications SET status = %s where leave_id = %s', (status, leaveid))
                mysql.connection.commit()
                cursor.execute('UPDATE leaveapplications SET leaves_taken = DATEDIFF(`to`, `from`) WHERE leaves_taken IS NULL')
                mysql.connection.commit()
                cursor.execute('SELECT faculty_details.email FROM faculty_details INNER JOIN leaveapplications ON faculty_details.faculty_id = leaveapplications.faculty_id WHERE leaveapplications.leave_id = %s', (leaveid,))
                email = cursor.fetchone()
                cursor.close()
                subject='Your Leave is Approved'
                body=f"Your leave is approved\n\nEnjoy your leave"
                sendmail(to=email,subject=subject,body=body)
                return redirect(url_for('manageleaves'))
            else:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT faculty_details.email FROM faculty_details INNER JOIN leaveapplications ON faculty_details.faculty_id = leaveapplications.faculty_id WHERE leaveapplications.leave_id = %s', (leaveid,))
                email = cursor.fetchone() 
                cursor.execute('UPDATE leaveapplications SET status = %s where leave_id = %s', (status,leaveid))
                mysql.connection.commit()
                cursor.close()
                subject='Your Leave is Rejected'
                body=f"Your leave is Rejected\n\nSorry for the trouble"
                sendmail(to=email,subject=subject,body=body)
                return redirect(url_for('manageleaves'))
    return render_template('manage_leaves.html', workloads=workloads, notWorkloads=notWorkloads,applications=applications,options=options)
@project.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        faculty_id = request.form['facultyid']
        data = request.form['whathappend']
        cursor = mysql.connection.cursor()
        cursor.execute('Select username from faculty_details where faculty_id =%s',(faculty_id,))
        name = cursor.fetchone()[0]
        cursor.execute('Select email from ho_details')
        email = cursor.fetchall()
        cursor.execute('insert into contact(faculty_id, faculty_name, ThisHappened) values(%s, %s,%s)',(faculty_id,name,data))
        mysql.connection.commit()
        cursor.close()
        for i in email: 
            subject=f'Informing about the webiste'
            body=f"The faculty person name is {name}\n\n He holds the id {faculty_id}\n\n He contact you for below reason:\n\n {data}"
            sendmail(to=i,subject=subject,body=body)           
    return render_template('contact.html')
@project.route('/messages',)
def messages():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from contact')
    contacts = cursor.fetchall()
    cursor.close()
    return render_template('messages.html', contacts=contacts)

@project.route('/leavestatus')
def leavestatus():
    if session.get('faculty'):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT leaveapplications.leave_id, leaveapplications.faculty_id, faculty_details.username, leaveapplications.status, leaveapplications.reason FROM leaveapplications INNER JOIN faculty_details ON leaveapplications.faculty_id = faculty_details.faculty_id WHERE leaveapplications.faculty_id = %s',(session.get('faculty'),))
        leavedata = cursor.fetchall()
        cursor.close()
    return render_template('leave_status.html',leavedata = leavedata)

if __name__ == '__main__':
    project.run(debug= True, use_reloader=True)