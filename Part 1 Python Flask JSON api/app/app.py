from flask import Flask, render_template, jsonify
import requests
import xmltodict
import json
import re

parcelurl = "http://neocando.case.edu/cando/housingReport/lbxml.jsp"
parcelpattern = re.compile('[0-9]{3}-[0-9]{2}-[0-9]{3}')
apikey = 'GOOGLE MAPS API KEY GOES HERE'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/parceljson/<pn>")
def parceljson(pn=''):
    pnvalid = parcelpattern.match(pn)
    if not pnvalid:
        return render_template('parcelasjson.html', pn=pn)
    parceldetails = ''
    if pn != '':
        parceldetails=pullparcel(pn)
    pv = json.loads(parceldetails)
    response = jsonify(pv)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    #return "<pre>"+json.dumps(pv,indent=4)+"</pre>"

@app.route("/pullparcel/")
@app.route("/pullparcel/<pn>")
def pullparcel(pn=''):
    pnvalid = parcelpattern.match(pn)
    if not pnvalid:
        return render_template('parcelasjson.html', pn=pn)
    parcelasxml = requests.get(parcelurl+"?parcel="+pn, headers={'Accept': 'application/xml'})
    #xml has leading 13 leading returns. So, strip them out with strip().
    parcelasdict = xmltodict.parse(parcelasxml.text.strip())
    return json.dumps(parcelasdict,indent=4)

@app.route("/parceldetails/<pn>")
def parceldetails(pn=''):
    pnvalid = parcelpattern.match(pn)
    if not pnvalid:
        return render_template('parcelasjson.html', pn=pn)
    parceldetails=pullparcel(pn)
    pv = json.loads(parceldetails)
    pr=pv['lbstream']['parcelid']['source'][0]['record']
    pr_address=pr['number']['value']+' '+pr['street']['value'].title()+', '+pr['neighbor']['value']+', OH '+pr['zip']['value']
    pr_res1=pv['lbstream']['parcelid']['source'][1]['record']
    return render_template('parceldetails.html', pn=pn, pr=pr, pr_address=pr_address, pr_res1=pr_res1, apikey=apikey)
