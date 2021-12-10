import os
import sys
import random

from flask import Flask, render_template, request
from DES import startDecrpyt, startEncryption

#setup flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def start_Page():
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
    keyList = []
    key1 = request.form['key1']
    if key1 != '':
        keyList.append(key1)
    key2 = request.form['key2']
    if key2 != '':
        keyList.append(key2)
    key3 = request.form['key3']
    if key3 != '':
        keyList.append(key3)
    #turn message into hex by character, remove 0x, make one large string
    for character in message:
        element = hex((ord(character)))
        element = element[2:]
        messageHex += element
    blockNum = -(len(messageHex) // -16)
    #split into 8 byte blocks 64bit each
    messageBlocks = []
    for i in range (0,blockNum):
        upper = -16 * (i+1)
        lower = -16 * i
        if lower == 0:
            block = messageHex[upper:]
            message = int(block, base=16)
        else:
            block = messageHex[-16 * (i+1):-16 * i]
            message = int(block, base=16)
        messageBlocks.append(message)
    messageBlocks.reverse()
    #perform 3 DES
    for i in range(0,len(keyList)):
        enc = startEncryption(messageBlocks, keyList[i])
        cipherBlocks = list(map(lambda x: int(x, base=16), enc))
        messageBlocks = cipherBlocks
    #form to display
    display = ''
    for cipher in enc:
        cipher = cipher + '\n'
        display += cipher
    return render_template('index.html', ciphertext = display)

@app.route('/decrypt/', methods=['POST'])
def decrypt():
    keyList = []
    message = request.form['dectext']
    key1 = request.form['key1']
    if key1 != '':
        keyList.append(key1)
    key2 = request.form['key2']
    if key2 != '':
        keyList.append(key2)
    key3 = request.form['key3']
    if key3 != '':
        keyList.append(key3)
    #format message to be feed into the decrypt
    message.strip('\n')
    cipherBlocks = message.split("0x")
    cipherBlocks.remove('')
    cipherBlocks = list(map(lambda x: int(x, base=16), cipherBlocks))
    #perform 3 DES dec with reversed keys
    if len(keyList) == 1:
        dec = startDecrpyt(cipherBlocks, keyList[0])
        clearHex = list(map(lambda x: x[2:], dec))
    elif len(keyList) == 2:
        for i in range(0, len(keyList)):
            dec = startDecrpyt(cipherBlocks, keyList[1-i])
            halfBlocks = list(map(lambda x: int(x, base=16), dec))
            cipherBlocks = halfBlocks
        clearHex = list(map(lambda x: x[2:], dec))
    elif len(keyList) == 3:
        for i in range(0, len(keyList)):
            dec = startDecrpyt(cipherBlocks, keyList[2-i])
            halfBlocks = list(map(lambda x: int(x, base=16), dec))
            cipherBlocks = halfBlocks
        clearHex = list(map(lambda x: x[2:], dec))
    #format to display
    decodetext = ''
    for clear in clearHex: 
        decodetext += bytearray.fromhex(clear).decode(errors='backslashreplace').replace('\\xda', '<br>')
    return render_template('index.html', cleartext = decodetext)

#run
app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)
