import os
import sys
import random

from flask import Flask, render_template, request
from des_one_block import startDecrpyt, startEncryption

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

@app.route('/encrypt/', methods=['POST'])
def encrypt():
    message = request.form['enctext']
    messageHex = ''
    key = request.form['key']
    for character in message:
        element = hex((ord(character)))
        element = element[2:]
        messageHex += element
    enc = startEncryption(messageHex, key)
    return render_template('index.html', ciphertext = hex(enc))

@app.route('/decrypt/', methods=['POST'])
def decrypt():
    message = request.form['dectext']
    key = request.form['key']
    dec = startDecrpyt(message, key)
    dec = hex(dec)
    dec = dec[2:]
    return render_template('index.html', cleartext = bytearray.fromhex(dec).decode())

#run
app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)