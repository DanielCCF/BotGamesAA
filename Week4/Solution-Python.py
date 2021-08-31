#Automation packages
import rpa
from PIL import Image 
import pytesseract

#Utils packages
import os
import re
import glob

#Using Tesseract to extract the information form the files
def get_text_from_image(filename):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    try:
        return pytesseract.image_to_string (Image.open(filename).convert("RGBA"), lang = "eng")
    except:
        return ""

#The given fucntions extract specific data
#based on specific patterns
def get_invoice_number(invoiceData):
    invoiceTextWithNumberPattern = r'Invoice no.[ ]{0,}[0-9]{1,}'
    invoiceTextAndNextLinePattern = r'Invoice no.*[\n| ]+[^\n]+'
    numberPattern = r'[0-9]{1,}$'

    invoiceNumber = ''.join(re.findall(invoiceTextWithNumberPattern,invoiceData))
    if invoiceNumber == '':
        invoiceNumber = ''.join(re.findall(invoiceTextAndNextLinePattern,invoiceData,re.MULTILINE))

    return ''.join(re.findall(numberPattern,invoiceNumber))

def get_invoice_date(invoiceData):
    fullDatePattern = r'[0-9]{1,2} [A-Za-za-z]{3} [0-9]{4}'

    return ''.join(re.findall(fullDatePattern,invoiceData))

def get_invoice_total(invoiceData):
    invoiceTotalEntireRowPattern = r'Invoice Amount.*[0-9,.]{1,}$'
    invoiceValueOnlyPattern = r'[0-9,.]{1,}$'
    
    invoiceValue = ''.join(re.findall(invoiceTotalEntireRowPattern,invoiceData,re.MULTILINE))
    invoiceValue = ''.join(re.findall(invoiceValueOnlyPattern,invoiceValue))
    invoiceValue = invoiceValue.replace(',','')
    
    return invoiceValue

def get_invoice_quantities(invoiceData):
    tableContentPattern = r'^[0-9]{1,} \|.*$'
    quantitiesPattern = r'^[0-9]{1,}(?=\|| \|)'

    quantities = '\n'.join(re.findall(tableContentPattern,invoiceData,re.MULTILINE))
    quantities = re.findall(quantitiesPattern,quantities,re.MULTILINE)
    quantities = [x.strip() for x in quantities]

    return quantities

def get_invoice_descriptions(invoiceData):
    tableContentPattern = r'^[0-9]{1,} \|.*$'
    quantitiesPlusIdPattern = r'^[0-9]{1,}[ ]{0,}\|[ ]{0,}[\S]*'
    pricePlusTaxPlusAmountPattern = r' [0-9,.]{1,}[\W]{0,}[A-Z]{1,1}[\W]{0,}[0-9,.]{1,}$'

    descriptions = re.findall(tableContentPattern,invoiceData,re.MULTILINE)
    descriptions = [re.sub(quantitiesPlusIdPattern,'',x) for x in descriptions]
    descriptions = [re.sub(pricePlusTaxPlusAmountPattern,'',x) for x in descriptions]
    descriptions = [x.strip() for x in descriptions]

    return descriptions

def get_invoice_totals_per_item(invoiceData):
    tableContentPattern = r'^[0-9]{1,} \|.*$'
    amountsPattern = r'(?<=[G][ |\|])[0-9,.]{1,}'

    totalsPerItem = '\n'.join(re.findall(tableContentPattern,invoiceData,re.MULTILINE))
    totalsPerItem = re.findall(amountsPattern,totalsPerItem,re.MULTILINE)
    totalsPerItem = [x.replace(',','').strip() for x in totalsPerItem]

    return totalsPerItem


#Getting current directory
dir = os.path.dirname(__file__)

rpa.init()

#Extracting all invoices data
invoiceData = []
os.chdir(dir)
for imageName in glob.glob("*.tiff"):
    #Building the file name and extracting its information
    filename = os.path.join(dir, imageName)
    output = get_text_from_image(filename)

    #Getting the invoice data and adding to the list
    invoiceData.append({'invoiceNumber': get_invoice_number(output).strip(),
                        'invoiceDate' : get_invoice_date(output).strip(),
                        'invoiceTotal' : get_invoice_total(output).strip(),
                        'invoiceQuantities' : get_invoice_quantities(output),
                        'invoiceDescriptions' : get_invoice_descriptions(output),
                        'invoiceTotalsPerItem' : get_invoice_totals_per_item(output),
                        'filename': filename})

#Acessing challenge website
rpa.url('https://developer.automationanywhere.com/challenges/automationanywherelabs-invoiceentry.html')

rpa.wait(2)
#Looping through each invoice
for invoice in invoiceData:
    #Filling input fields information
    rpa.dom('document.getElementById("invoiceNumber").value = ' + "'" + invoice['invoiceNumber'] + "'")
    rpa.dom('document.getElementById("invoiceDate").value = ' + "'" + invoice['invoiceDate'] + "'")
    rpa.dom('document.getElementById("invoiceTotal").value = ' + "'" + invoice['invoiceTotal'] + "'")

    #Adding the amount of needed rows for processing
    for i in range(len(invoice['invoiceQuantities'])-1):
         rpa.dom('document.evaluate("//*[@id=\'myDIV\']/div/button[1]",document,null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')

    #Filing the invoice details in a table
    for i in range(len(invoice['invoiceQuantities'])):
        rpa.dom('document.getElementById("quantity_row_'+ str(i+1) +'").value = ' + "'" + invoice['invoiceQuantities'][i] + "'")
        rpa.dom('document.getElementById("description_row_'+ str(i+1) +'").value = ' + "'" + invoice['invoiceDescriptions'][i] + "'")
        rpa.dom('document.getElementById("price_row_'+ str(i+1) +'").value = ' + "'" + invoice['invoiceTotalsPerItem'][i] + "'")


    #Uploading the file, agreeing with terms and submit input
    rpa.upload('#fileupload',invoice['filename'])
    rpa.dom("document.getElementById('agreeToTermsYes').click()")
    rpa.dom("document.getElementById('submit_button').click()")

#Waiting for the ouput image and printing it
rpa.wait(2)
rpa.snap('page', '\\Week4\\Result-Standard.png')
rpa.close()