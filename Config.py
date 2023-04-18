
import pandas as pd 
import os as _os
import Modules.Functions as Func
from sqlalchemy import create_engine

df = pd.read_xml('config.xml')
configList = df.iloc[0].to_list()

USERNAME = configList[3]
PASSWORD = configList[4]

##Start Detection
base = configList[2]
###Change the environment POD



RESPONSEXML = _os.path.join("export","Response.xml")
RESPONSECSV = _os.path.join("export","Response.csv")
DRESPONSEXML = _os.path.join("export","DResponse.xml")
POLICY_LIST_XML = _os.path.join("export","PResponse.XML")
POLICYCLEAN = _os.path.join("export","_policy.csv")
POLICY_RESULT = _os.path.join("export","_policy_result.csv")
DETECTIONS = _os.path.join("export","_detections.csv")
HOSTS = _os.path.join("export","_hosts.csv")
TAGS = _os.path.join("export","_tags.csv")
SW = _os.path.join("export","_sw.csv")
PORTS = _os.path.join("export","_ports.csv")
KB_XML = _os.path.join("export","KB.xml")
KB_CSV = _os.path.join("export","KB.csv")
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