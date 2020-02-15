from . import bp_callbk
from flask import redirect, request,make_response, jsonify
#from flask_cors import CORS, cross_origin
from nawalcube.common import dbfunc as db
from nawalcube.common import error_logics as errhand
from nawalcube.common import jwtfuncs as jwtf
#from nawalcube.common import settings as settings
from datetime import datetime
import pkgutil
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import jwt
import urllib.parse as up

@bp_callbk.route("/callback",methods=["GET","POST","OPTIONS"])
def callback():
    if request.method=="OPTIONS":
            print("inside callback options")
            response = "inside callback options"
            #print(request.headers)
            response1 = make_response(jsonify(response))            
            return response1

    elif request.method=="GET":
        print("inside callback get")
        params = request.args
        print(params)
        code1 = params.split('code=')[1]
        code = up.unquote(code1)
        print('code1')
        print(code1)
        print('code')
        print(code)
        #print(settings.MYNOTIPG[settings.LIVE])
        #url = settings.MYNOTIPG[settings.LIVE]
        url = 'http://localhost:4200'
        #url = 'https://waki.store/shop/'
        typ = 'tlogin'
        regdata = 'success'
        msg = 'test message'
 
        response1 = make_response(redirect(url+"?type="+typ+"&regdata="+regdata+"&msg="+msg, code=302))

        response1.headers['Access-Control-Allow-Origin'] = "*"
        response1.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
        response1.headers['Access-Control-Allow-Headers'] = "Origin, entityid, Content-Type, X-Auth-Token, countryid"
        print(response1.headers)
        return response1

    elif request.method=="POST":
        print("inside callback POST")
        #payload = request.get_json()
        payload = request.data
        code = payload.split('code=')[1]
        print("payload 11111111")
        print(payload)
        print(code)
       
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        url = settings.MYNOTIPG[settings.LIVE]
        #url = 'https://waki.store/shop/'
        typ = 'login'
        regdata = 'success'
        msg = 'test message'

        response1 = make_response(redirect(url+"?type="+typ+"&regdata="+regdata+"&msg="+msg, code=302))
        print("after response make")
        response1.headers['Access-Control-Allow-Origin'] = "*"
        response1.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
        response1.headers['Access-Control-Allow-Headers'] = "Origin, entityid, Content-Type, X-Auth-Token, countryid"
        print(response1.headers)
        return response1 
