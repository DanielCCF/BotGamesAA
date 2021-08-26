//Creating the paths for the Excel Files and VBS Script
js flow_path_formated = flow_path.split('/').join('\\')
ExcelToVBS = flow_path_formated + '\\ExcelToVbs.vbs'
StateAssignments = flow_path_formated + '\\StateAssignments.xlsx'
TargetCsvFile = flow_path_formated + '\\StateAssignments.csv'

//Acessing website
`MainWebSite`

//Downloading Excel file and transforming it in a CSV
click `ExcelDownloadButton`
wait 2 s
run cmd /c `ExcelToVBS` `StateAssignments` `TargetCsvFile`

//Loading and transforming the data
load StateAssignments.csv to fullData
js fullData = fullData.split('\n')

//Acessing the PO System and returning to the main page
click `POTrackingRedirect`
popup POTrackingLogin
    type inputEmail as admin@procurementanywhere.com
    type inputPassword as paypacksh!p
    click `SignInButton`

keyboard [ctrl][pageup]

//Refreshing the main page to reduce the execution time
`MainWebSite`

//Getting the total amount of cases to process
dom return document.evaluate("count(//*[contains(@id,'PONumber')])",document).numberValue
wait 1 s
PurchaseOrdersAmount = dom_result

//Filling the information per case
for i from 1 to PurchaseOrdersAmount
    read //*[@id="PONumber`i`"] to CurrentPoNumber
    popup POtrackingLookup
        type //*[@id="dtBasicExample_filter"]/label/input as [clear]`CurrentPoNumber`
        read //*[@id="dtBasicExample"]/tbody/tr/td[7] to CurrentDate
        read //*[@id="dtBasicExample"]/tbody/tr/td[8] to CurrentValue
        js CurrentValue = CurrentValue.replace('$','')
        read //*[@id="dtBasicExample"]/tbody/tr/td[5] to CurrentState

        //Getting the agent name based on the state captured and
        //the CSV data that came from the Excel file
        dom_json = {data:fullData,state:CurrentState}
        dom return dom_json.data.filter(function(item){return item.includes(dom_json.state)})[0].split(',')[1].trim()
        CurrentAgent = dom_result

    type //*[@id="shipDate`i`"] as `CurrentDate`
    type //*[@id="orderTotal`i`"] as `CurrentValue`
    select //*[@id="agent`i`"] as `CurrentAgent`


//Submiting and taking a snapshot 
click //*[@id="submitbutton"]
wait 1 s
snap page to Result-Standard.png
