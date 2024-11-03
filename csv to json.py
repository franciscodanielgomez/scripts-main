import csv

csvFile = '/Users/franciscodanielgomez/Desktop/Nuevos.csv'
txtFile = '/Users/franciscodanielgomez/Desktop/myfile.txt'

csvData = csv.reader(open(csvFile))
txtData = open(txtFile, 'w')

txtData.write('[' + "\n")
rowNum = 0
for row in csvData:
    if rowNum == 0:
        tags = row
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(';', '-')
    else: 
       
        for i in range(len(tags)):

            txtData.write('  {' + "\n")
            txtData.write('"model": "stock.product",' + "\n")

            txtData.write('"pk": ' + '"null"' + ' , ' + "\n")
            txtData.write('"fields": {' + "\n")
            txtData.write('"sku": ' + '"' + row[0] + '"' + ', ' + "\n")
            txtData.write('"name": ' + '"' + row[1] + '"' + ',' + "\n")
            txtData.write('"price": ' + row[2] + ',' + "\n")
            txtData.write('"description": ' + '"' + row[3] + '"' + ',' +  "\n")
            txtData.write('"category": ' + row[4] +  "\n")

            txtData.write('    }' + "\n")
            txtData.write('  },' + "\n")

    rowNum +=1
    
txtData.write('  }' + "\n")
txtData.write(']' + "\n")
txtData.close()

