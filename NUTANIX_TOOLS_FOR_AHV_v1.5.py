
##############################################################################
#                                                         					 #
# SCRIPT NUTANIX TOOLS FOR AHV v1.5                                          #
# PYTHON 3.6                                                                 #
# Testing on AOS , 5.8.x, 5.9.x, 5.10.x                                      #                       
# David Lira, dlira96@gmail.com                                              #
##############################################################################

import csv
import getpass
import json
import requests
import urllib3
import time
import datetime
import xlsxwriter
import sys
from tqdm import *
 
version_soft = 'Nutanix tools for AHV v1.5' 
print(version_soft)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
date_time = time.strftime('%d_%m_%Y_%H_%M')
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 

##LOGIN SECURE PRISM ELEMENT
ip_pe = input("Prism-Element-IP: ")
url = ('https://' + ip_pe +':9440')
username = input("Username: ")
password = getpass.getpass()

##LOGIN NO SECURE PRISM ELEMENT
#ip_pe = '10.26.1.2'
#url = ('https://' + ip_pe +':9440')
#username = 'admin'
#password = 'Pass1010.,'

###Folder or directory
#directory = "C:/Users/ext_fecastilloc/Desktop/NTNX SCRIPT/"
directory = "/home/sertechno.local/dlira/Desktop/"

## API REQUEST V1 AND V2
TIMEOUT = 15

try:
	pe_vm_info = requests.get(url + '/PrismGateway/services/rest/v2.0/vms/?include_vm_disk_config=true&include_vm_nic_config=true', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_cluster_info = requests.get(url + '/PrismGateway/services/rest/v2.0/cluster/', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_network = requests.get(url + '/PrismGateway/services/rest/v2.0/networks/', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_container = requests.get(url + '/api/nutanix/v2.0/storage_containers/', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_host = requests.get(url + '/PrismGateway/services/rest/v2.0/hosts/', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_vmdisk = requests.get(url + '/PrismGateway/services/rest/v2.0/virtual_disks/', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_vgroup = requests.get(url + '/PrismGateway/services/rest/v2.0/volume_groups/?include_disk_size=true', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_ha = requests.get(url + '/api/nutanix/v2.0/ha/', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_image = requests.get(url + '/PrismGateway/services/rest/v2.0/images/?include_vm_disk_sizes=true', auth=(username, password), verify=False, timeout=TIMEOUT)
	pe_resilency = requests.get(url + '/PrismGateway/services/rest/v1/cluster/domain_fault_tolerance_status', auth=(username, password), verify=False, timeout=TIMEOUT)
except Exception as v:
		print(f"Error: {v}")
		print('Login Failed to API V2, Bad Password , Bad IP/FQDN Prism Element or networks problems. Run again the script')
		time.sleep(2)
		sys.exit()	

if  (pe_vm_info.status_code == requests.codes.ok
	and pe_cluster_info.status_code == requests.codes.ok
	and pe_network.status_code == requests.codes.ok
	and pe_container.status_code == requests.codes.ok
	and pe_host.status_code == requests.codes.ok
	and pe_vmdisk.status_code == requests.codes.ok
	and pe_vgroup.status_code == requests.codes.ok
	and pe_ha.status_code == requests.codes.ok
	and pe_image.status_code == requests.codes.ok
	and pe_resilency.status_code == requests.codes.ok):
	pe_success_login = 100
	print('Login Succesfully API V1 and V2 on Prism Element')
	time.sleep(2)
else:
	print('Login Failed to API V1 or V2, Bad Password , Bad IP/FQDN Prism Element or networks problems. Run the script again')
	sys.exit()

## API REQUEST V3 WITH SESSION ON PRISM CENTRAL
prRed('\nINFO: The Prism Central must manage the selected prism element.\n')


try:
	confirm= None
	while confirm not in ('y','n'):
		confirm = input("Do you want Prism Central info('y' , 'n') ")
		if confirm in "n":
			print('\nNo prism central info selected\n')
			#return
		elif confirm in "y":
			print('\nPrism central info selected\n')
			samepass= None
			pc_ip = input("Prism-Central-IP: ")
			while samepass not in ('y','n'):
				samepass = input("Prism Central has same user/password Prism Element?('y' , 'n'):")
				if samepass in "n":
					print('LOGIN PRISM CENTRAL')
					###################################################
					##SECURE LOGIN PRISM CENTRAL
					pc_url = ('https://' + pc_ip +':9440')
					pc_username = input("Username: ")
					pc_password = getpass.getpass()
					###################################################
                    ###################################################
					##NO SECURE LOGIN PRISM CENTRAL
					#pc_url = ('https://' + pc_ip +':9440')
					#pc_username = 'User'
					#pc_password = 'Password'
					###################################################
				elif samepass in "y":
					pc_url = ('https://' + pc_ip +':9440')
					pc_username = username
					pc_password = password
				else:
					print("You should enter either \"y\" or \"n\".")
			##NO SECURE LOGIN PRISM CENTRAL
			#pc_ip = '10.26.1.15'
			#pc_url = ('https://' + pc_ip +':9440')
			#pc_username = 'admin'
			#v = 'Pass1010.,'
			################################
			print('\n##########################################')
			print ('Prism Central URL', pc_url)
			print('##########################################')
			session = requests.Session()
			session.auth = (pc_username,pc_password)
			session.verify = False
			session.headers.update({'Content-Type': 'application/json; charset = utf-8'})
			session.headers.update({'Accept': 'application/json'})
			###PRISM CENTRAL VM INFO
			vminfo='{"kind": "vm","offset": 0,"length": 1}'
			pc_vm_info = session.post(pc_url + '/api/nutanix/v3/vms/list',vminfo)
			#print(central_vm_info.json())
			if pc_vm_info.status_code == requests.codes.ok:
				print('Login Succesfully API V3 on Prism Central')
				time.sleep(2)
		else:
			print("You should enter either \"y\" or \"n\".")

except Exception as e:
	print('Login Failed to API V2, Bad Password , Bad IP/FQDN Prism Central or networks problems. Run again the script')
	print(f"Error: {e}")
	time.sleep(2)
	sys.exit()	

###PRISM ELEMENT
##API_DATA:CLUSTER,VMS,HARDWARE,NETWORKING

if  pe_success_login == 100: 
      ##CLUSTER
    if pe_cluster_info.status_code == requests.codes.ok:    
        out_json = pe_cluster_info.json()
        raw_cluster =  out_json
        #print(raw_cluster)
        #print('name=',raw_cluster)
        cluster_name= raw_cluster['name']
        timezoneclu= raw_cluster['timezone']
        storagetype= raw_cluster['storage_type']
        numnodesclu= raw_cluster['num_nodes']
        nameserver= raw_cluster['name_servers']
        cluster_rf= raw_cluster['cluster_redundancy_state']['current_redundancy_factor']
        #print('replication_factor: ', cluster_rf)
        #print(nameserver)
        ntpserver= raw_cluster['ntp_servers']
        print('Cluster Name :',cluster_name)
        versionaos=(raw_cluster['version'])
        print('Version AOS :',versionaos)
        versionncc=raw_cluster['ncc_version']
        #print('Version NCC :',versionncc)
        subnetcluster=raw_cluster['external_subnet']
        clusterip=raw_cluster['cluster_external_ipaddress']
        clusterdataip=raw_cluster['cluster_external_data_services_ipaddress']

    ##NETWORK
    if pe_network.status_code == requests.codes.ok:    
        out_json = pe_network.json()
        raw_network = out_json
        #print(raw_network)    
        vlan_ent = [(x['name'], x['vlan_id'], x['uuid']) for x in raw_network['entities']]
        #print('NETWORK',vlan_ent)
    
    ##CONTAINER
    if pe_container.status_code == requests.codes.ok:
        out_json = pe_container.json()
        raw_container = out_json
        #print(raw_network)    
        container = [(x['name'], x.get('storage_container_uuid', '-'), x.get('max_capacity', '-'), x.get('replication_factor', '-'), x.get('erasure_code', '-'), x.get('on_disk_dedup', '-'), x.get('compression_enabled', '-'), x['usage_stats']) for x in raw_container['entities']]
        #print('container',container)
    
    ##HOST AHV
    if pe_host.status_code == requests.codes.ok:
        out_json = pe_host.json()
        raw_host = out_json
        #print(raw_host)    
        ahvhost = [(x['uuid'], x.get('name', '-'), x.get('hypervisor_address', '-'), x.get('serial', '-'), x.get('block_serial', '-'), x.get('block_model_name', '-'), x.get('cpu_model', '-'), x['num_cpu_cores'], x['num_cpu_threads'], x['num_cpu_sockets'], x['memory_capacity_in_bytes'], x['hypervisor_full_name'], x['num_vms'], x['is_degraded'], x['host_in_maintenance_mode'], x['ipmi_address'], x['state'],x['controller_vm_backplane_ip']) for x in raw_host['entities']]
        #print('raw_host')
    
    ##VM INFO
    if pe_vm_info.status_code == requests.codes.ok:    
        out_json = pe_vm_info.json()
        vminfo = out_json['entities']
        #print(json.dumps(out_json, sort_keys=True, indent=4))
        entities = [(x['name'], x['uuid'], x['power_state'], x.get('host_uuid', '-'), x['vm_nics'], x['num_cores_per_vcpu'], x['num_vcpus'], x['timezone'], x['vm_disk_info'],x['memory_mb'],x.get('description', '-')) for x in out_json['entities']]
        metadata = out_json['metadata']
        num_vm_cluster=(metadata['grand_total_entities'])
        #print(num_vm_cluster)     
    
    ##VDISK
    if pe_vmdisk.status_code == requests.codes.ok:
        out_json = pe_vmdisk.json()
        raw_vdisk = out_json    
        vdisk = [(x['attached_vmname'], x['disk_address'], x['disk_capacity_in_bytes'], x['storage_container_uuid'], x.get('flash_mode_enabled', '-'), x['nutanix_nfsfile_path'], x['attached_volume_group_id'], x['uuid']) for x in raw_vdisk['entities']]
        #print(vdisk)
    
    ##VG
    if pe_vgroup.status_code == requests.codes.ok:
        out_json = pe_vgroup.json()
        raw_vg = out_json    
        vg = [(x['uuid'], x['name'], x['disk_list']) for x in raw_vg['entities']]

    ##HA
    if pe_ha.status_code == requests.codes.ok:
        out_json = pe_ha.json()
        ha = out_json    
        failover_en = (ha['failover_enabled'])
        reservation = (ha['reservation_type'])
        host_tolerate = (ha['num_host_failures_to_tolerate'])
        ha_state = (ha['ha_state'])

    ##RESILENCY DISK
    if pe_resilency.status_code == requests.codes.ok:
    	out_json_resilency = pe_resilency.json()
    	#print(out_json)


    ##IMAGE
    if pe_image.status_code == requests.codes.ok:
        out_json = pe_image.json()
        image = out_json['entities']
              
    ###EXCEL
    
    ##WORKBOOK
    if confirm == 'y':
    	workbook = xlsxwriter.Workbook(directory + 'NTNX_VM_INFO_PE_PC' + '(' + cluster_name + ')' + '_DATE_' + '('+  date_time + 'HRS' + ')' + '.xlsx')
    else:
    	workbook = xlsxwriter.Workbook(directory + 'NTNX_VM_INFO_PE_' + '(' + cluster_name + ')' + '_DATE_' + '('+  date_time + 'HRS' + ')' + '.xlsx')
    worksheet0 = workbook.add_worksheet('SUMMARY')
    worksheet1 = workbook.add_worksheet('VM INFO')
    worksheet2 = workbook.add_worksheet('VM DISK INFO')
    worksheet3 = workbook.add_worksheet('VM NETWORK')
    worksheet4 = workbook.add_worksheet('STORAGE CONTAINER')
    worksheet5 = workbook.add_worksheet('HOST AHV')
    worksheet6 = workbook.add_worksheet('VOLUME GROUP')
    worksheet7 = workbook.add_worksheet('VDISK INFO')
    worksheet8 = workbook.add_worksheet('IMAGE')
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1,'font_color': 'red','bg_color': 'black'})
    boldcell = workbook.add_format({'align': 'center'}) 
    
    # Data headers.
    worksheet0.write('A1', 'CLUSTER NAME', bold)
    worksheet0.write('A2', 'CLUSTER VERSION', bold)
    worksheet0.write('A3', 'CLUSTER TIMEZONE', bold)
    worksheet0.write('A4', 'CLUSTER DNS', bold)
    worksheet0.write('A5', 'CLUSTER NTP', bold)
    worksheet0.write('A6', 'CLUSTER N°NODES', bold)
    worksheet0.write('A7', 'CLUSTER STORAGE TYPE', bold)
    worksheet0.write('A8', 'CLUSTER IP', bold)
    worksheet0.write('A9', 'CLUSTER DATA SERVICE IP', bold)
    worksheet0.write('A10', 'CLUSTER REDUNDANCY FACTOR', bold)
    worksheet0.write('A11', 'TOTAL VM', bold)
    worksheet0.write('A12', 'HA ENABLED', bold)
    worksheet0.write('A13', 'HA RESERVATION', bold)
    worksheet0.write('A14', 'HA HOST TOLERATE', bold)
    worksheet0.write('A15', 'HA STATE', bold)
    worksheet0.write('A16', 'RESILIENCY STATUS LEVEL', bold)
    worksheet0.write('A17', 'N°DISK CAN BE FAIL ON METADATA', bold)
    worksheet0.write('A18', 'DISK IS REBUILDING ', bold)
    worksheet0.write('A19', 'N°DISK CAN BE FAIL ON ERASURE_CODE_STRIP_SIZE', bold)
    worksheet0.write('A20', 'DISK IS REBUILDING ', bold)
    worksheet0.write('A21', 'N°DISK CAN BE FAIL ON EXTENT_GROUPS', bold)
    worksheet0.write('A22', 'DISK IS REBUILDING ', bold)
    worksheet0.write('A23', 'N°DISK CAN BE FAIL ON OPLOG', bold)
    worksheet0.write('A24', 'DISK IS REBUILDING ', bold)
    worksheet0.write('A25', 'DATE', bold)
    worksheet1.write('A1', 'Cluster', bold)
    worksheet1.write('B1', 'AOS version', bold)
    worksheet1.write('C1', 'NCC version', bold)
    worksheet1.write('D1', 'Subnet Cluster', bold)
    worksheet1.write('E1', 'VM UUID', bold)
    worksheet1.write('F1', 'VM Name', bold)
    worksheet1.write('G1', 'Host_uuid', bold)
    worksheet1.write('H1', 'Host_Name', bold)
    worksheet1.write('I1', 'Power_state', bold)
    worksheet1.write('J1', 'Ip_address', bold)
    worksheet1.write('K1', 'Mac_address', bold)
    worksheet1.write('L1', 'Is_connected', bold)
    worksheet1.write('M1', 'Network_UUID', bold)
    worksheet1.write('N1', 'VLAN NAME', bold)
    worksheet1.write('O1', 'Num_cores_per_vcpu', bold)
    worksheet1.write('P1', 'Num_vcpus', bold)
    worksheet1.write('Q1', 'Memory in MB', bold)
    worksheet1.write('R1', 'Timezone', bold)
    worksheet1.write('S1', 'Description', bold)
    if confirm == 'y':
        worksheet1.write('T1', 'Project', bold)
        worksheet1.write('U1', 'NGT State', bold)
        worksheet1.write('V1', 'NGT Install status', bold)
        worksheet1.write('W1', 'NGT Version', bold)
        worksheet1.write('X1', 'NGT Reachable', bold)
        worksheet1.write('Y1', 'NGT OS', bold)
        worksheet1.write('Z1', 'VM CREATION TIME', bold)
    worksheet2.write('A1', 'VM NAME', bold)
    worksheet2.write('B1', 'VM UUID', bold)
    worksheet2.write('C1', 'DISK INTERFACE', bold)
    worksheet2.write('D1', 'DISK INTERFACE LABEL', bold)
    worksheet2.write('E1', 'DISK INDEX', bold)
    worksheet2.write('F1', 'DISK VMDISK/VOLUME GROUP', bold)
    worksheet2.write('G1', 'VDISK UUID', bold)
    worksheet2.write('H1', 'VDISK SIZE IN GB', bold)
    worksheet2.write('I1', 'VDISK ON STORAGE CONTAINER UUID', bold)
    worksheet2.write('J1', 'VDISK ON STORAGE NAME', bold)
    worksheet2.write('K1', 'VOLUME GROUP UUID', bold)
    worksheet2.write('L1', 'VOLUME GROUP NAME', bold)
    worksheet2.write('M1', 'VM FLASH MODE', bold)
    worksheet2.write_comment('M1', 'IF CLUSTER IS FULL SSD THIS OPTION NOT´S APPLY')
    worksheet2.write('N1', 'CDROM', bold)
    worksheet2.write('O1', 'CDROM ISO MOUNTED', bold)
    worksheet3.write('A1', 'UUID', bold)
    worksheet3.write('B1', 'Network Name', bold)
    worksheet3.write('C1', 'Vlan ID', bold)
    worksheet4.write('A1', 'UUID', bold)
    worksheet4.write('B1', 'Name', bold)
    worksheet4.write('C1', 'Used Space Bytes', bold)
    worksheet4.write('D1', 'Used Space GB', bold)
    worksheet4.write('E1', 'Max_capacity_in_Bytes', bold)
    worksheet4.write('F1', 'Max_capacity_in_GB', bold)
    worksheet4.write('G1', 'Replication_factor', bold)
    worksheet4.write('H1', 'erasure_code', bold)
    worksheet4.write('I1', 'on_disk_dedup', bold)
    worksheet4.write('J1', 'compression_enabled', bold)
    worksheet5.write('A1', 'UUID', bold)
    worksheet5.write('B1', 'NAME', bold)
    worksheet5.write('C1', 'HYPERVISOR IP', bold)
    worksheet5.write('D1', 'SERIAL NODE', bold)
    worksheet5.write('E1', 'CVM IP', bold)
    worksheet5.write('F1', 'SERIAL BLOCK', bold)
    worksheet5.write('G1', 'BLOCK MODEL', bold)
    worksheet5.write('H1', 'CPU MODEL', bold)
    worksheet5.write('I1', 'Nro CPU', bold)
    worksheet5.write('J1', 'Nro Threads', bold)
    worksheet5.write('K1', 'Nro SOCKET', bold)
    worksheet5.write('L1', 'Memory in GB', bold)
    worksheet5.write('M1', 'HYPERVISOR VERSION', bold)
    worksheet5.write('N1', 'Nro VM', bold)
    worksheet5.write('O1', 'DEGRADED', bold)
    worksheet5.write('P1', 'MAINTENANCE MODE', bold)
    worksheet5.write('Q1', 'IPMI IP', bold)
    worksheet5.write('R1', 'NODE STATE', bold)
    worksheet6.write('A1', 'UUID', bold)
    worksheet6.write('B1', 'NAME', bold)
    worksheet6.write('C1', 'VMDISK UUID', bold)
    worksheet6.write('D1', 'VMDISK SIZE GB', bold)
    worksheet6.write('E1', 'FLASH MODE', bold)
    worksheet6.write_comment('E1', 'IF CLUSTER IS FULL SSD THIS OPTION NOT´S APPLY')
    worksheet7.write('A1', 'VM NAME', bold) 
    worksheet7.write('B1', 'DEVICE ADDRESS', bold) 
    worksheet7.write('C1', 'VMDISK UUID', bold) 
    worksheet7.write('D1', 'DEVICE IN GB', bold) 
    worksheet7.write('E1', 'StorateCont UUID', bold) 
    worksheet7.write('F1', 'StorateCont Name', bold)
    worksheet7.write('G1', 'Ndfs_filepath', bold) 
    worksheet8.write('A1', 'Name', bold)
    worksheet8.write('B1', 'Image Type', bold)
    worksheet8.write('C1', 'Image Size in GB', bold)
    worksheet8.write('D1', 'Image State', bold)
    worksheet8.write('E1', 'created_time_in_usecs', bold)
    worksheet1.autofilter('A1:Y1')
    worksheet2.autofilter('A1:G1')
    worksheet3.autofilter('A1:C1')
    worksheet4.autofilter('A1:J1')
    worksheet5.autofilter('A1:G1')
    worksheet6.autofilter('A1:D1')
    worksheet7.autofilter('A1:D1')
    
    #SUMMARY
    

    row=0
    today = datetime.date.today()
    worksheet0.write(row ,   1 ,cluster_name, boldcell)
    worksheet0.write(row+1 , 1 ,versionaos, boldcell)
    worksheet0.write(row+2 , 1 ,timezoneclu, boldcell)
    worksheet0.write(row+3 , 1 ,str(nameserver), boldcell)
    worksheet0.write(row+4 , 1 ,str(ntpserver), boldcell)
    worksheet0.write(row+5 , 1 ,numnodesclu, boldcell)
    worksheet0.write(row+6 , 1 ,storagetype, boldcell)
    worksheet0.write(row+7 , 1 ,clusterip, boldcell)
    worksheet0.write(row+8 , 1 ,clusterdataip, boldcell)
    worksheet0.write(row+9 , 1 ,cluster_rf, boldcell)
    worksheet0.write(row+10 , 1 ,num_vm_cluster, boldcell)
    worksheet0.write(row+11, 1 ,failover_en, boldcell)
    worksheet0.write(row+12, 1 ,reservation, boldcell)
    worksheet0.write(row+13 , 1 ,host_tolerate, boldcell)
    worksheet0.write(row+14 , 1 ,ha_state, boldcell)
    for resilency_raw in out_json_resilency:
    	domain=resilency_raw['domainType']
    	if 'METADATA' in resilency_raw['componentFaultToleranceStatus'].keys():
    		if 'numberOfFailuresTolerable' in resilency_raw['componentFaultToleranceStatus']['METADATA'].keys():
    			numberofdiskfail = resilency_raw['componentFaultToleranceStatus']['METADATA']['numberOfFailuresTolerable']
    			if 'underComputation' in resilency_raw['componentFaultToleranceStatus']['METADATA'].keys():
    				disk_rebuild = resilency_raw['componentFaultToleranceStatus']['METADATA']['underComputation']
    				if resilency_raw['domainType'] == 'DISK':
    					worksheet0.write(row+15 , 1 ,resilency_raw['domainType'], boldcell)
    					worksheet0.write(row+16 , 1 ,numberofdiskfail, boldcell)
    					worksheet0.write(row+17 , 1 ,disk_rebuild, boldcell)
    	if 'ERASURE_CODE_STRIP_SIZE' in resilency_raw['componentFaultToleranceStatus'].keys():	
    		if 'numberOfFailuresTolerable' in resilency_raw['componentFaultToleranceStatus']['ERASURE_CODE_STRIP_SIZE'].keys():
    			numberofdiskfail = resilency_raw['componentFaultToleranceStatus']['ERASURE_CODE_STRIP_SIZE']['numberOfFailuresTolerable']
    			if 'underComputation' in resilency_raw['componentFaultToleranceStatus']['ERASURE_CODE_STRIP_SIZE'].keys():
    				disk_rebuild = resilency_raw['componentFaultToleranceStatus']['ERASURE_CODE_STRIP_SIZE']['underComputation']
    				if resilency_raw['domainType'] == 'DISK':
    					worksheet0.write(row+18 , 1 ,numberofdiskfail, boldcell)
    					worksheet0.write(row+19 , 1 ,disk_rebuild, boldcell)
    	if 'EXTENT_GROUPS' in resilency_raw['componentFaultToleranceStatus'].keys():	
    		if 'numberOfFailuresTolerable' in resilency_raw['componentFaultToleranceStatus']['EXTENT_GROUPS'].keys():
    			numberofdiskfail = resilency_raw['componentFaultToleranceStatus']['EXTENT_GROUPS']['numberOfFailuresTolerable']
    			if 'underComputation' in resilency_raw['componentFaultToleranceStatus']['EXTENT_GROUPS'].keys():
    				disk_rebuild = resilency_raw['componentFaultToleranceStatus']['EXTENT_GROUPS']['underComputation']
    				if resilency_raw['domainType'] == 'DISK':
    					worksheet0.write(row+20 , 1 ,numberofdiskfail, boldcell)
    					worksheet0.write(row+21 , 1 ,disk_rebuild, boldcell)
    	if 'OPLOG' in resilency_raw['componentFaultToleranceStatus'].keys():	
    		if 'numberOfFailuresTolerable' in resilency_raw['componentFaultToleranceStatus']['OPLOG'].keys():
    			numberofdiskfail = resilency_raw['componentFaultToleranceStatus']['OPLOG']['numberOfFailuresTolerable']
    			if 'underComputation' in resilency_raw['componentFaultToleranceStatus']['OPLOG'].keys():
    				disk_rebuild = resilency_raw['componentFaultToleranceStatus']['OPLOG']['underComputation']
    				if resilency_raw['domainType'] == 'DISK':
    					worksheet0.write(row+22 , 1 ,numberofdiskfail, boldcell)
    					worksheet0.write(row+23 , 1 ,disk_rebuild, boldcell)
    worksheet0.write(row+24 , 1 ,today.strftime('Running on %d, %b %Y'), boldcell)

    #VM INFO PRINT
    row = 0
    raw = 1 
    progress_in = 0
    for vm in entities:  ### VM WITH NIC
    	for nic in vm[4]:
            row = row + 1
            raw = raw + 1
            print('Get info from ,', vm[0])
            namevlan = "="+"VLOOKUP"+"(M"+(str(raw))+",'VM NETWORK'!$A$2:$B$1000000,COLUMN('VM NETWORK'!B:B)-COLUMN('VM NETWORK'!$A$2:$B$1000000)+1,0)"
            #excel_if = "="+"IF("+"G"+(str(raw))+"="+'"-"'+","+'"VM OFF"'+","
            namehost = "="+"IF("+"G"+(str(raw))+"="+'"-"'+","+'"-"'+","+"VLOOKUP"+"(G"+(str(raw))+",'HOST AHV'!$A$2:$B$1000000,COLUMN('HOST AHV'!B:B)-COLUMN('HOST AHV'!$A$2:$B$1000000)+1,0))"
            col = 0
            if confirm == 'y':
            	pc_vm_single= session.get(pc_url + '/api/nutanix/v3/vms/'+vm[1], verify=False, timeout=TIMEOUT)
            	pc_vm_single_raw = (pc_vm_single.json())
            	if 'metadata' in pc_vm_single_raw.keys():
            		metadata = 100
            		if 'project_reference' in pc_vm_single_raw['metadata'].keys():
            			pc_vm_single_project= pc_vm_single_raw['metadata']['project_reference']['name']
            			proyect_reference= 101
            		if 'creation_time' in pc_vm_single_raw['metadata'].keys():
            			pc_vm_single_creation = pc_vm_single_raw['metadata']['creation_time']
            			pc_vm_single_creation_reference= 102
            worksheet1.write(row , col , cluster_name)
            worksheet1.write(row , col +1 ,versionaos)
            worksheet1.write(row , col +2 ,versionncc)
            worksheet1.write(row , col +3 ,subnetcluster)
            worksheet1.write(row , col +4 ,vm[1])
            worksheet1.write(row , col +5 ,vm[0])
            worksheet1.write(row , col +6 ,vm[3])
            worksheet1.write_formula(row , col +7 ,namehost)
            worksheet1.write(row , col +8 ,vm[2])
            worksheet1.write(row , col +9 ,nic.get('ip_address', '-'))
            worksheet1.write(row , col +10 ,nic.get('mac_address', '-'))
            worksheet1.write(row , col +11 ,nic.get('is_connected', '-'))
            worksheet1.write(row , col +12 ,nic.get('network_uuid', '-'))
            worksheet1.write_formula(row , col +13 , namevlan )
            worksheet1.write(row , col +14 ,vm[5])
            worksheet1.write(row , col +15 ,vm[6])
            worksheet1.write(row , col +16 ,str(vm[9]))
            worksheet1.write(row , col +17 ,vm[7])
            worksheet1.write(row , col +18 ,vm[10])
            if confirm == 'y':
            	if metadata == 100 and proyect_reference == 101:
            		worksheet1.write(row , col +19 ,pc_vm_single_project)
            	else:
            		worksheet1.write(row , col +19 ,'-')
            	if 'guest_tools' in pc_vm_single_raw['status']['resources'].keys():
            		if 'ngt_state' in pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools'].keys(): 
            			pc_vm_guest_install= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['ngt_state']
            			worksheet1.write(row , col +21 ,pc_vm_guest_install)
            		else:
            			worksheet1.write(row , col +21 ,'no info')
            		pc_vm_guest_state= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['state']
            		pc_vm_guest_reachable= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['is_reachable']
            		worksheet1.write(row , col +20 ,pc_vm_guest_state)
            		if 'version' in pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools'].keys():
            			pc_vm_guest_version= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['version']
            			worksheet1.write(row , col +22 ,pc_vm_guest_version)
            		worksheet1.write(row , col +23 ,pc_vm_guest_reachable)
            		if 'guest_os_version' in pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools'].keys():
            			pc_vm_guest_os_version= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['guest_os_version']
            			worksheet1.write(row , col +24 ,pc_vm_guest_os_version)
            	else:
            		worksheet1.write(row , col +20 ,'DISABLED')
            		worksheet1.write(row , col +21 ,'Enable for check')
            		worksheet1.write(row , col +22 ,'-')
            		worksheet1.write(row , col +23 ,'-')
            		worksheet1.write(row , col +24 ,'-')
            	if pc_vm_single_creation_reference == 102:
            		worksheet1.write(row , col +25 ,pc_vm_single_creation)
            	else:
            		worksheet1.write(row , col +25 ,'-')
            progress_in = progress_in + 1
            for i in tqdm(range(progress_in)):
            	time.sleep(.0001)
    for vm in entities: ### VM WITH NO NIC
    	if not vm[4]: 
    		row = row + 1
    		raw = raw + 1
    		print('Get info from ,', vm[0])
    		namehost = "="+"IF("+"G"+(str(raw))+"="+'"-"'+","+'"-"'+","+"VLOOKUP"+"(G"+(str(raw))+",'HOST AHV'!$A$2:$B$1000000,COLUMN('HOST AHV'!B:B)-COLUMN('HOST AHV'!$A$2:$B$1000000)+1,0))"
    		if confirm == 'y':
    			pc_vm_single= session.get(pc_url + '/api/nutanix/v3/vms/'+vm[1], verify=False, timeout=TIMEOUT)
    			pc_vm_single_raw = (pc_vm_single.json())
    			if 'metadata' in pc_vm_single_raw.keys():
    				metadata = 100
    				if 'project_reference' in pc_vm_single_raw['metadata'].keys():
    					pc_vm_single_project= pc_vm_single_raw['metadata']['project_reference']['name']
    					proyect_reference= 101
    				if 'creation_time' in pc_vm_single_raw['metadata'].keys():
    					pc_vm_single_creation = pc_vm_single_raw['metadata']['creation_time']
    					pc_vm_single_creation_reference= 102
    		worksheet1.write(row , col , cluster_name)
    		worksheet1.write(row , col +1 ,versionaos)
    		worksheet1.write(row , col +2 ,versionncc)
    		worksheet1.write(row , col +3 ,subnetcluster)
    		worksheet1.write(row , col +4 ,vm[1])
    		worksheet1.write(row , col +5 ,vm[0])
    		worksheet1.write(row , col +6 ,vm[3])
    		worksheet1.write_formula(row , col +7 ,namehost)
    		worksheet1.write(row , col +8 ,vm[2])
    		worksheet1.write(row , col +9 ,'-')
    		worksheet1.write(row , col +10 ,'-')
    		worksheet1.write(row , col +11 ,'-')
    		worksheet1.write(row , col +12 ,'-')
    		worksheet1.write(row , col +13 , '-' )
    		worksheet1.write(row , col +14 ,vm[5])
    		worksheet1.write(row , col +15 ,vm[6])
    		worksheet1.write(row , col +16 ,str(vm[9]))
    		worksheet1.write(row , col +17 ,vm[7])
    		worksheet1.write(row , col +18 ,vm[10])
    		if confirm == 'y':
    			if metadata == 100 and proyect_reference == 101:
    				worksheet1.write(row , col +19 ,pc_vm_single_project)
    			else:
    				worksheet1.write(row , col +19 ,'-')
    			if 'guest_tools' in pc_vm_single_raw['status']['resources'].keys():
    				pc_vm_guest_install= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['ngt_state'] 
    				pc_vm_guest_state= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['state']
    				pc_vm_guest_reachable= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['is_reachable']
    				worksheet1.write(row , col +20 ,pc_vm_guest_state)
    				worksheet1.write(row , col +21 ,pc_vm_guest_install)
    				if 'version' in pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools'].keys():
    					pc_vm_guest_version= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['version']
    					worksheet1.write(row , col +22 ,pc_vm_guest_version)
    				worksheet1.write(row , col +23 ,pc_vm_guest_reachable)
    				if 'guest_os_version' in pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools'].keys():
    					pc_vm_guest_os_version= pc_vm_single_raw['status']['resources']['guest_tools']['nutanix_guest_tools']['guest_os_version']
    					worksheet1.write(row , col +24 ,pc_vm_guest_os_version)
    			else:
    				worksheet1.write(row , col +20 ,'DISABLED')
    				worksheet1.write(row , col +21 ,'Enable for check')
    				worksheet1.write(row , col +22 ,'-')
    				worksheet1.write(row , col +23 ,'-')
    				worksheet1.write(row , col +24 ,'-')
    			if pc_vm_single_creation_reference == 102:
    				worksheet1.write(row , col +25 ,pc_vm_single_creation)
    			else:
    				worksheet1.write(row , col +25 ,'-')
    		progress_in = progress_in + 1
    		for i in tqdm(range(progress_in)):
    			time.sleep(.0001)


    #VM DISK INFO PRINT
    row = 0
    raw = 1     
    for vm in entities:
        for disk in vm[8]:
            #print('disk=',disk)                           
            info=disk['disk_address']
            filepath='' 
            if 'source_disk_address' in disk.keys():
                if 'ndfs_filepath' in disk['source_disk_address'].keys():
                    filepath=disk['source_disk_address']['ndfs_filepath']
            volume_group=''
            if 'disk_address' in disk.keys():
                if 'volume_group_uuid' in disk['disk_address'].keys():
                	volume_group=disk['disk_address']['volume_group_uuid']
                else:
                    volume_group='-'
            row = row + 1
            raw = raw + 1
            col = 0
            vdisksize = "="+"IF("+"G"+(str(raw))+"="+'"-"'+","+'"-"'+","+"VLOOKUP"+"(G"+(str(raw))+",'VDISK INFO'!$C$2:$D$1000000,COLUMN('VDISK INFO'!D:D)-COLUMN('VDISK INFO'!$C$2:$D$1000000)+1,0))"
            scname = "="+"IF("+"G"+(str(raw))+"="+'"-"'+","+'"-"'+","+"VLOOKUP"+"(I"+(str(raw))+",'STORAGE CONTAINER'!$A$2:$B$1000000,COLUMN('STORAGE CONTAINER'!B:B)-COLUMN('STORAGE CONTAINER'!$A$2:$B$1000000)+1,0))"
            vgname = "="+"IF("+"K"+(str(raw))+"="+'""'+","+'"-"'+","+"VLOOKUP"+"(K"+(str(raw))+",'VOLUME GROUP'!$A$2:$B$1000000,COLUMN('VOLUME GROUP'!B:B)-COLUMN('VOLUME GROUP'!$A$2:$B$1000000)+1,0))"
            vgorvdisk = "="+"IF("+"G"+(str(raw))+"="+'"-"'+","+'"VOLUME GROUP"'+","+'"VMDISK")'
            worksheet2.write(row , col , vm[0])
            worksheet2.write(row , col +1 ,vm[1])
            worksheet2.write(row , col +2 ,info['device_bus'])
            worksheet2.write(row , col +3 ,info['disk_label'])
            worksheet2.write(row , col +4 ,info['device_index'])
            if volume_group == '-':
                if  info.get('vmdisk_uuid','-') == '-':
                    worksheet2.write(row , col +5 ,'CDROM')
                else:
                    worksheet2.write(row , col +5 ,'VDISK')
            else:
                worksheet2.write(row , col +5 ,'VG')
            worksheet2.write(row , col +6 ,info.get('vmdisk_uuid', '-'))
            worksheet2.write(row , col +7 ,vdisksize)
            worksheet2.write(row , col +8 ,disk.get('storage_container_uuid', '-'))
            worksheet2.write(row , col +9 ,scname)
            worksheet2.write(row , col +10 ,volume_group)
            if volume_group == '-':
                worksheet2.write(row , col +11 ,'-')
            else:
                worksheet2.write(row , col +11 ,vgname)
            worksheet2.write(row , col +12 ,disk.get('flash_mode_enabled', '-'))
            worksheet2.write(row , col +13 ,disk['is_cdrom'])
            worksheet2.write(row , col +14 ,disk.get('is_empty', '-'))
            #print(info['device_bus'])
    
    
    #NETWORK PRINT
    
    row = 0
    for network in vlan_ent:
        row = row + 1
        col = 0
        worksheet3.write(row , col ,network[2])
        worksheet3.write(row , col +1 ,network[0])
        worksheet3.write(row , col +2 ,network[1])
    
    ##STORAGE CONTAINER PRINT
    
    row = 0
    raw = 1
    for scontainer in container:
        row = row + 1
        raw = raw + 1
        col = 0
        form1 = '=E'+(str(raw))+'/1024'+'/1024'+'/1024' #Capacidad de Bytes a GB
        form2 = '=C'+(str(raw))+'/1024'+'/1024'+'/1024' #Capacidad de Bytes a GB
        #print(form1)
        worksheet4.write(row , col ,scontainer[1])
        worksheet4.write(row , col +1 ,scontainer[0])   
        worksheet4.write(row , col +2 ,(scontainer[7]['storage.usage_bytes']))
        worksheet4.write(row , col +3 , form2 )
        worksheet4.write(row , col +4 ,scontainer[2])
        worksheet4.write(row , col +5 , form1 )
        worksheet4.write(row , col +6 ,scontainer[3])
        worksheet4.write(row , col +7 ,scontainer[4])
        worksheet4.write(row , col +8 ,scontainer[5])
        worksheet4.write(row , col +9 ,scontainer[6])
    
    ##HOST AHV PRINT
    
    row = 0
    raw = 1
    for host in ahvhost:
        row = row + 1
        raw = raw + 1
        col = 0
        memory_gb = (host[10])/1024/1024/1024
        #print(memory_gb)
        worksheet5.write(row , col ,host[0])
        worksheet5.write(row , col +1 ,host[1])
        worksheet5.write(row , col +2 ,host[2])
        worksheet5.write(row , col +3 ,host[3])
        worksheet5.write(row , col +4 ,host[17])
        worksheet5.write(row , col +5 ,host[4])
        worksheet5.write(row , col +6 ,host[5])
        worksheet5.write(row , col +7 ,host[6])
        worksheet5.write(row , col +8 ,host[7])
        worksheet5.write(row , col +9 ,host[8])
        worksheet5.write(row , col +10 ,host[9])
        worksheet5.write(row , col +11 ,memory_gb)
        worksheet5.write(row , col +12 ,host[11])
        worksheet5.write(row , col +13 ,host[12])
        worksheet5.write(row , col +14 ,host[13])
        worksheet5.write(row , col +15 ,host[14])
        worksheet5.write(row , col +16 ,host[15])
        worksheet5.write(row , col +17 ,host[16])
    
    ##VG INFO RAW PRINT
    
    row = 0
    raw = 1
    for vgroup in vg:
        for volume in vgroup[2]:
            row = row + 1
            raw = raw + 1
            col = 0      
            worksheet6.write(row , col ,vgroup[0])
            worksheet6.write(row , col +1 ,vgroup[1])
            worksheet6.write(row , col +2 ,volume.get('vmdisk_uuid', '-'))
            worksheet6.write(row , col +3 ,'='+str(volume.get('vmdisk_size_mb', '-'))+'/1024')
            worksheet6.write(row , col +4 ,volume.get('flash_mode_enabled', 'FALSE'), boldcell)
    
    #VDISK INFO RAW PRINT
    
    raw = 1
    row = 0 
    #print(vdisk)
    for vmdisk in vdisk:
     if vmdisk[0] is not None:
      #print(vmdisk[2])
      row = row + 1
      raw = raw + 1
      col = 0
      containername= "="+"VLOOKUP"+"(E"+(str(raw))+",'STORAGE CONTAINER'!$A$2:$B$1000000,COLUMN('STORAGE CONTAINER'!B:B)-COLUMN('STORAGE CONTAINER'!$A$2:$B$1000000)+1,0)"
      vmsizegb= (vmdisk[2])/1024/1024/1024
      worksheet7.write(row , col ,vmdisk[0])
      worksheet7.write(row , col +1 ,vmdisk[1])
      worksheet7.write(row , col +2 ,vmdisk[7])
      worksheet7.write(row , col +3 ,vmsizegb)
      worksheet7.write(row , col +4 ,vmdisk[3])
      worksheet7.write(row , col +5 ,containername)
      worksheet7.write(row , col +6 ,vmdisk[5])
      worksheet7.write(row , col +7 ,vmdisk[6])

    ##IMAGE INFO PRINT
    
    row = 0
    col = 0
    for image_not_size in image:
        if not 'vm_disk_size' in image_not_size.keys():
            row = row + 1
            nameimage = image_not_size['name']
            image_type = image_not_size['image_type']
            image_state = image_not_size['image_state']
            created_time_in_usecs = image_not_size['created_time_in_usecs']     
            worksheet8.write(row , col ,nameimage)
            worksheet8.write(row , col +1 ,image_type)
            worksheet8.write(row , col +2 ,'-')
            worksheet8.write(row , col +3 ,image_state)
            worksheet8.write(row , col +4 ,created_time_in_usecs)
    
    for image_size in image:
        if 'vm_disk_size' in image_size.keys():
            nameimage1 = image_size['name']
            image_size1 = image_size['vm_disk_size']
            image_type1 = image_size['image_type']
            image_state1 = image_size['image_state']
            created_time_in_usecs1 = image_size['created_time_in_usecs']
            #print('NAME_2: ',nameimage1)
            row = row + 1
            worksheet8.write(row , col ,nameimage1)
            worksheet8.write(row , col +1 ,image_type1)
            worksheet8.write(row , col +2 ,'='+(str(image_size1)) +'/1024/1024/1024')
            worksheet8.write(row , col +3 ,image_state1)
            worksheet8.write(row , col +4 ,created_time_in_usecs1)
    
    workbook.close()
    
    if confirm == 'y':
    	namefile='\nNTNX_VM_INFO_PE_PC' + '(' + cluster_name + ')' + '_DATE_' + '('+  date_time + 'HRS' + ')' + '.xlsx'
    else:
    	namefile='\nNTNX_VM_INFO_PE_' + '(' + cluster_name + ')' + '_DATE_' + '('+  date_time + 'HRS' + ')' + '.xlsx'
    print('File :', namefile +' saved on ' + directory)
    def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
    #prRed('\nWarning:if the VM does not have a created NIC, it can not be displayed in the "VM INFO" tab.\n') ##FIXED V1.2
    print('Enjoy :)')
    time.sleep(5)




    

