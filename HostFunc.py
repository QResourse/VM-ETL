import xml.etree.ElementTree as Xet
import Functions as Func



def getHostTags(RESPONSEXML,ScanDateforSQL):
    rows = []
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
    Data = root.find("data")
    HostAssets  = Data.findall("HostAsset")
    index = 0
    for host in HostAssets:
        print("procecing tag ",str(index))
        id = host.find("id").text
        tagsObj = host.findall("tags/list/TagSimple")
        for tag in tagsObj:
            tagId = Func.tryToGetAttribute(tag,"id")
            tagName= Func.tryToGetAttribute(tag,"name")
            rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "HOST_ID": id,
                    "TAG_NAME": tagName,
                    "TAG_ID":tagId
                    })
            
        index+=1
    return rows


def getHostAssets(RESPONSEXML,ScanDateforSQL):
    index = 0
    rows = []
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
    Data = root.find("data")
    HostAssets  = Data.findall("HostAsset")
    for host in HostAssets:
        print("procecing host ",str(index))
        id = Func.tryToGetAttribute(host,"id")
        name = Func.tryToGetAttribute(host,"name")
        created = Func.tryToGetAttribute(host,"created")
        modified = Func.tryToGetAttribute(host,"modified")
        type= Func.tryToGetAttribute(host,"type")
        qwebHostID = Func.tryToGetAttribute(host,"qwebHostId")
        ip_address = Func.tryToGetAttribute(host,"address")
        fqdn = Func.tryToGetAttribute(host,"fqdn")
        os = Func.tryToGetAttribute(host,"os")
        dns= Func.tryToGetAttribute(host,"dnsHostName")
        agentVer = Func.tryToGetAttribute(host,"agentInfo/agentVersion")
        agentId = Func.tryToGetAttribute(host,"agentInfo/agentId")
        status = Func.tryToGetAttribute(host,"agentInfo/status")
        lastCheckedIn= Func.tryToGetAttribute(host,"agentInfo/lastCheckedIn")
        rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "HOST_ID": id,
                    "NAME": name,
                    "CREATED":created,
                    "MODIFIED": modified,
                    "TYPE": type,
                    "QWEB_HOST_ID": qwebHostID,
                    "IP_ADDRESS": ip_address,
                    "FQDN" : fqdn,
                    "OPERATING_SYSTEM" : os,
                    "DNS_NAME" : dns,
                    "AGENT_VERSION" : agentVer,
                    "AGENT_ID" : agentId,
                    "STATUS" : status,
                    "LAST_CHEKCED_IN" : lastCheckedIn
                    })
        index+=1
    return rows


#SQL part



# conn = Func.connectToSQL()



# qry = "BULK INSERT " + "Detections" + " FROM '" + _os.path.join(_os.getcwd(),DETECTIONS) + "' WITH (FIRSTROW = 2,FIELDTERMINATOR = ',', ROWTERMINATOR = ' ',  TABLOCK)"
# cursor = conn.cursor()
# success = cursor.execute(qry)
# print("Detections CSV upload to SQL")
# conn.commit()

# cursor = conn.cursor()
# qry = "BULK INSERT " + "Tags" + " FROM '" + _os.path.join(_os.getcwd(),TAGS) + "' WITH (FORMAT = 'CSV', FIRSTROW = 2)"
# success = cursor.execute(qry)
# conn.commit()


# cursor = conn.cursor()
# qry = "BULK INSERT " + "Tags" + " FROM '" + _os.path.join(_os.getcwd(),TAGS) + "' WITH (FORMAT = 'CSV', FIRSTROW = 2)"
# success = cursor.execute(qry)
# conn.commit()


# cursor = conn.cursor()
# qry = "BULK INSERT " + "Assets" + " FROM '" + _os.path.join(_os.getcwd(),HOSTS) + "' WITH (FORMAT = 'CSV',FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = ' ')"
# success = cursor.execute(qry)
# conn.commit()

# cursor.close


