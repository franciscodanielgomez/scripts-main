import csv

csvFile = '/Users/franciscodanielgomez/Desktop/Stocks.csv'
txtFile1 = '/Users/franciscodanielgomez/Desktop/Stocks.txt'
txtFile2 = '/Users/franciscodanielgomez/Desktop/Photo.txt'

csvData = csv.reader(open(csvFile))
txtData1 = open(txtFile1, 'w')
txtData2 = open(txtFile2, 'w')

txtData1.write('[' + "\n")
txtData2.write('[' + "\n")

count = 500

for row in csvData:

#Stock
    
    txtData1.write('  {' + "\n")
    txtData1.write('"model": "stock.stock",' + "\n")

    txtData1.write('"pk": ' +  str(count) + ',' + "\n")
    txtData1.write('"fields": {' + "\n")
    txtData1.write('"qty": ' + row[0] + ',' + "\n")
    txtData1.write('"product": ' + row[2] +',' + "\n")
    txtData1.write('"size": ' + row[3] + ',' + "\n")
    txtData1.write('"width": ' + row[4] + ','+ "\n")
    txtData1.write('"color": ' + row[5] + ','+ "\n")
    txtData1.write('"position": ' + '"' + row[6] + '"' + "\n")

    txtData1.write('    }' + "\n")
    txtData1.write('  },' + "\n")

#Photo
    
    txtData2.write('  {' + "\n")
    txtData2.write('"model": "stock.photo",' + "\n")

    txtData2.write('"pk": null ,' + "\n")
    txtData2.write('"fields": {' + "\n")
    txtData2.write('"url": ' + '"http://royaljoyas.allianzy.com/images/' + row[1] + '.jpg"' + ',' + "\n")
    txtData2.write('"stock": ' + str(count) + "\n")

    txtData2.write('    }' + "\n")
    txtData2.write('  },' + "\n")

    count += 1
    
txtData1.write('  }' + "\n")
txtData1.write(']' + "\n")
txtData1.close()


txtData2.write('  }' + "\n")
txtData2.write(']' + "\n")
txtData2.close()
