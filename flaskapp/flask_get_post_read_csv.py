
from flask import Flask, render_template
import pandas as pd
 
#*** Backend operation
# Read csv file in python_ flask
df = pd.read_csv(r'input\tripadivsordata.csv',sep=';')

 
# WSGI Application
# Configure template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
 
@app.route('/')
def index():
    return render_template('index_upload_and_show_data_page2.html')
 
@app.route('/show_data',  methods=("POST", "GET"))
def showData():
    # Convert pandas dataframe to html table flask
    df_html = df.to_html()
    return render_template('show_csv_data.html', data=df_html)
 
if __name__=='__main__':
    app.run(debug = True)