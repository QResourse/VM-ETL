
import pandas as pd
import HostFunc as HF

def getSWInfo(RESPONSE_FILEARRAY,SW,ScanDateforSQL,USESQL):
    #Start SW data
    cols = ["SCANDATEFORSQL","HOST_ID","SW_NAME","SW_VERSION"]
    rows = []
    for filename in RESPONSE_FILEARRAY:
        print("Processing file name: " + filename)
        rowsData = HF.getHostSoftware(filename,ScanDateforSQL)
        rows= rows + rowsData

    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(SW,index=False, encoding="utf-8")
    if(USESQL[0]):
        df.to_sql('Tags', index=False,con=USESQL[1],if_exists=USESQL[2])
        print("SW CSV upload to SQL")


def getTagInfo(RESPONSE_FILEARRAY,TAGS,ScanDateforSQL,USESQL):
    #Start Tags data
    cols = ["SCANDATEFORSQL","HOST_ID","TAG_ID","TAG_NAME"]
    rows = []
    for filename in RESPONSE_FILEARRAY:
        print("Processing file name: " + filename)
        rowsData = HF.getHostTags(filename,ScanDateforSQL)
        rows= rows + rowsData

    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(TAGS,index=False, encoding="utf-8")
    if(USESQL[0]):
        df.to_sql('Tags', index=False, con=USESQL[1],if_exists=USESQL[2])
        print("Tags CSV upload to SQL")


def GetPortInfo(RESPONSE_FILEARRAY,PORTS,ScanDateforSQL,USESQL):
    cols = ["SCANDATEFORSQL","HOST_ID","PORT","PROTOCOL"]
    rows = []
    for filename in RESPONSE_FILEARRAY:
        print("Processing file name: " + filename)
        rowsData = HF.getHostOpenPorts(filename,ScanDateforSQL)
        rows= rows + rowsData

    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(PORTS,index=False, encoding="utf-8")
    if(USESQL[0]):
        df.to_sql('Tags', index=False, con=USESQL[1],if_exists=USESQL[2])
        print("port CSV upload to SQL")


def GetAssetInfo(RESPONSE_FILEARRAY,HOSTS,ScanDateforSQL,list_of_tags,USESQL):

    cols = ["SCANDATEFORSQL","HOST_ID","NAME","CREATED","MODIFIED","TYPE","QWEB_HOST_ID","IP_ADDRESS",\
    "FQDN","OPERATING_SYSTEM","DNS_NAME","AGENT_VERSION","AGENT_ID","STATUS","LAST_CHEKCED_IN"]

    for item in list_of_tags:
        cols.append(item)

    rows=[]
    for filename in RESPONSE_FILEARRAY:
        print("Processing file name: " + filename)
        rowsData= HF.getHostAssets(filename,ScanDateforSQL)
        print("length of rows data: "+ str(len(rows)))
        rows = rows + rowsData



    print("length of rows: "+ str(len(rows)))
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(HOSTS,index=False, encoding="utf-8")

    if(USESQL[0]):
        df.to_sql('Assets', index=False, con=USESQL[1],if_exists=USESQL[2])
        print("Assets CSV upload to SQL")
