from datetime import datetime, date, timedelta
from flask import Flask, jsonify,render_template,flash,redirect, template_rendered,url_for,session,logging,request
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import mysql.connector
from mysql.connector import errorcode
#prediction model
#from CPModel.Nakuru_model import timeseries_predictor

app=Flask(__name__)

#configure database (MYSQL)

app.config['MYSQL_HOST']='' #host
app.config['MYSQL_USER']='' #user
app.config['MYSQL_PASSWORD']='' #your password
app.config['MYSQL_DB']=''
app.config['MYSQL_CURSORCLASS']='DictCursor'


#initialize mysql
mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

class Submit(Form):
    date1=StringField('date1',[validators.Length(min=7,max=7)])
    date2=StringField('date2',[validators.Length(min=7,max=7)])

@app.route('/nakuru_reg',methods=['GET','POST'])
def nakuru_reg():
    form=Submit(request.form)
    if request.method=='POST' and form.validate():
        d1=form.date1.data
        d2=form.date2.data
        
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO data(start_date,end_date) VALUES(%s,%s)",(d1,d2))
        
        mysql.connection.commit()
        cur.close()
        
        return render_template('nakuru_reg.html')
    return render_template('nakuru_reg.html',form=form)



@app.route('/nakuru')
def nakuru():
        
        
        return render_template('nakuru.html')


if __name__=='__main__':
    app.secret_key='key123'
    app.run(debug=True)