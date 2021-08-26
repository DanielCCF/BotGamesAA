rowsCsvFile = ''
currentRow = []
optionDiscount = ''
optionNonDisclosureAgreement = ''
csvFileToDownload = '/html/body/div[1]/p/a'

https://developer.automationanywhere.com/challenges/automationanywherelabs-customeronboarding.html

// Downloading the csv file
click `csvFileToDownload`
wait 2
load MissingCustomers.csv to fullData

// Loading the data in a iterable Array
js rowsCsvFile = fullData.split('\n').length;
js splittedRows = fullData.split('\n');

// Reading the Array and filling the website form
for i from 1 to rowsCsvFile-1
   js currentRow = fullData.split('\n')[i].split(',') 
   type customerName as [clear]`currentRow[0]`
   type customerID as [clear]`currentRow[1]`
   type primaryContact as [clear]`currentRow[2]`
   type street as [clear]`currentRow[3]`
   type city as [clear]`currentRow[4]`
   select state as `currentRow[5]`  
   type zip as [clear]`currentRow[6]`
   type email as [clear]`currentRow[7]`
   js  optionDiscount = 'activeDiscount' + currentRow[8].replace('YES','Yes').replace('NO','No')
   click `optionDiscount`
   js optionNonDisclosureAgreement = currentRow[9].replace('YES',1).replace('NO',0)
   dom_json = {option:optionNonDisclosureAgreement}
   dom document.getElementById("NDA").checked = parseInt(dom_json.option)

   click submit_button

// Printing the results
wait 1 s
snap page to Result-Standard.png
