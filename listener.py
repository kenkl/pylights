#!/usr/bin/env python3

from flask import Flask, request, render_template
from scenes import *

app = Flask(__name__)

@app.route('/')
def default_page():
    text = 'call with /api?call=scenefunction() with NO embedded spaces.\n\n'
    #return text
    return render_template('top.html')

@app.route('/api')
def api():
    call = request.args.get('call', type = str)
    gotthis = eval(call)
    if not gotthis == None:
        if isinstance(gotthis, str) or isinstance(gotthis, dict):
            #return gotthis
            return render_template('apidone.html')
        elif isinstance(gotthis, bool) or isinstance(gotthis, list) or isinstance(gotthis, tuple):
            #return str(gotthis)
            return render_template('apidone.html')
        else:
            #return gotthis
            return render_template('apidone.html')
        
    else:
        #return call
        return render_template('apidone.html')

@app.route('/api2')
def api2():
    call = request.args.get('call', type = str)
    gotthis = eval(call)
    if not gotthis == None:
        if isinstance(gotthis, str) or isinstance(gotthis, dict):
            return gotthis
        elif isinstance(gotthis, bool) or isinstance(gotthis, list) or isinstance(gotthis, tuple):
            return str(gotthis)
        else:
            return gotthis
        
    else:
        return call


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)


