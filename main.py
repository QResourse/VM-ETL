import pandas as pd 
import xml.etree.ElementTree as Xet
import Functions as Func
import HostFunc as HF
import DetectFunc as Detect
import os as _os
from sqlalchemy import create_engine



df = pd.read_xml('config.xml')
configList = df.iloc[0].to_list()



USERNAME = configList[3]
PASSWORD = configList[4]

##Start Detection
base = configList[2]
###Change the environment POD


URL = "/qps/rest/2.0/search/am/hostasset/"
URL = base+URL
RESPONSEXML = _os.path.join("export","Response.xml")
RESPONSECSV = _os.path.join("export","Response.csv")
DRESPONSEXML = _os.path.join("export","DResponse.xml")
DETECTIONS = _os.path.join("export","_detections.csv")
HOSTS = _os.path.join("export","_hosts.csv")
TAGS = _os.path.join("export","_tags.csv")
SW = _os.path.join("export","_sw.csv")
PORTS = _os.path.join("export","_ports.csv")

DateForSearch= Func.getSearchTime()
dt_string = Func.getStempTime()
ScanDateforSQL = dt_string
if(configList[6]):
  DB = {'servername': configList[1],
        'database': configList[5],
        'driver': configList[0]}
  engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])
# conn = Func.connectToSQL()


# ad table to sql 
#What to do if the table exists? replace, append, or fail?

if_exists = 'replace'

#processing hostasset api 
header = Func.getXmlHeader(True,USERNAME,PASSWORD)
payload = Func.getXmlPayload()
response = Func.postRequest(URL,payload,header)


if (response.ok != True):
  print("Failed to get response from API")
  exit()


with open(RESPONSEXML, "w") as f:
    f.write(response.text.encode("utf8").decode("ascii", "ignore"))
    f.close()


#Start Tags data
cols = ["SCANDATEFORSQL","HOST_ID","TAG_ID","TAG_NAME"]
rows = []

rows = HF.getHostTags(RESPONSEXML,ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)
df.to_csv(TAGS,index=False, encoding="utf-8")
if(configList[6]):
  df.to_sql('Tags', index=False, con=engine,if_exists=if_exists)
  print("Tags CSV upload to SQL")


#Start SW data
cols = ["SCANDATEFORSQL","HOST_ID","SW_NAME","SW_VERSION"]
rows = []

rows = HF.getHostSoftware(RESPONSEXML,ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)
df.to_csv(SW,index=False, encoding="utf-8")
if(configList[6]):
  df.to_sql('Tags', index=False, con=engine,if_exists=if_exists)
  print("SW CSV upload to SQL")


#Start SW data
cols = ["SCANDATEFORSQL","HOST_ID","PORT","PROTOCOL"]
rows = []

rows = HF.getHostOpenPorts(RESPONSEXML,ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)
df.to_csv(PORTS,index=False, encoding="utf-8")
if(configList[6]):
  df.to_sql('Tags', index=False, con=engine,if_exists=if_exists)
  print("port CSV upload to SQL")


#start Asset data
cols = ["SCANDATEFORSQL","HOST_ID","NAME","CREATED","MODIFIED","TYPE","QWEB_HOST_ID","IP_ADDRESS",\
    "FQDN","OPERATING_SYSTEM","DNS_NAME","AGENT_VERSION","AGENT_ID","STATUS","LAST_CHEKCED_IN"]
rows= HF.getHostAssets(RESPONSEXML,ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)
df.to_csv(HOSTS,index=False, encoding="utf-8")

if(configList[6]):
  df.to_sql('Assets', index=False, con=engine,if_exists=if_exists)
  print("Assets CSV upload to SQL")

#Start detections
#base ='https://qualysapi.qg1.apps.qualys.com.au'
#base = 'https://qualysapi.qg3.apps.qualys.com'
URL = "/api/2.0/fo/asset/host/vm/detection/"
URL = base+URL
cols = ['SCANDATEFORSQL','HOST_ID','IP_ADDRESS','TRACKING_METHOD','NETWORK_ID','OPERATING_SYSTEM','DNS_NAME',\
'NETBIOS_NAME','DOMAIN','QG_HOSTID','LAST_SCAN_DATETIME','LAST_VM_SCANNED_DATE','LAST_VM_AUTH_SCANNED_DATE','LAST_PC_SCANNED_DATE','QID','TYPE',\
'FQDN','SSL','STATUS','SEVERITY','FIRST_FOUND_DATETIME','LAST_FOUND_DATETIME','LAST_TEST_DATETIME','LAST_UPDATE_DATETIME',\
'LAST_FIXED_DATETIME','IGNORED','DISABLED','TIMES_FOUND','LAST_PROCESSED_DATETIME']




payload={'action': 'list',
'status': 'New,Active,Fixed,Re-Opened',
'detection_updated_since': DateForSearch,
'output_format': 'XML',
'truncation_limit': '1000000'}

header = Func.getHeader(False,USERNAME,PASSWORD)
response = Func.postRequest(URL,payload,header)

if (response.ok != True):
  print("Failed to get response from API")


with open(DRESPONSEXML, 'w') as f:
    f.write(response.text)
    f.close()


rows = Detect.getHostDetections(DRESPONSEXML, ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)

df.to_csv(DETECTIONS,index=False, encoding="utf-8")


#SQL part


if(configList[6]):
  df.to_sql('Detections', index=False, con=engine,if_exists=if_exists)
  print("Detections CSV upload to SQL")
