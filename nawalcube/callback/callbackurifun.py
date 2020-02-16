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
        params = request.args.getlist('code')
        print(params)
        code1 = params[0]
        print('code1')
        print(code1)        
        code = up.unquote(code1)

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
        client_id = 'MIF6RFEC7HN8WAJ5ZWWVZHV3EA3E7KVV'
        redirect_uri = 'https://nawalapi.herokuapp.com/callback'   
        resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        data={'grant_type': 'authorization_code',
                            'refresh_token': '',
                            'access_type': 'offline',
                            'code': code,
                            'client_id': client_id,
                            'redirect_uri': redirect_uri})

        if resp.status_code != 200:
            raise Exception('Could not authenticate!')
        print('22222222222222222')
        print(resp.json())
        dd = resp.json()
        hdr =  {'Authorization': 'Bearer ' + dd['access_token']}
        resp1 = requests.get('https://api.tdameritrade.com/v1/userprincipals', headers = hdr )
        print('333333333')
        print(resp1)
        print(resp1.json())
        print('22222222222222222')
        return resp.json()

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
