import xml.etree.ElementTree as Xet
import Functions as Func




def getListOfScanIds(Scanlist):
  scans = []
  for scan in Scanlist:
    scans.append(scan['ID'])
  return scans

def getPcScans(POLICY_LIST_XML,ScanDateforSQL):
    rows = []
    tree = Xet.parse(POLICY_LIST_XML)
    root = tree.getroot()
    Data = root.find("RESPONSE")
    reportList = Data.find("REPORT_LIST")
    reports  = reportList.findall("REPORT")

    for report in reports:
        Id = Func.tryToGetAttribute(report,"ID")
        print("procecing report ",str(Id))
        Type= Func.tryToGetAttribute(report,"TYPE")
        title= Func.tryToGetAttribute(report,"TITLE")
        format= Func.tryToGetAttribute(report,"OUTPUT_FORMAT")
        lunch= Func.tryToGetAttribute(report,"LAUNCH_DATETIME")
        statusObj = Func.tryToGetObj(report,"STATUS")
        state= Func.tryToGetAttribute(statusObj,"STATE")
        expires = Func.tryToGetAttribute(report,"EXPIRATION_DATETIME")
        if(format == 'CSV'):
            rows.append({'SCANDATEFORSQL' : ScanDateforSQL,
                    "ID": Id,
                    "TYPE": Type,
                    "FORMAT":format,
                    "TITLE":title,
                    "LAUNCH_DATETIME": lunch,
                    "OUTPUT_FORMAT": format,
                    "EXPIRATION_DATETIME": expires,
                    "STATE":state
                    })

        

    return rows