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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
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
        if password in userDetails:
            return ('SUCCUSS')
        else:
            return ('ERROR')
       
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
