from datetime import datetime
from flask import Flask, jsonify,render_template,flash,redirect, template_rendered,url_for,session,logging,request

#prediction model
from CPModel.commodity_prediction_model import infer_model
#from CPModel.Nakuru_model import timeseries_predictor

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/analysis')
def analysis():
    county_name=request.args.get('county_name')
    #dates for trends
    fstart_date=request.args.get('fstart_date')
    fend_date=request.args.get('fend_date')
    #dates for prediction
    pred_strdate=request.args.get('fstr')
    pred_enddate=request.args.get('fend')
    
    fstart_date=datetime.strptime(fstart_date,'%Y-%m-%d')
    fend_date=datetime.strptime(fend_date,'%Y-%m-%d')
    pred_strdate=datetime.strptime(pred_strdate,'%Y-%m-%d')
    pred_enddate=datetime.strptime(pred_enddate,'%Y-%m-%d')
    pred=infer_model(county_name,fstart_date,fend_date,pred_strdate,pred_enddate)
    
    return render_template('analysis.html',county=county_name,startDate=fstart_date,endDate=fend_date,predStrdate=pred_strdate,predEnddate=pred_enddate,prediction=pred)

@app.route('/submit',methods=['POST'])
def submitForm():
    county_name=request.form.get('countyName')
    fstart_date=request.form.get('str_date')
    fend_date=request.form.get('end_date')
    future_start_date=request.form.get('fs_date')
    future_end_date=request.form.get('fe_date')
    
    return redirect(f"/analysis?county_name={county_name}&fstart_date={fstart_date}&fend_date={fend_date}&fstr={future_start_date}&fend={future_end_date}")



if __name__=='__main__':
    app.secret_key='key123'
    app.run(debug=True)