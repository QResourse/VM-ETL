import requests
from lxml import etree as ltree
import xml.etree.ElementTree as Xet
import base64
from datetime import timedelta, date
import pyodbc 
import Modules.HostFunc as HF
import os as _os
import pandas as pd 
import shutil as SU

import re

def filter_xml_chars(text):
    # Define a regular expression pattern to match special XML characters
    pattern = re.compile(r'[&<>"\']')
    # Use the sub() method to replace the matched characters with their escaped versions
    text = pattern.sub(lambda m: {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;'}[m.group(0)], text)
    return text


def connectToSQL():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=MYDESKTOP\SQLEXPRESS;'
                        'Database=Test;'
                        'Trusted_Connection=yes;')
    return conn



def tryToGetAttribute(Object,inputString):
    try:
        output = Object.find(inputString).text
    except:
        output = "Null"
    
    return output

def tryToGetObj(Object,inputString):
    try:
        output = Object.find(inputString)
    except:
        output = "Null"
    
    return output

#SUFFIX = "2VQl"

def getToken(USERNAME,PASSWORD):
    AuthStringRaw = USERNAME+":"+PASSWORD
    base64_bytes = AuthStringRaw.encode("ascii")
    authtoken = base64.b64encode(base64_bytes)
    base64_authtoken = authtoken.decode("ascii")
    return base64_authtoken






def getSearchTime(delta):
    today = date.today()
    lastweek_date = today - timedelta(days=delta)
    DateForSearch=lastweek_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return DateForSearch

def getStempTime():
    today = date.today()
    dt_string = today.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt_string




def getXmlPayload(id,delta):
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\r\n<ServiceRequest>\r\n    <filters>\r\n        <Criteria field=\"lastVulnScan\" operator=\"GREATER\">"+str(getSearchTime(delta))+"</Criteria>\r\n <Criteria field=\"id\" operator=\"GREATER\">"+str(id)+"</Criteria>\r\n    </filters>\r\n</ServiceRequest>"
    return payload



##Override - Delete - remove the False=True option
def getXmlHeader(USERNAME={},PASSWORD={}):
    headers = {
    "Content-Type": "application/xml",
    "Accept": "application/xml",
    "X-Requested-With": "QualysPostman",
    "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
    }
    return headers



def getHeader(USERNAME,PASSWORD):
    headers = {
    "X-Requested-With": "QualysPostman",
    "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
    }
    return headers



def postRequest(URL,payload,headers,files=[]):
    print("POSTING to "+ URL)
    #print("Payload: "+ str(payload))
    #print("Header: ",headers)
    try:
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
        return str(response.status_code)
    
    if (response.ok != True):
        print("Failed to get response from API")
        return {"Error"}
    else:
        return  response


def getRequest(URL,payload,headers,files=[]):
    proxy = {}
    print("POSTING to "+ URL)
    print("Payload: "+ str(payload))
    print("Header: ",headers)
    try:
        response = requests.request("GET", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
    
    if (response.ok != True):
        print("Failed to get response from API")
        return {"Error"}
    else:
        return  response

def getTokenHeader():
    headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "X-Requested-With": "QualysPostman",
    }
    return headers


def getHeaderBearer(token):
    headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
    "X-Requested-With": "QualysPostman",
    'pageSize': '100',
    #'X-Requested-With': 'QualysPostman',
    'Authorization': 'Bearer '+ token
    }
    return headers


def getNewHeaderBearer(token,lastId):
    headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
    'X-Requested-With': 'QualysPostman',
    'lastSeenAssetId': lastId,
    'pageSize': '100',
    #'X-Requested-With': 'QualysPostman',
    'Authorization': 'Bearer '+ token
    }
    return headers
    

def pocessHostRequests(header,RESPONSEXML,URL):
    RESPONSE_FILEARRAY = []
    index = 1
    while(int(HF.checkForMoreHostRecords(RESPONSEXML)) > 0 ):
        if (index == 1):
            filename = "Response_" + str(index)+".xml"
            newFile =_os.path.join("export",filename)
            SU.copyfile(RESPONSEXML, newFile)
            RESPONSE_FILEARRAY.append(newFile)
            index+=1
        lastId = HF.checkForMoreHostRecords(RESPONSEXML)
        #_os.remove(RESPONSEXML)
        payload= {}
        #header = getNewHeaderBearer(token,lastId)
        requestUrl = URL+"?lastSeenAssetId="+str(lastId)
        response = postRequest(requestUrl,payload,header)
        if(response.status_code == 200):
            with open(RESPONSEXML, "w") as f:
                f.write(response.text.encode("utf8").decode("ascii", "ignore"))
                f.close()
            filename = "Response_" + str(index)+".xml"
            newFile =_os.path.join("export",filename)
            SU.copyfile(RESPONSEXML, newFile)
            RESPONSE_FILEARRAY.append(newFile)
            if(HF.checkForMoreRecordsBool(RESPONSEXML)):
                index+=1
            else:
                break

    print(RESPONSE_FILEARRAY)
    return RESPONSE_FILEARRAY


def MergeHostAndTags(HOSTS,TAGS):
    df1 = pd.read_csv(HOSTS)
    df2 = pd.read_csv(TAGS)
    #list of hosts from _host file
    listOfHosts= df1.ASSET_ID.unique().tolist()
    for host in listOfHosts:
        #all the indexes of tags relevent to host
        tagIndexList = df2.index[df2['HOST_ID']==host].tolist()
        print("Host ID: "+ str(host) + " Tag list: "+str(tagIndexList))
        for index in tagIndexList:
            TagName =  df2.iloc[index][3]
            hostIndex = df1.index[df1['ASSET_ID']==host].tolist()
            df1.at[int(hostIndex[0]),TagName] = 1
    df1.to_csv(HOSTS)


def deleteTempFiles(files):
    for file in files:
        if _os.path.exists(file):
            _os.remove(file)



