import xml.etree.ElementTree as Xet
import requests
import xml.etree.ElementTree as Xet
import base64
from datetime import timedelta, date
import pyodbc 


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



#SUFFIX = "2VQl"

def getToken(USERNAME,PASSWORD):
    AuthStringRaw = USERNAME+":"+PASSWORD
    base64_bytes = AuthStringRaw.encode("ascii")
    authtoken = base64.b64encode(base64_bytes)
    base64_authtoken = authtoken.decode("ascii")
    return base64_authtoken






def getSearchTime():
    today = date.today()
    lastweek_date = today - timedelta(days=150)
    DateForSearch=lastweek_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return DateForSearch

def getStempTime():
    today = date.today()
    dt_string = today.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt_string




def getXmlPayload():
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\r\n<ServiceRequest>\r\n    <filters>\r\n        <Criteria field=\"lastVulnScan\" operator=\"GREATER\">"+str(getSearchTime())+"</Criteria>\r\n    </filters>\r\n</ServiceRequest>"
    return payload



##Override - Delete - remove the False=True option
def getXmlHeader(Fake,USERNAME={},PASSWORD={}):
    if (Fake==False):
        headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml",
        "X-Requested-With": "QualysPostman",
        "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
        }
    else:
        headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml",
        "X-Requested-With": "Qualys",
        "Authorization": "Basic cWF1eXM0YWE6XjRiQTFZR14yVlFs"
        }

    return headers



def getHeader(Fake,USERNAME,PASSWORD):
    if (Fake==False):
        headers = {
        "X-Requested-With": "QualysPostman",
        "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
        }
    else:
        headers = {
        "X-Requested-With": "Qualys",
        "Authorization": "Basic cWF1eXM0YWE6XjRiQTFZR14yVlFs"
        }

    return headers



def postRequest(URL,payload,headers,files=[]):
    print("POSTING to "+ URL)
    print("Payload: "+ str(payload))
    try:
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
    
    if (response.ok != True):
        print("Failed to get response from API")
        return {"Error"}
    else:
        return  response