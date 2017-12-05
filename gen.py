import xlrd,csv

def excel2csv(ExcelFile, SheetName, CSVFile):
    print("Excel2CSV")
    return None
    workbook = xlrd.open_workbook(ExcelFile)
    worksheet = workbook.sheet_by_name(SheetName)
    csvfile = open(CSVFile, 'wb')
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    for rownum in range(worksheet.nrows):
        wr.writerow(
            list(x.encode('utf-8') if type(x) == type(u'') else x
                for x in worksheet.row_values(rownum)))

    csvfile.close()
