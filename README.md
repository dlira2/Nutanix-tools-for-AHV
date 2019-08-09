# NIACtool / EX-Nutanix-tools-for-AHV

![alt text](https://github.com/dlira2/Nutanix-tools-for-AHV/releases/download/v_old/niaclogo.pn?raw=true "Title")

There are 3 versions with different objectives.

0) NIACtool v2.4 Latest (Windows),
     Purpose: 100% GUI interface for windows.

Check release for download old versions:

1) NUTANIX_TOOLS_FOR_AHV_v1.7.9.py,
     Purpose: Run from terminal windows or lisnux having the interpreter and python modules installed. This version requests
     input from the user.
     
2) NUTANIX_TOOLS_FOR_AHV_v1.7.9_WEB_VERSION_NO_INPUT.py,
     Purpose: Run from terminal windows or linux having the interpreter and python modules installed. This version can have
     all the necessary input in the same call. Ideal to invoke the creation of the report through an execution schedule and
     automate the process.
     
     Example:
     python NUTANIX_TOOLS_FOR_AHV_v1.7.9_WEB_VERSION_DEF.py 10.26.1.2 admin Pass1010., CENTRAL 10.26.1.147 admin Pass1010.,
     
     
NEW ON NIACtool v2.4:

	Fix:
	1) FIX BUG ON PROTECTION DOMAIN , ON V2.3.1 NO SHOW INACTIVE PD. 
	
	New info:
	1) ADD NEW COLUMN(LOCAL/REMOTE) IN SNAPSHOT ON PD.
	
	Improvement:
	1) New order in the columns associated with the "SNAPSHOT ON DP" tab.
        2) New button in gui, now NIACtool can check if exit a new version.
   
NEW ON NIACtool v2.3:

	Fix:
	1) FIX BUG IF NO EXIT ANY NIC ON VM'S 
	2) FIX USECTIME TO DATETIME

	New info:
	1) ADD DATA PROTECTION 
	2) ADD SNAP ON DATA PROTECTION

	Improvement:
	1) STORAGE POOL NEW DISPLAY METHOD FOR SIZE POOL/DISK
	2) CONTAINER NEW DISPLAY METHOD FOR SIZE POOL/DISK
	3) SUMMARY, STORAGE CAPACITY NEW DISPLAY METHOD FOR SIZE
	4) SUMMARY, CPU AND MEMORY MORE CLEAR INFO
	
	Minor fix v2.3.1
	1) Bug on snapid ,In some situations the snapid value
	brings text and not just number, producing an error when creating the "SNAPSHOT ON PD" tab.
	Thanks Le,Loc for reporting this bug!!

NEW ON NIACtool v2.2:

Fixes:

     VM INFO TAB: 
     *NGT reachable. (Now the information is displayed correctly)
     STORAGE CONTAINER TAB:
     *FREE SPACE AND USED SPACE (Now the information is clearer)


New on gui and engine:

      GUI / CORE:
   	*FREE SPACE AND USED SPACE (Now the information is clearer)
	*Error handlers
	*Pop-ups at the end of work
	*Pop-ups if errors are found
	*Pop-ups if the required data is not complete when you press RUN

New info: 
      
      SUMMARY TAB:
	*CLUSTER CPU % USAGE.
	*CLUSTER MEMORY % USAGE.
	*CLUSTER STORAGE CAPACITY(PHYSICAL).
	*CLUSTER STORAGE USED(PHYSICAL).
	*CLUSTER STORAGE FREE(PHYSICAL).

VM INFO TAB:

        *VM OS(NGT must be installed) ( Is necessary prism central info and NGT installed on VM)


INFO:

Data collector associated with the Nutanix AHV cluster and VM´s.

Script developed in python to collect the information of Prism Element with the option of being able to connect to a Prism Central to obtain the project to which each VM belongs. The code generates an Excel table with all the information of the Nutanix platform with AHV. Many searches within the script are using Excel formulas to avoid overuse of API and the collection is more faster. The script will consult if there is an instance of Prism Central and if the user wants to obtain such information by means of a confirmation. If "Y" is selected, it will recolect the Prism Central VM proyect info. when this option is selected it may take a longer time, because you must consult for each VM to which project it belongs. A "Progress Bar" indicator was added to see if the script is running or there is a problem.

Tested on AOS 5.5.x , 5.8.x , 5.9.x and 5.10.x

Requirements (NEED UPDATES):

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


It is possible to execute connections "Safe" and not "Secure". to avoid placing IP and password repeatedly. ( Only for script)

     -Prism Element secure connection, lines 31 to 35.
     -Prism Central secure connection, lines 104 to 109.
    
     IMPORTANT 1: the variable "directory" must be declared on line 42, there is an example for windows and linux.
     IMPORTANT 2: there is a variable named TIMEOUT which by default is 15 seconds. If there are problems of slowness or     connection can modify this value according to the reality of each connection.Line 45, default 15.
     IMPORTANT 3: Variable poolingvmapi in line 47 . Hoy many VM get from prism central , default 500.. Max 500. If you want  to get less info you can modify this variable. But the script take more time tu complete all the process if you select      prism central info.

If you need help to running or any problem please contact me , dlira96@gmail.com.

INFORMATION COLLECTED BY THE SCRIPT :

-Sumarry Cluster:

     Cluster Name 
     Cluster Version
     Cluster AHV Version
     Cluster NCC Version
     Cluster Subnet
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
     RESILIENCY STATUS LEVEL ( ONLY FOR DISK)
          -N°DISK CAN BE FAIL ON METADATA
          -DISK IS REBUILDING
          -N°DISK CAN BE FAIL ON ERASURE_CODE_STRIP_SIZE
          -DISK IS REBUILDING
          -N°DISK CAN BE FAIL ON EXTENT_GROUPS
          -DISK IS REBUILDING
          -N°DISK CAN BE FAIL ON OPLOG
          -DISK IS REBUILDING 
     Date

-VM INFO:

     Cluster
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
     BIOS VERSION ( ONLY FOR NX SERIES )
     BMC VERSION ( ONLY FOR NX SERIES )
     
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
   

-PE IMAGE ( PRISM ELEMENT ):

     Name
     Image Type
     Image Size in GB
     Image State
     created_time_in_usecs
     
-PC IMAGE ( NO READY JET):

     Name
     Image Type
     Image Size in GB
     Image State
     created_time_in_usecs     
     
-PHYSICAL DISK( AHV HOST ):

     HOST IP
     HOST NAME
     CVM IP
     TIER
     LOCATION ( DISK LOCATION ON SHELF)
     DISK SIZE
     DISK ONLINE
     DISK STATE
     DISK MODEL
     DISK FIRMWARE
     DISK SERIAL
     DISK HEALTH
     
-STORAGE POOL( AHV HOST ):

     POOL UUID
     POOL NAME
     POOL CAPACITY IN TB ( RAW )
     POOL DISK UUID
     
-PROTECTION DOMAIN

     DP NAME
     ACTIVE/INACTIVE
     REMOTE SITE
     POOL DISK UUID
     NEXT SNAPSHOT
     VM NAME
     POWER STATE
     CONSISTENCY GROUP NAME
     SNAPSHOT CONSISTENCY
     SNAP TYPE
     SNAP LOCAL RETENTION
     SNAP REMOTE RETENTION
     
-SNAPSHOT ON PD

     SNAP ID
     LOCAL/REMOTE SNAP
     PROTECTED ENTITY
     DP NAME
     SNAPSHOT CREATION TIME
     SNAPSHOT EXPIRY TIME
     RECLAIMABLE SPACE
     PROTECTION TYPE
     SNAP UUID
     ENTITY DEPENDENCY

Tested on windows 10 and Linux Minut , Centos and rhel.
