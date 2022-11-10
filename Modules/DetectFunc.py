import pandas as pd 
import xml.etree.ElementTree as Xet
import Modules.Functions as Func


#Start Detection 

def getHostDetections(DRESPONSEXML, ScanDateforSQL):

    tree = Xet.parse(DRESPONSEXML)
    root = tree.getroot()
    Data = root.find("RESPONSE")
    Hosts  = Data.find("HOST_LIST")
    rows=[]

    index = 0
    for host in Hosts:
            print("Detactions: creating host ",str(index))
            id = Func.tryToGetAttribute(host,"ID")
            ip_address = Func.tryToGetAttribute(host,"IP")
            tracking = Func.tryToGetAttribute(host,"TRACKING_METHOD")
            network_id = Func.tryToGetAttribute(host,"NETWORK_ID")
            operating_system = Func.tryToGetAttribute(host,"OS")
            dns = Func.tryToGetAttribute(host,"DNS")
            dnsObj1 =  host.find("DNS_DATA/HOSTNAME")
            hostname = Func.tryToGetAttribute(dnsObj1,"HOSTNAME")
            dnsObj2 =  host.find("DNS_DATA/DOMAIN")
            domin = Func.tryToGetAttribute(dnsObj2,"DOMAIN")
            dnsObj3 =  host.find("DNS_DATA/FQDN")
            fqdn = Func.tryToGetAttribute(dnsObj3,"FQDN")
            qg_hostId = Func.tryToGetAttribute(host,"QG_HOSTID")
            last_scan_datetime = Func.tryToGetAttribute(host,"LAST_SCAN_DATETIME")
            last_vm_scan_date = Func.tryToGetAttribute(host,"LAST_VM_SCANNED_DATE")
            last_vm_auth_scan_date = Func.tryToGetAttribute(host,"LAST_VM_AUTH_SCANNED_DATE")
            last_pc_scan_date = Func.tryToGetAttribute(host,"LAST_PC_SCANNED_DATE")
            
            #
            try:
                detections =  host.findall("DETECTION_LIST/DETECTION")
            except:
                detections = False
                print("failed to get detections for host " + id + " With index " + index )

            if(detections):
                for detection in detections:
                    print("Detactions: procecing host detection ",str(index))
                    qid= Func.tryToGetAttribute(detection,"QID")
                    type = Func.tryToGetAttribute(detection,"TYPE")
                    severity = Func.tryToGetAttribute(detection,"SEVERITY")
                    ssl = Func.tryToGetAttribute(detection,"SSL")
                    status = Func.tryToGetAttribute(detection,"STATUS")
                    first_found_datetime = Func.tryToGetAttribute(detection,"FIRST_FOUND_DATETIME")
                    last_fond_datetime = Func.tryToGetAttribute(detection,"LAST_FOUND_DATETIME")
                    times_found = Func.tryToGetAttribute(detection,"TIMES_FOUND")
                    last_test_datetime = Func.tryToGetAttribute(detection,"LAST_TEST_DATETIME")
                    last_update_datetime = Func.tryToGetAttribute(detection,"LAST_UPDATE_DATETIME")
                    last_fixed_datetime = Func.tryToGetAttribute(detection,"LAST_FIXED_DATETIME")
                    is_ignored = Func.tryToGetAttribute(detection,"IS_IGNORED")
                    is_disabed = Func.tryToGetAttribute(detection,"IS_DISABLED")
                    last_processsed_datetime = Func.tryToGetAttribute(detection,"LAST_PROCESSED_DATETIME")
                    rows.append ({
                        'SCANDATEFORSQL' : ScanDateforSQL,
                        'HOST_ID': id,
                        'IP_ADDRESS': ip_address,
                        'TRACKING_METHOD': tracking,
                        'NETWORK_ID': network_id,
                        'OPERATING_SYSTEM': operating_system,
                        'DNS_NAME': dns,
                        'NETBIOS_NAME': hostname,
                        'DOMAIN': domin,
                        'QG_HOSTID': qg_hostId,
                        'LAST_SCAN_DATETIME': last_scan_datetime,
                        'LAST_VM_SCANNED_DATE': last_vm_scan_date,
                        'LAST_VM_AUTH_SCANNED_DATE': last_vm_auth_scan_date,
                        'LAST_PC_SCANNED_DATE' : last_pc_scan_date,
                        'QID' : qid,
                        'TYPE' :type ,
                        'FQDN' : fqdn	,
                        'SSL'	: ssl,
                        'STATUS' : status,
                        'SEVERITY' : severity,
                        'FIRST_FOUND_DATETIME' : first_found_datetime,
                        'LAST_FOUND_DATETIME' : last_fond_datetime,
                        'LAST_TEST_DATETIME' : last_test_datetime,
                        'LAST_UPDATE_DATETIME' : last_update_datetime,
                        'LAST_FIXED_DATETIME' : last_fixed_datetime,
                        'IGNORED' : is_ignored,
                        'DISABLED' : is_disabed,
                        'TIMES_FOUND' : times_found,
                        'LAST_PROCESSED_DATETIME': last_processsed_datetime
                            })
                index+=1
            else:
                print("no detections found for host " + str(id))
                index+=1

    return rows


#For Use with JSON
# do not use without eebug. not working
# def getDetectionsFromCsv(RESPONSECSV,ScanDateforSQL):
#     myCSV = pd.read_csv(RESPONSECSV,low_memory=False)
#     file =  open('response_f.csv', 'w')
#     index = 0 
#     while index < (len(myCSV)-1):
#         if (myCSV.iloc[index]['Host ID']):
#             print("procecing detection ",str(index))
#             rowData = myCSV.iloc[index]
#             ScanDateforSQL = dt_string
#             TrackingMethod = rowData['Tracking Method']
#             HostID = rowData['Host ID']
#             #NetworkID = rowData['Network ID']
#             IpAddress = rowData['IP Address']
#             OS = rowData['Operating System']
#             Dns = rowData['DNS Name']
#             Netbios = rowData['Netbios Name']
#             QGHost = rowData['QG HostID']
#             LastScanDate = rowData['Last Scan Datetime']
#             OsCpe = rowData['OS CPE']
#             LastVmScanDate = rowData['Last VM Scanned Date']
#             LastVmScanDuration = rowData['Last VM Scanned Duration']
#             LastAuthScanDate = rowData['Last VM Auth Scanned Date']
#             LastAuthScanDuration = rowData['Last VM Auth Scanned Duration']
#             LastPcScanDate = rowData['Last PC Scanned Date']    
#             while(myCSV.iloc[index].QID !='NaN'):
#                 if (index < len(myCSV)-1):
#                     rows.append ({
#                         'SCANDATEFORSQL' : ScanDateforSQL,
#                         'HOST_ID': HostID,
#                         'IP_ADDRESS': IpAddress,
#                         'TRACKING_METHOD': TrackingMethod,
#                         #'NETWORK_ID': NetworkID,
#                         'OPERATING_SYSTEM': OS,
#                         'DNS_NAME': Dns,
#                         'NETBIOS_NAME': Netbios,
#                         'QG_HOSTID': QGHost,
#                         'LAST_SCAN_DATETIME': LastScanDate,
#                         'OS_CPE': OsCpe,
#                         'LAST_VM_SCANNED_DATE': LastVmScanDate,
#                         'LAST_VM_SCANNED_DURATION': LastAuthScanDuration,
#                         'LAST_VM_AUTH_SCANNED_DATE': LastAuthScanDate,
#                         'LAST_VM_AUTH_SCANNED_DURATION': LastAuthScanDuration,
#                         'LAST_PC_SCANNED_DATE' : LastPcScanDate,
#                         'QID' : myCSV.iloc[index]['QID'],
#                         'TYPE' :myCSV.iloc[index]['Type'] ,
#                         'PORT' : myCSV.iloc[index]['Port']	,
#                         'PROTOCOL' : myCSV.iloc[index]['Protocol'],
#                         'FQDN' : myCSV.iloc[index]['FQDN']	,
#                         'SSL'	: myCSV.iloc[index]['SSL'],
#                         'INSTANCE' : myCSV.iloc[index]['Instance'],
#                         'STATUS' : myCSV.iloc[index]['Status'],
#                         'SEVERITY' : myCSV.iloc[index]['Severity'],
#                         'FIRST_FOUND_DATETIME' : myCSV.iloc[index]['First Found Datetime'],
#                         'LAST_FOUND_DATETIME' : myCSV.iloc[index]['Last Found Datetime'],
#                         'LAST_TEST_DATETIME' : myCSV.iloc[index]['Last Test Datetime'],
#                         'LAST_UPDATE_DATETIME' : myCSV.iloc[index]['Last Update Datetime'],
#                         'LAST_FIXED_DATETIME' : myCSV.iloc[index]['Last Fixed Datetime'],
#                         'RESULTS' : myCSV.iloc[index]['Results'],
#                         'IGNORED' : myCSV.iloc[index]['Ignored'],
#                         'DISABLED' : myCSV.iloc[index]['Disabled'],
#                         'TIMES_FOUND' : myCSV.iloc[index]['Times Found'],
#                         'SERVICE' : myCSV.iloc[index]['Service'],
#                         'LAST_PROCESSED_DATETIME': myCSV.iloc[index]['Last Processed Datetime']
#                     })
#                     myCSV.iloc[index]['Host ID'] = HostID
#                     print(myCSV.iloc[index])
#                     index +=1
#                 elif(index == len(myCSV)-1):
#                     myCSV.iloc[index]['Host ID'] = HostID
#                     rows.append ({
#                         'SCANDATEFORSQL' : ScanDateforSQL,
#                         'HOST_ID': HostID,
#                         'IP_ADDRESS': IpAddress,
#                         'TRACKING_METHOD': TrackingMethod,
#                         #'NETWORK_ID': NetworkID,
#                         'OPERATING_SYSTEM': OS,
#                         'DNS_NAME': Dns,
#                         'NETBIOS_NAME': Netbios,
#                         'QG_HOSTID': QGHost,
#                         'LAST_SCAN_DATETIME': LastScanDate,
#                         'OS_CPE': OsCpe,
#                         'LAST_VM_SCANNED_DATE': LastVmScanDate,
#                         'LAST_VM_SCANNED_DURATION': LastAuthScanDuration,
#                         'LAST_VM_AUTH_SCANNED_DATE': LastAuthScanDate,
#                         'LAST_VM_AUTH_SCANNED_DURATION': LastAuthScanDuration,
#                         'LAST_PC_SCANNED_DATE' : LastPcScanDate,
#                         'QID' : myCSV.iloc[index]['QID'],
#                         'TYPE' :myCSV.iloc[index]['Type'] ,
#                         'PORT' : myCSV.iloc[index]['Port']	,
#                         'PROTOCOL' : myCSV.iloc[index]['Protocol'],
#                         'FQDN' : myCSV.iloc[index]['FQDN']	,
#                         'SSL'	: myCSV.iloc[index]['SSL'],
#                         'INSTANCE' : myCSV.iloc[index]['Instance'],
#                         'STATUS' : myCSV.iloc[index]['Status'],
#                         'SEVERITY' : myCSV.iloc[index]['Severity'],
#                         'FIRST_FOUND_DATETIME' : myCSV.iloc[index]['First Found Datetime'],
#                         'LAST_FOUND_DATETIME' : myCSV.iloc[index]['Last Found Datetime'],
#                         'LAST_TEST_DATETIME' : myCSV.iloc[index]['Last Test Datetime'],
#                         'LAST_UPDATE_DATETIME' : myCSV.iloc[index]['Last Update Datetime'],
#                         'LAST_FIXED_DATETIME' : myCSV.iloc[index]['Last Fixed Datetime'],
#                         'RESULTS' : myCSV.iloc[index]['Results'],
#                         'IGNORED' : myCSV.iloc[index]['Ignored'],
#                         'DISABLED' : myCSV.iloc[index]['Disabled'],
#                         'TIMES_FOUND' : myCSV.iloc[index]['Times Found'],
#                         'SERVICE' : myCSV.iloc[index]['Service'],
#                         'LAST_PROCESSED_DATETIME': myCSV.iloc[index]['Last Processed Datetime']
#                     })
#                     print(myCSV.iloc[index])
#                     break

    
                
             




