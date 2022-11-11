import xml.etree.ElementTree as Xet
import Modules.Functions as Func
import csv
import Config as Conf



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



def getAllCsvFileRows():
  rows = []
  with open(Conf.POLICYCLEAN, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
      if (row != []):
        rows.append(row)
    
    return rows

def getGeneralReportData(rows):
  index = 0 
  GeneralData = []
  while(index < len(rows)):
    if (rows[index][0] == "RESULTS"):
      break
    else:
      GeneralData.append(rows[index])
    index+=1
  return GeneralData 

def getSummaryData(GeneralData):
  i = 8
  dataLength = len(GeneralData)
  #getting the summary data
  rangeObj = range(8,dataLength)
  fullSummaryData = []
  for i in rangeObj:
    fullSummaryData.append(GeneralData[i])
  
  return fullSummaryData

def getResultData(rows,GeneralData):
  i = len(GeneralData)+1
  rangeObj = range(i+1,len(rows))
  fullResultData = []
  for i in rangeObj:
    fullResultData.append(rows[i])
  
  return fullResultData