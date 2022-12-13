from flask import Flask, render_template, request, session, send_file, redirect, url_for, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
from pandas.io.json import json_normalize
import csv
import os


#*** Backend operation
# Read comment csv data
# df = pd.read_csv(r'input\sampledata.csv',sep=';')
# df.to_csv('sampleeng.csv',encoding='utf-8-sig',index=False)
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name

app = Flask(__name__, template_folder='flaskapp/templateFiles', static_folder='flaskapp/staticFiles')
app.secret_key = 'You Will Never Guess'
 
@app.route('/')
def welcome():
    return render_template('homepage.html')
 
@app.route('/sean',  methods=("POST", "GET"))
def index():
    return render_template('sean_page.html')
 
@app.route('/sean',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        uploaded_file = request.files['uploaded-file']
        df = pd.read_csv(uploaded_file)
        session['uploaded_csv_file'] = df.to_json()
        return render_template('sean-page.html')
 
@app.route('/show_data')
def showData():
    # Get uploaded csv file from session as a json value
    uploaded_json_string = session.get('uploaded_csv_file', None)
    
    # convert string to dict
    uploaded_json = eval(uploaded_json_string)

    # convert dict to df
    uploaded_df = pd.DataFrame.from_dict(uploaded_json)
    # Convert dataframe to html format
    uploaded_df_html = uploaded_df.sample(5).to_html()
    # uploaded_df_html = json2html.convert(json = infoFromJson)

    return render_template('show_results.html', data=uploaded_df_html)
 
@app.route('/sentiment')
def SentimentAnalysis():
    # Get uploaded csv file from session as a json value
    uploaded_json_string = session.get('uploaded_csv_file', None)    
    # convert string to dict
    uploaded_json = eval(uploaded_json_string)
    # convert dict to df
    uploaded_df = pd.DataFrame.from_dict(uploaded_json)

    # Apply sentiment function to get sentiment score
    from sentiment.sentiment import sentAnalysisApp
    sent_app = sentAnalysisApp(uploaded_df,'review')
    uploaded_df_sentiment = sent_app.runModel()
    # uploaded_df_sentiment = pd.read_csv(r'G:\My Drive\Yacht\Opdrachten\Hogeschool Utrecht\Repos\sean\flaskapp\input\results.csv')
    uploaded_df_html = uploaded_df_sentiment.sample(5).to_html()
    uploaded_df_sentiment.to_csv(r'output\results.csv')
    return render_template('show_results.html', data=uploaded_df_html)


@app.route('/downloadcsv') # this is a job for GET, not POST
def plot_csv():
    return send_file(
        r'output\results.csv')
 
if __name__=='__main__':
    app.run(debug = True)