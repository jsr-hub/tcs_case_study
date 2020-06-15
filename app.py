from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
z=0

duser=None
user=None
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        global z
        userDetails = request.form
        print(userDetails)
        Login_id = userDetails['Login_id']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("select Password from userstore where Login=%s",[Login_id])
        if resultValue > 0:
            userDetails = cur.fetchone()
        print(userDetails)
        cur.close()
        if z==0:
            if password in userDetails:
                z+=1
                print(z)
                return ('SUCCUSS')
                
            else:
                return ('ERROR')
        else:
            return ('session active')
       
    return render_template('01 Login Page.html')

@app.route('/createcustomer', methods=['GET', 'POST'])
def createcustomer():
    if request.method == 'POST':
        # Fetch form data
        userDetails = dict(request.form)
        print(userDetails)
        cur = mysql.connection.cursor()
        z=cur.execute("SELECT * FROM Customer WHERE ws_ssn= %s",(userDetails["ssn_id"],))
        print(z)
        if(len(userDetails["ssn_id"])==9 and z==0):
            
            cur.execute("insert into Customer(ws_ssn,ws_name,ws_age,ws_adrs) values (%s,%s,%s,%s)",(userDetails["ssn_id"],userDetails["name"],userDetails["age"],userDetails["addr"]))
            mysql.connection.commit()
            cur.execute("SELECT MAX(ws_cust_id) FROM Customer");
            cust_id = cur.fetchone()
            print(cust_id)
            cur.execute("insert into customerstatus(ws_ssn_id,ws_cust_id,Status,Message) values (%s,%s,%s,%s)",(userDetails["ssn_id"],cust_id,"Active","customer created succussfully"))
            mysql.connection.commit()
            cur.close()
            return('succuss')
        else:
            return('error')
        
    return render_template('02 Create Customer.html')
@app.route('/customersearchupdate', methods=['GET', 'POST'])
def customersearchupdate():
    if request.method == 'POST':
        # Fetch form data
        global user 
        userDetails = dict(request.form)
        print(userDetails)
        ssnid=userDetails['ssnid']
        custid=userDetails['custid']
        cur = mysql.connection.cursor()
        
        if(ssnid=='' and custid==''):
            return('error')
        if(ssnid!='' and custid!=''):
            z=cur.execute("SELECT * FROM Customer WHERE ws_ssn= %s AND ws_cust_id=%s",(userDetails["ssnid"],userDetails['custid']))
            if(z==0):
                return('NO CUSTOMER')
            else:
                user =cur.fetchone()
                return redirect('/updatecustomer')

        if(ssnid!=''):
            z=cur.execute("SELECT * FROM Customer WHERE ws_ssn= %s ",(userDetails["ssnid"],))
            print(z)
            if(z==0):
                return('NO CUSTOMER')
            else:
                user =cur.fetchone()
                return redirect('/updatecustomer')

        if(custid!=''):
            z=cur.execute("SELECT * FROM Customer WHERE  ws_cust_id=%s",(userDetails['custid'],))
            if(z==0):
                return('NO CUSTOMER')
            else:
                user =cur.fetchone()
                print(user)
                return redirect('/updatecustomer')
        cur.close()
        #return redirect('/updatecustomer')
    return render_template('09 customer search.html')

@app.route('/updatecustomer', methods=['GET', 'POST'])
def updatecustomer():
    
    global user
    print(user)
    if request.method == 'POST':
        # Fetch form data
        userDetails = dict(request.form)
        print(userDetails)
        cur = mysql.connection.cursor()
        z=cur.execute("UPDATE Customer SET ws_name = %s, ws_adrs= %s,ws_age=%s WHERE ws_cust_id =%s",(userDetails['name'],userDetails['adr'],userDetails['age'],user[1]))
        mysql.connection.commit()
        cur.execute("insert into customerstatus(ws_ssn_id,ws_cust_id,Status,Message) values (%s,%s,%s,%s)",(user[0],user[1],"Active","customer update complete"))
        mysql.connection.commit()
        cur.close()
        return('succuss')
    return render_template('03 UpdateCustomer.html',ssnid=user[0],custid=user[1],name=user[2],adr=user[3],age=user[4])


@app.route('/customersearchdel', methods=['GET', 'POST'])
def customersearchdel():
    if request.method == 'POST':
        # Fetch form data
        global duser 
        userDetails = dict(request.form)
        print(userDetails)
        ssnid=userDetails['ssnid']
        custid=userDetails['custid']
        cur = mysql.connection.cursor()
        
        if(ssnid=='' and custid==''):
            return('error')
        if(ssnid!='' and custid!=''):
            z=cur.execute("SELECT * FROM Customer WHERE ws_ssn= %s AND ws_cust_id=%s",(userDetails["ssnid"],userDetails['custid']))
            if(z==0):
                return('NO CUSTOMER')
            else:
                duser =cur.fetchone()
                return redirect('/deletecustomer')

        if(ssnid!=''):
            z=cur.execute("SELECT * FROM Customer WHERE ws_ssn= %s ",(userDetails["ssnid"],))
            print(z)
            if(z==0):
                return('NO CUSTOMER')
            else:
                duser =cur.fetchone()
                return redirect('/deletecustomer')

        if(custid!=''):
            z=cur.execute("SELECT * FROM Customer WHERE  ws_cust_id=%s",(userDetails['custid'],))
            if(z==0):
                return('NO CUSTOMER')
            else:
                duser =cur.fetchone()
                print(user)
                return redirect('/deletecustomer')
        cur.close()
        
    return render_template('09 customer search.html')

@app.route('/deletecustomer', methods=['GET', 'POST'])
def deletecustomer():
    
    
    global duser
    print(duser)
    if request.method == 'POST':
        # Fetch form data
        userDetails = dict(request.form)
        print(userDetails)
        cur = mysql.connection.cursor()
        z=cur.execute("delete from Customer  WHERE  ws_cust_id=%s",(duser[1],))
        mysql.connection.commit()
        cur.execute("insert into customerstatus(ws_ssn_id,ws_cust_id,Status,Message) values (%s,%s,%s,%s)",(duser[0],duser[1],"Active","customer deleted successfully"))
        mysql.connection.commit()
        cur.close()
        return('succuss')
    return render_template('04 Delete Customer.html',ssnid=duser[0],name=duser[2],adr=duser[3],age=duser[4])

@app.route('/customerstatus')
def customerstatus():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM customerstatus")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('05 Customer Status.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)
