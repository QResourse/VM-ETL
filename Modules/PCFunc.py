import xml.etree.ElementTree as Xet
import Modules.Functions as Func
import csv
import Config as Conf
import os
import pandas as pd
import sys
maxInt = sys.maxsize
import re

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

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
  if (reportList):
    reports  = reportList.findall("REPORT")
  else:
    print("no policy report was found")
    return []

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
      if(format == 'CSV' and Type == "Scan"):
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


def getAllCsvFileRows(_file):
  rows = []
  with open(_file, 'r') as file:
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

def getSummaryData(GeneralData,index):
  i = index + 1
  dataLength = len(GeneralData)
  #getting the summary data
  rangeObj = range(i,dataLength)
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



def getCsvReports(scans,URL,payload,header):
  file_array = []
  for scan in scans:
      #parsing the latest scan
      action = "?action=fetch&id="+scan
      REQUEST_URL = Conf.base+URL+action
      response = Func.getRequest(REQUEST_URL,payload,header)
      if (response.ok != True):
          print("Failed to get response from API")

      fileToExport = os.path.join("export","_policy_"+str(scan)+".csv")
      file_array.append(fileToExport)
      with open(fileToExport, 'w', encoding="utf-8") as f:
          f.write(response.text)
          f.close()
  return file_array

def getSummaryIndex(GeneralData):
    summaryIndex = 0
    for summaryIndex in range(0,len(GeneralData)):
        if(GeneralData[int(summaryIndex)][0] =='SUMMARY'):
            return int(summaryIndex)
        

def getDataFrameArray(rowsArray):
  FullResultArray = []
  for rows in rowsArray:
    GeneralData = getGeneralReportData(rows[1])
    id = re.findall("\d+", rows[0])
    #summaryIndex = getSummaryIndex(GeneralData)
    if (len(rows[1]) > len(GeneralData)):
        #getting the header of the summary (Always seventh row)
        #headerSummary = GeneralData[summaryIndex + 1]
        #headerSummary.append("SCAN_ID")
        #fullSummaryData = getSummaryData(GeneralData,summaryIndex+1)
        #collecting only result data (index starts after summary data ends)
        i = len(GeneralData)+1
        headerResult = rows[1][i]
        #headerResult.append("SCAN_ID")
        fullResultData = getResultData(rows[1],GeneralData)
        resultDataFrame = pd.DataFrame(fullResultData,columns=headerResult)
        resultDataFrame["SCAN_ID"] = str(id[0])
        resultDataFrame.drop(['Exception Comments History', 'Remediation', 'Evidence','Rationale'], axis=1, inplace=True)
        
        FullResultArray.append(resultDataFrame)
        #summaryDataFrame = pd.DataFrame(fullSummaryData,columns=headerSummary)
    else:
        print("please use the _policy.csv file")
  return FullResultArray


def ConsolidateReports(FullResultArray):
  report = FullResultArray[0]
  index = 1
  resultDataFrame = []
  for index in range(1,len(FullResultArray)):
      if index == 1:
          resultDataFrame = pd.concat([FullResultArray[index],report])
      else:
          resultDataFrame = pd.concat([resultDataFrame,FullResultArray[index]])
  return resultDataFrame