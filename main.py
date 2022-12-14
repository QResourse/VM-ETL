
import pandas as pd 
import Modules.Functions as Func
import Config as Conf
import Modules.DetectFunc as Detect
import Modules.HostWrapper as HW
import Modules.PCFunc as PC
import time



####################Start######################
#This is hostasset API part                   #
###############################################
URL = "/qps/rest/2.0/search/am/hostasset/"
REQUEST_URL = Conf.base+URL

#processing hostasset api 
header = Func.getXmlHeader(Conf.USERNAME,Conf.PASSWORD)
payload = Func.getXmlPayload(0,30)
response = Func.postRequest(REQUEST_URL,payload,header)

if (response.ok != True):
  print("Failed to get response from API")
  exit()

with open(Conf.RESPONSEXML, "w") as f:
    f.write(response.text.encode("utf8").decode("ascii", "ignore"))
    f.close()

 #Create response and get hosts
RESPONSE_FILEARRAY =  Func.pocessHostRequests(response,Conf.RESPONSEXML,REQUEST_URL,payload,header,Conf.delta)

#Start Tags data
HW.getTagInfo(RESPONSE_FILEARRAY,Conf.TAGS,Conf.ScanDateforSQL,Conf.USESQL)
#Start SW data
HW.getSWInfo(RESPONSE_FILEARRAY,Conf.SW,Conf.ScanDateforSQL,Conf.USESQL)
#Start Port data
HW.GetPortInfo(RESPONSE_FILEARRAY,Conf.PORTS,Conf.ScanDateforSQL,Conf.USESQL)

#Starting Host Data
df = pd.read_csv(Conf.TAGS)
tags_for_columns =  df.TAG_NAME.unique()
list_of_tags=list(tags_for_columns)

#start Asset data
HW.GetAssetInfo(RESPONSE_FILEARRAY,Conf.HOSTS,Conf.ScanDateforSQL,list_of_tags,Conf.USESQL)

Func.MergeHostAndTags(Conf.HOSTS,Conf.TAGS)
time.sleep(5)

####################Start######################
#This is detection API part                   #
###############################################
URL = "/api/2.0/fo/asset/host/vm/detection/"
REQUEST_URL = Conf.base+URL
cols = ['SCANDATEFORSQL','HOST_ID','IP_ADDRESS','TRACKING_METHOD','NETWORK_ID','OPERATING_SYSTEM','DNS_NAME',\
'NETBIOS_NAME','DOMAIN','QG_HOSTID','LAST_SCAN_DATETIME','LAST_VM_SCANNED_DATE','LAST_VM_AUTH_SCANNED_DATE','LAST_PC_SCANNED_DATE','QID','TYPE',\
'FQDN','SSL','STATUS','SEVERITY','FIRST_FOUND_DATETIME','LAST_FOUND_DATETIME','LAST_TEST_DATETIME','LAST_UPDATE_DATETIME',\
'LAST_FIXED_DATETIME','IGNORED','DISABLED','TIMES_FOUND','LAST_PROCESSED_DATETIME']

payload={'action': 'list',
'status': 'New,Active,Fixed,Re-Opened',
'detection_updated_since': Conf.DateForSearch,
'output_format': 'XML',
'truncation_limit': '1000000'}

header = Func.getHeader(Conf.USERNAME,Conf.PASSWORD)
response = Func.postRequest(REQUEST_URL,payload,header)

if (response.ok != True):
  print("Failed to get response from API")


with open(Conf.DRESPONSEXML, 'w', encoding="utf-8") as f:
    f.write(response.text)
    f.close()

rows = []
rows = Detect.getHostDetections(Conf.DRESPONSEXML, Conf.ScanDateforSQL)

df = pd.DataFrame(rows, columns=cols)

df.to_csv(Conf.DETECTIONS,index=False, encoding="utf-8")



####################Start######################
#This is PC API part                   #
###############################################
#Getting a list of all recent scans 
URL = "/api/2.0/fo/report/"
action = "?action=list"
REQUEST_URL = Conf.base+URL+action
payload={}

header = Func.getHeader(Conf.USERNAME,Conf.PASSWORD)
response = Func.getRequest(REQUEST_URL,payload,header)

if (response.ok != True):
    print("Failed to get response from API")

#Writing the response to a XML file 
with open(Conf.POLICY_LIST_XML, 'w', encoding="utf-8") as f:
    f.write(response.text)
    f.close()

#list of all scans (in all formats)
Scanlist = PC.getPcScans(Conf.POLICY_LIST_XML,Conf.ScanDateforSQL)
#list of scan ids (only CSV)
scans = PC.getListOfScanIds(Scanlist)
scans.sort()

file_array = PC.getCsvReports(scans,URL,payload,header)

time.sleep(5)






######Start here for debug with static file################

rowsArray = []
for file in file_array:
    rows = PC.getAllCsvFileRows(file)
    rowsArray.append([file,rows])

FullResultArray = PC.getDataFrameArray(rowsArray)
resultDataFrame = PC.ConsolidateReports(FullResultArray)



resultDataFrame.to_csv(Conf.POLICY_RESULT,index = False)


####################Start######################
#Push to SQL                                  #
###############################################
if(Conf.USESQL[0]):
  df.to_sql('Detections', index=False, con=Conf.USESQL[1],if_exists=Conf.USESQL[2])
  print("Detections CSV upload to SQL")

