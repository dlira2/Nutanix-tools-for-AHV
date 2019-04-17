# Nutanix-tools-for-AHV v1.4
Data collector associated with the Nutanix AHV cluster and VM´s.

Script developed in python to collect the information of Prism Element with the option of being able to connect to a Prism Central to obtain the project to which each VM belongs. The code generates an Excel table with all the information of the Nutanix platform with AHV. Many searches within the script are using Excel formulas to avoid overuse of API and the collection is more faster. The script will consult if there is an instance of Prism Central and if the user wants to obtain such information by means of a confirmation. If "Y" is selected, it will recolect the Prism Central VM proyect info. when this option is selected it may take a longer time, because you must consult for each VM to which project it belongs. A "Progress Bar" indicator was added to see if the script is running or there is a problem.

Tested on AOS 5.5.x , 5.8.x , 5.9.x and 5.10.x

Requirements:

python 3.6 or higher.
Python Module :

     csv,
     getpass,
     json,
     requests,
     urllib3,
     time,
     datetime,
     xlsxwriter,
     sys,
     tqdm.

It is possible to execute connections "Safe" and not "Secure". to avoid placing IP and password repeatedly.

     -Prism Element secure connection, lines 28 to 32.
     -Prism Central secure connection, lines 100 to 102.
    
     IMPORTANT 1: the variable "directory" must be declared on line 42, there is an example for windows and linux.
     IMPORTANT 2: there is a variable named TIMEOUT which by default is 15 seconds. If there are problems of slowness or connection can modify this value according to the reality of each connection.

If you need help to running or any problem please contact me , dlira96@gmail.com.

INFORMATION COLLECTED BY THE SCRIPT :

-Sumarry Cluster:

     Cluster Name 
     Cluster Version
     Cluster Timezone
     Cluster DNS
     Cluster NTP
     Cluster Number of nodos
     Cluster Storage Type
     Cluster IP
     Cluster Data services IP
     Cluster Redundancy Factor
     Total VM
     HA enabled status
     HA reservation Status
     HA host tolerate
     HA state
     Date

-VM INFO:

     Cluster
     AOS
     NCC
     SUBNET
     VM UUID
     VM NAME
     HOST UUID
     HOST NAME
     POWER STATE
     IP ADDRESS
     MAC ADDRESS
     IS CONECCTED (NIC) NOTE : ONLY AVAILABLE FROM 5.9 OR LATER
     Network UUID
     Vlan Name
     Num core per cpu
     Num CPU
     Memory
     Timezone (hardware)
     Description
     Project NOTE : ONLY AVAILABLE IF OPTIONS PRISM CENTRAL IS SELECTED IN THE SCRIPT
     NGT STATUS : ONLY AVAILABLE IF OPTIONS PRISM CENTRAL IS SELECTED IN THE SCRIPT
     NGT INSTALL STATUS : ONLY AVAILABLE IF OPTIONS PRISM CENTRAL IS SELECTED IN THE SCRIPT
     NGT VERSION : ONLY AVAILABLE IF OPTIONS PRISM CENTRAL IS SELECTED IN THE SCRIPT
     NGT GUEST OS : ONLY AVAILABLE IF OPTIONS PRISM CENTRAL IS SELECTED IN THE SCRIPT
     VM CREATION TIME :ONLY AVAILABLE IF OPTIONS PRISM CENTRAL IS SELECTED IN THE SCRIPT
  
-VM DISK INFO:

     VM NAME
     VM UUID
     DISK INTERFACE
     DISK INTERFACE LABEL
     DISK INDEX
     DISK VMDISK/VOLUME GROUP
     VDISK UUID
     VDISK SIZE IN GB
     VDISK ON STORAGE CONTAINER UUID
     VDISK ON STORAGE NAME
     VOLUME GROUP UUID
     VOLUME GROUP NAME
     VM FLASH MODE
     CDROOM
     CDROOM ISO MOUNTED

-VM NETWORK:

     UUID
     Network Name
     Vlan ID

-STORAGE CONTAINER:

     UUID
     Name
     Used Space Bytes
     Used Space GB
     Max_capacity_in_Bytes
     Max_capacity_in_GB
     Replication_factor
     erasure_code
     on_disk_dedup
     compression_enabled
     
-HOST AHV :

     UUID
     NAME
     HYPERVISOR IP
     SERIAL NODE
     CVM IP
     SERIAL BLOCK
     BLOCK MODEL
     CPU MODEL
     Nro CPU
     Nro Threads
     Nro SOCKET
     Memory in GB
     HYPERVISOR VERSION
     Nro VM
     DEGRADED
     MAINTENANCE MODE
     
-VOLUME GROUP:

     UUID
     NAME
     VMDISK UUID
     VMDISK SIZE GB
     FLASH MODE

-VDISK INFO:

     VM NAME
     DEVICE ADDRESS
     VMDISK UUID
     DEVICE IN GB
     StorateCont UUID
     StorateCont Name
     Ndfs_filepath
   

-IMANGE ( PRISM ELEMENT ):

     Name
     Image Type
     Image Size in GB
     Image State
     created_time_in_usecs

Tested on windows 10 and Linux Minut , Centos and rhel.

# Nutanix-tools-for-AHV LLDP

Additional script to obtain the data associated with the physical ports of the switch top of rack and the physical ports of AHV ..
It is necessary to have the prism element information and the password of the "nutanix" user for the SSH connection.
It only works on LINUX platforms.

Requirements modules:

     paramiko
     sys
     tempfile
     time
     os
     datetime
     xlsxwriter
     subprocess
     getpass
     requests
     urllib3

Requirment on switch TOR for nutanix cluster ( Top of rack ):
     Enable LLDP or CDP on ports or global conf.

Tested on Ubuntu and Linux Mint.

INFORMATION COLLECTED BY THE SCRIPT :

     HOSTNAME
     SWITCH NAME
     SWITCH PORT
     AHV PORT

