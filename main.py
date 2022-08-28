
import pandas as pd 
import Functions as Func

import DetectFunc as Detect
import os as _os
from sqlalchemy import create_engine
import HostWrapper as HW



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
USESQL = []

delta = int(configList[7])
DateForSearch= Func.getSearchTime(delta)
dt_string = Func.getStempTime()
ScanDateforSQL = dt_string
if(configList[6]):
  USESQL.append(configList[6])
  DB = {'servername': configList[1],
        'database': configList[5],
        'driver': configList[0]}
  engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])
  if_exists = 'replace'
  USESQL.append(engine)
  USESQL.append(if_exists)
else:
  # conn = Func.connectToSQL()
  USESQL.append(configList[6])


# ad table to sql 
#What to do if the table exists? replace, append, or fail?



#processing hostasset api 
header = Func.getXmlHeader(USERNAME,PASSWORD)
payload = Func.getXmlPayload(0,30)
response = Func.postRequest(URL,payload,header)


if (response.ok != True):
  print("Failed to get response from API")
  exit()


with open(RESPONSEXML, "w") as f:
    f.write(response.text.encode("utf8").decode("ascii", "ignore"))
    f.close()

 #Create response and get hosts
RESPONSE_FILEARRAY =  Func.pocessHostRequests(response,RESPONSEXML,URL,payload,header,delta)

#Start Tags data
HW.getTagInfo(RESPONSE_FILEARRAY,TAGS,ScanDateforSQL,USESQL)


#Start SW data
HW.getSWInfo(RESPONSE_FILEARRAY,SW,ScanDateforSQL,USESQL)


#Start Port data
HW.GetPortInfo(RESPONSE_FILEARRAY,PORTS,ScanDateforSQL,USESQL)

#Starting Host Data
df = pd.read_csv(TAGS)
tags_for_columns =  df.TAG_NAME.unique()
list_of_tags=list(tags_for_columns)

#start Asset data
HW.GetAssetInfo(RESPONSE_FILEARRAY,HOSTS,ScanDateforSQL,list_of_tags,USESQL)

Func.MergeHostAndTags(HOSTS,TAGS)
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

header = Func.getHeader(USERNAME,PASSWORD)
response = Func.postRequest(URL,payload,header)

if (response.ok != True):
  print("Failed to get response from API")


with open(DRESPONSEXML, 'w') as f:
    f.write(response.text)
    f.close()

rows = []
rows = Detect.getHostDetections(DRESPONSEXML, ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)

df.to_csv(DETECTIONS,index=False, encoding="utf-8")


#SQL part


if(USESQL[0]):
  df.to_sql('Detections', index=False, con=USESQL[1],if_exists=USESQL[2])
  print("Detections CSV upload to SQL")
