If WScript.Arguments.Count < 2 Then 
  Wscript.Quit 
End If 

Dim oExcel 
Dim oBook, local

Set oExcel = CreateObject("Excel.Application") 
    oExcel.DisplayAlerts = False
    Set oBook = oExcel.Workbooks.Open(Wscript.Arguments.Item(0))
local = false

call oBook.SaveAs(WScript.Arguments.Item(1), 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, local)

oBook.Close False 
oExcel.Quit 