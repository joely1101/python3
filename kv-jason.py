from flask import Flask 
from flask import jsonify
from flask import make_response
from flask import request
from flask import abort
import json
import os
import sys
# 
def get_filfullpath(filename):

    if len(sys.argv) >= 2 and sys.argv[1]:
        prefix=sys.argv[1]
    else:
        prefix='./'
    fullpath= prefix + filename

    print(fullpath)
    if not os.path.exists(filename):
        return None
    
    return fullpath
def setconfig(filename,value):

    fp=get_filfullpath(filename)
    if not fp:
        return None
    f=open(fp, 'w')
    for key in value.keys():
        f.write(key+'='+value[key]+'\n')

    f.close()

def readconfig(filename):
    fp=get_filfullpath(filename)
    if not fp:
        print(filename + ' not found')
        return None
    words={}
    f=open(fp, 'r').read().split('\n')
    for line in f:
        line = str(line).replace('#', '\0', 1)

        if not line:
            #print('empty line')
            continue
        a,b=str(line).split('=',1)
        words[a]=b
    return words
    
app = Flask(__name__)
# 
@app.route('/api', defaults={'path': ''},methods=['GET'])
@app.route('/api/<path:path>',methods=['GET'])
def index(path):
    gg=readconfig(path)
    if not gg:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({path: gg})
    #return 'welcome'
# 

@app.route('/api/config',methods=['POST'])
def config_set():
    
    if not request.json:
        return make_response(jsonify({'error': 'not jason'}), 404)
    
    req_data = request.get_json()
    gg=None
    allgg={}
    print(req_data)
    for key in req_data.keys():
        value=req_data[key]
        print(value)
        if gg:
            del gg
        gg=readconfig(key)
        if not gg:
            return make_response(jsonify({'error': 'Not found ' + key}), 404)
        if isinstance(value, dict):
            for k2 in value.keys():
                gg[k2]=value[k2]
                print(k2 + '==' + gg[k2])
        setconfig(key,gg)
        allgg[key] =gg
    return jsonify(allgg)
@app.route('/api/control',methods=['POST'])
def control():
    print('control')
    if not request.json:
        return make_response(jsonify({'error': 'not jason'}), 404)

    req_data = request.get_json()
    for k2 in req_data.keys():
        if k2 == "mand":
            if req_data[k2] == "restart":
                print('restart mand')
                os.system('killall mand')
                return make_response(jsonify({'200OK': 'mand restart'}))
    
    return make_response(jsonify({'error': 'command not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
