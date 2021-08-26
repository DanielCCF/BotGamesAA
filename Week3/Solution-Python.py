#Automation packages
import rpa as r
from pywinauto.application import Application
import requests

#Utils packages
import json
import os
import sys
import subprocess
from zipfile import ZipFile

#Gets the app '.exe' path and launching it
def get_database_app():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'EmployeeList.exe')
    return Application().start(filename).EmployeeDatabase

#It uses the employeer id to return certain
#data from an API
def get_emp_info_from_api(emp_Id):
    request = requests.get(
        'https://botgames-employee-data-migration-vwsrh7tyda-uc.a.run.app/employees?id='+emp_Id)
    return request.content

#With the given app, it will extract the information based
#on the employeer id
def get_emp_info_from_database_app(emp_Id, app):
    app.child_window(auto_id='txtEmpId').type_keys(emp_Id)
    app.child_window(auto_id='btnSearch').click()
    info = {'firstName': app.child_window(auto_id='txtFirstName').window_text()}
    info['lastName'] = app.child_window(auto_id='txtLastName').window_text()
    info['email'] = app.child_window(auto_id='txtEmailId').window_text()
    info['zipCode'] = app.child_window(auto_id='txtZip').window_text()
    info['city'] = app.child_window(auto_id='txtCity').window_text()
    info['jobTitle'] = app.child_window(auto_id='txtJobTitle').window_text()
    info['department'] = app.child_window(auto_id='txtDepartment').window_text()
    info['manager'] = app.child_window(auto_id='txtManager').window_text()
    info['state'] = app.child_window(auto_id='txtState').window_text()
    app.child_window(auto_id='btnClear').click()
    
    return info


r.init()

#Preparing the execution
dir = os.path.dirname(__file__)
zippedAppPath = dir + '\\EmployeeList.zip'
downloadAppButton = '/html/body/div[1]/div/div[2]/div[1]/div[2]/a'
r.url('https://developer.automationanywhere.com/challenges/automationanywherelabs-employeedatamigration.html')
r.download_location(dir)

#Downloading and opening the App
r.click(downloadAppButton)
while not os.path.exists(zippedAppPath):
    r.wait(1)
with ZipFile(zippedAppPath, 'r') as zipApp:
   zipApp.extractall(dir)
app = get_database_app()

#Refreshing the app after preparation is done
r.url('https://developer.automationanywhere.com/challenges/automationanywherelabs-employeedatamigration.html')
r.wait(1)

for i in range(10):
     #Capturing the data
    emp = r.read('employeeID')
    desktop_app_data = get_emp_info_from_database_app(emp,app)
    api_data = json.loads(get_emp_info_from_api(emp))

    #Fill the information based on the extracted dictionaries
    r.dom('document.getElementById("firstName").value = ' + "'" + desktop_app_data['firstName'] + "'")
    r.dom('document.getElementById("lastName").value = ' +  "'" + desktop_app_data['lastName'] + "'")
    r.dom('document.getElementById("phone").value = ' + "'" + api_data['phoneNumber'] + "'")
    r.dom('document.getElementById("email").value = ' + "'" + desktop_app_data['email'] + "'")
    r.dom('document.getElementById("city").value = ' + "'" + desktop_app_data['city'] + "'")
    r.dom('document.getElementById("state").value = ' + "'" + desktop_app_data['state'] + "'")
    r.dom('document.getElementById("zip").value = ' + "'" + desktop_app_data['zipCode'] + "'")
    r.dom('document.getElementById("title").value = ' + "'" + desktop_app_data['jobTitle'] + "'")
    r.dom('document.getElementById("department").value = ' + "'" + desktop_app_data['department'] + "'")
    r.dom('document.getElementById("startDate").value = ' + "'" + api_data['startDate'] + "'")
    r.dom('document.getElementById("manager").value = ' + "'" + desktop_app_data['manager'] + "'")
    
    r.click('submitButton')

#Taking the snapshot and finishing the process
r.wait(2)

r.snap('page', '\\Week3\\Result-Standard.png')

r.close()
