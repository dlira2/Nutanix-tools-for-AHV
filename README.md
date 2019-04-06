# Nutanix-tools-for-AHV v1.0
Data collector associated with the Nutanix AHV cluster and VM´s.

Script developed in python to collect the information of Prism Element with the option of being able to connect to a Prism Central to obtain the project to which each VM belongs. The code generates an Excel table with all the information of the Nutanix platform with AHV. Many searches within the script are using Excel formulas to avoid overuse of API and the collection is more faster. The script will consult if there is an instance of Prism Central and if the user wants to obtain such information by means of a confirmation. If "Y" is selected, it will recolect the Prism Central VM proyect info. when this option is selected it may take a longer time, because you must consult for each VM to which project it belongs. A "Progress Bar" indicator was added to see if the script is running or there is a problem.

Requirements:

- python 3.6 or higher.
- Python Module :
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

