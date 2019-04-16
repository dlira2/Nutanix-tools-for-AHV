
##############################################################################
#                                                         					 #
# SCRIPT NUTANIX TOOLS SWITCH LLDP FOR AHV, Beta v1.0                         #
# PYTHON 3.6                                                                 #
# Testing on AOS , 5.8.x, 5.9.x, 5.10.x                                      #                       
# David Lira, dlira96@gmail.com                                              #
##############################################################################

import paramiko
import sys
import tempfile
import time
import os
import datetime
import xlsxwriter
import subprocess
import getpass
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## CREATE TEMP FILE
temp = tempfile.NamedTemporaryFile(mode='w+t')
os.chmod(temp.name, 0o640)

##LOGIN SECURE PRISM ELEMENT
ip_pe = input("Prism-Element-IP: ")
url = ('https://' + ip_pe +':9440')
username = input("Username: ")
password = getpass.getpass()
print('')
print('Nutanix user Password:')
nutanix_user_pass = getpass.getpass()

##LOGIN NO SECURE PRISM ELEMENT
#ip_pe = '10.26.1.2'
#url = ('https://' + ip_pe +':9440')
#username = 'admin'
#password = 'Pass1010.,'
#nutanix_user_pass = "nutanix/4u"

##WORKBOOK
directory = "/home/sertechno.local/dlira/Desktop/"
date_time = time.strftime('%d_%m_%Y_%H_%M')
workbook = xlsxwriter.Workbook(directory + 'NTNX_PORT_LLDP_INFO_'+ '_DATE_' + '('+  date_time + 'HRS' + ')' + '.xlsx')
worksheet0 = workbook.add_worksheet('SUMMARY')

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': 1,'font_color': 'red','bg_color': 'black'})
boldcell = workbook.add_format({'align': 'center'})
worksheet0.write('A1', 'HOSTNAME', bold)
worksheet0.write('B1', 'SWITCH NAME', bold)
worksheet0.write('C1', 'SWITCH PORT', bold)
worksheet0.write('D1', 'AHV PORT', bold)

###FORMAT
pe_host = requests.get(url + '/PrismGateway/services/rest/v2.0/hosts/', auth=(username, password), verify=False)
row = 0
if pe_host.status_code == requests.codes.ok:
	out_json = pe_host.json()
	raw_host = out_json
	for hosts in raw_host['entities']:
		ahvhost = hosts['hypervisor_address']
		cvmhost = hosts['controller_vm_backplane_ip']
		ahvname = hosts['name']
		#SSH DETAILS ##
		SSH_ADDRESS = cvmhost
		SSH_USERNAME = "nutanix"

		## SSH BELOW ##
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_stdin = ssh_stdout = ssh_stderr = None
		try:
			print('Get info from AHV: ', ahvname)
			print('CVM IP:            ', cvmhost )
			ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=nutanix_user_pass)
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ssh root@192.168.5.1 /usr/sbin/lldpcli show neighbors details")
			#print(ssh_stdout.readlines())
			temp.writelines(ssh_stdout.readlines())
			temp.seek(0)
			## DATA FILTER ##
			SYSNAME_COMMAND = "cat "+temp.name+" | grep SysName | awk '{ print $2"+'","'+"}"+"'"
			INTERFACE_COMMAND = "cat "+temp.name+" | grep Interface | awk '{ print $2 }'"
			PORT_COMMAND = "cat "+temp.name+" | grep PortDescr | awk '{ print $2"+'","'+"}"+"'"
			SYSNAME = subprocess.check_output(SYSNAME_COMMAND, shell=True)
			INTERFACE = subprocess.check_output(INTERFACE_COMMAND, shell=True)
			PORT = subprocess.check_output(PORT_COMMAND, shell=True)
			col = 0
			row = row + 1
			worksheet0.write(row , col , ahvname)
			worksheet0.write(row , col +1 , SYSNAME.decode())
			worksheet0.write(row , col +2 , PORT.decode())
			worksheet0.write(row , col +3 , INTERFACE.decode())
		except Exception as e:
			sys.stderr.write("SSH connection error: {0}".format(e))

workbook.close()
