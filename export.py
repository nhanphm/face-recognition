import csv
 
 
def export_csv(data):
    fields = ['ID', 'USER_ID', 'TIME', 'CREATE_AT']
   
    # data rows of csv file
 
    with open('export.csv', 'w') as f:
     
        # using csv.writer method from CSV package
        write = csv.writer(f)
     
        write.writerow(fields)
        write.writerows(data)