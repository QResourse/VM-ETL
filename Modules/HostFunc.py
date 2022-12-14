from typing import Protocol
import xml.etree.ElementTree as Xet
import Modules.Functions as Func




def checkForMoreRecords(RESPONSEXML):
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()   
    Data = root.find("hasMoreRecords")
    return str(Data.text)

def getLastRecord(RESPONSEXML):
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()   
    Data = root.find("lastId")
    return str(Data.text)

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



def getHostSoftware(RESPONSEXML,ScanDateforSQL):
    rows = []
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
    Data = root.find("data")
    HostAssets  = Data.findall("HostAsset")
    index = 0
    for host in HostAssets:
        print("procecing software ",str(index))
        id = host.find("id").text
        swList = host.findall("software/list/HostAssetSoftware")
        for sw in swList:
            swName = Func.tryToGetAttribute(sw,"name")
            swVersion = Func.tryToGetAttribute(sw,"version")
            rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "HOST_ID": id,
                    "SW_NAME": swName,
                    "SW_VERSION":swVersion
                    })
            
        index+=1
    return rows




def getHostOpenPorts(RESPONSEXML,ScanDateforSQL):
    rows = []
    tree = Xet.parse(RESPONSEXML)
    root = tree.getroot()
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