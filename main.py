import os
import sys
import random

from flask import Flask, render_template
from des_one_block import startDES

#setup flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def start_Page():

    #define id list and pick a random artist to highlight
    try:
        return render_template("index.html")
    except:
        e = sys.exc_info()[0]
        print(e)
        return render_template("index.html")

@app.route('/encrypt/')
def encrypt():
    startDES()

#run
app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)