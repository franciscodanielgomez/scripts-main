import csv
from stock.models import Color, Size, LinkWidth, Stock, Product

csvFile = '/Users/franciscodanielgomez/Desktop/Stocks.csv'
csvData = csv.reader(open(csvFile))

color = Color.objects.get(name="Unico")
size = Size.objects.get(name="Unico")
linkwidth = LinkWidth.objects.get(name="Unico")

#Stock

for row in csvData:
    sku = row[0]
    qty = int(row[1])

    try:
        product = Product.objects.get(sku=sku)
        stock, created = Stock.objects.get_or_create(product=product, color=color, size=size, width=linkwidth, defaults={'qty': 0})
    
        stock.qty = qty
        stock.save()
    except Product.DoesNotExist:
        print(f"Sku no encontrado: {sku}")
