import xml.etree.ElementTree as Xet
import Modules.Functions as Func
from lxml import etree



def checkForMoreRecords(RESPONSEXML):
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    recordCount = root.find("count").text
    if(int(recordCount) > 0):  
        Data = root.find("hasMoreRecords")
        return str(Data.text)
    else:
        return False


def checkForMoreRecordsBool(RESPONSEXML):
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    recordCount = root.find("count").text
    if(int(recordCount) > 0): 
        if (int(root.find("hasMore").text)==1):
            return True
        else:
            return False
    else:
        return False
    

def checkForMoreHostRecords(RESPONSEXML):
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    recordCount = root.find("count").text
    if(int(recordCount) > 0):  
        Data = root.find("lastSeenAssetId")
        return str(Data.text)
    else:
        return str(0)

def getLastRecord(RESPONSEXML):
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    Data = root.find("lastId")
    return str(Data.text)

def getHostTags(RESPONSEXML,ScanDateforSQL):
    rows = []
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    Data = root.find("assetListData")
    HostAssets  = Data.findall("asset")
    index = 0
    for host in HostAssets:
        print("procecing tag ",str(index))
        id = host.find("assetId").text
        hid = host.find("hostId").text
        tagsObj = host.find("tagList")
        try:
            len(tagsObj)>0
        except:
            break
        if (tagsObj):
            tagList = tagsObj.findall("tag")
            for tag in tagList:
                tagId = Func.tryToGetAttribute(tag,"tagId")
                tagName= Func.tryToGetAttribute(tag,"tagName")
                rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                        "HOST_ID": hid,
                        "ASSET_ID": id,
                        "TAG_NAME": tagName,
                        "TAG_ID":tagId
                        })        
        index+=1
    return rows


def getHostAssets(RESPONSEXML,ScanDateforSQL):
    index = 0
    rows = []
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    Data = root.find("assetListData")
    HostAssets  = Data.findall("asset")
    for host in HostAssets:
        print("procecing host ",str(index))
        id = Func.tryToGetAttribute(host,"assetId")
        hostID = Func.tryToGetAttribute(host,"hostId")
        name = Func.tryToGetAttribute(host,"assetName")
        created = Func.tryToGetAttribute(host,"createdDate")
        #modified = Func.tryToGetAttribute(host,"modified")
        type= Func.tryToGetAttribute(host,"assetType")
        #qwebHostID = Func.tryToGetAttribute(host,"qwebHostId")
        ip_address = Func.tryToGetAttribute(host,"address")
        #fqdn = Func.tryToGetAttribute(host,"fqdn")
        os = Func.tryToGetAttribute(host,"operatingSystem/osName")
        dns= Func.tryToGetAttribute(host,"dnsName")
        #agentVer = Func.tryToGetAttribute(host,"agentInfo/agentVersion")
        #agentId = Func.tryToGetAttribute(host,"agentInfo/agentId")
        #status = Func.tryToGetAttribute(host,"agentInfo/status"
        lastCheckedIn= Func.tryToGetAttribute(host,"sensorLastUpdatedDate")
        rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "HOST_ID": hostID,
                    "ASSET_ID": id,
                    "NAME": name,
                    "CREATED":created,
                    "TYPE": type,
                    "IP_ADDRESS": ip_address,
                    "OPERATING_SYSTEM" : os,
                    "DNS_NAME" : dns,
                    "LAST_CHEKCED_IN" : lastCheckedIn
                    })
        index+=1
    return rows


def getQIDs(RESPONSEXML,ScanDateforSQL):
    index = 0
    rows = []
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
    RESPONSE = root.find("RESPONSE")
    VULN_LIST = RESPONSE.find("VULN_LIST")
    qids  = VULN_LIST.findall("VULN")
    for qid in qids:
        SOFTWARE_LIST = qid.find('SOFTWARE_LIST')
        if (SOFTWARE_LIST):
            for SW in SOFTWARE_LIST:
                print("procecing qid ",str(index))
                QID = Func.tryToGetAttribute(qid,"QID")
                SEVERITY_LEVEL = Func.tryToGetAttribute(qid,"SEVERITY_LEVEL")
                PATCHABLE = Func.tryToGetAttribute(qid,"PATCHABLE")
                PRODUCT = Func.tryToGetAttribute(SW,"PRODUCT")
                VENDOR = Func.tryToGetAttribute(SW,"VENDOR")
                VENDOR = Func.tryToGetAttribute(SW,"VENDOR")
            rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                        "QID": QID,
                        "SEVERITY_LEVEL": SEVERITY_LEVEL,
                        "PATCHABLE":PATCHABLE,
                        "PRODUCT": PRODUCT,
                        "VENDOR": VENDOR
                        })
            index+=1
    return rows


def getHostSoftware(RESPONSEXML,ScanDateforSQL):
    rows = []
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    Data = root.find("assetListData")
    HostAssets  = Data.findall("asset")
    index = 0
    for host in HostAssets:
        print("procecing software ",str(index))
        assetId = host.find("assetId").text
        hostId = host.find("hostId").text
        swList = host.findall("softwareListData/software")
        for sw in swList:
            swName = Func.tryToGetAttribute(sw,"fullName")
            softwareType = Func.tryToGetAttribute(sw,"softwareType")
            category1 = Func.tryToGetAttribute(sw,"category1")
            category2 = Func.tryToGetAttribute(sw,"category2")
            productName = Func.tryToGetAttribute(sw,"productName")
            component = Func.tryToGetAttribute(sw,"component")
            publisher = Func.tryToGetAttribute(sw,"publisher")
            marketVersion = Func.tryToGetAttribute(sw,"marketVersion")
            rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "HOST_ID": hostId,
                    "ASSET_ID": assetId,
                    "SW_NAME": swName,
                    "SW_Type":softwareType,
                    "category1": category1,
                    "category2": category2,
                    "productName": productName,
                    "component": component,
                    "publisher": publisher,
                    "marketVersion": marketVersion
                    })
            
        index+=1
    return rows




def getHostOpenPorts(RESPONSEXML,ScanDateforSQL):
    rows = []
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    Data = root.find("data")
    HostAssets  = Data.findall("HostAsset")
    index = 0
    for host in HostAssets:
        print("procecing open ports ",str(index))
        id = host.find("id").text
        portList = host.findall("openPort/list/HostAssetOpenPort")
        for portItem in portList:
            port = Func.tryToGetAttribute(portItem,"port")
            Protocol = Func.tryToGetAttribute(portItem,"protocol")
            rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "HOST_ID": id,
                    "PORT": port,
                    "PROTOCOL":Protocol
                    })
            
        index+=1
    return rows