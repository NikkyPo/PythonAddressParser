import csv
import sys
#import usaddress

#example CSV path: C:\Users\helge312\Desktop\myfile.csv

def initialize():
    '''This function is the beginning of the program. The following describe the steps:
       1. Reads a CSV path that the user inputs.
       2. Calls the ReadCSV function that will read the CSV path and return a list of
           columns that are assigned to the variable ColumnOptions.
       3. Calls the userSelectColumn function that allows the user to select a column and
           assigns it to a new variable called AddressColumn.
       4. Calls the ColumnEdit function that uses AddressColumn and inCSV as arguments in
           order to parse the addresses. This is assigned to the variable Address Data and
           then, the first item (column name) is popped off.
       5. Calls the Read2NewCSV function which merges two lists together. This output is
           assigned to variable savedList.
       6. The OutCSV function is called which creates a new csv file. A message is displayed
           to confirm the process worked.
       7. Lastly, the user has the option to repeat the process. Their response is returned.'''
    
    inCSV = raw_input("Please enter the CSV path: ")
    ColumnOptions = ReadCSV(inCSV)
    AddressColumn = userSelectColumn(ColumnOptions)
    AddressData = list(ColumnEdit(AddressColumn, inCSV))
    AddressData.pop(0)    
    savedList = Read2NewCSV(inCSV, AddressData)
    OutCSV(savedList)
    print "Your new csv has been created."
    print("\n")
    NewAddress = str(raw_input("Would you like to run this program again? (Y or N): "))
    return NewAddress

def Read2NewCSV(inCSV, AddressData):
    '''This function creates two separate lists from two data sources and combines them into one.
    It uses two arguments as input. 1. inCSV - the original CSV file and 2. The formatted addresses.
    
        The first variable(outList) creates a list from the inCSV data by reading it with a
    dictionary method and using a loop to write the information into a new variable called outList.
    
       The next variable (saveList) uses a loop to read the AddressData and assigns this to a
    new variable(TempAddressDict). The first row is left out since it only contains column
    labels. Next, the .items method is used to iterate over the TempAddressDict and the previous
    outList dictionary variables and assigns both to the NewDict variable. These two are merged
    together so that the output will contain both the original CSV data and the new, parsed
    addresses. The NewDict is passed as an argument and appended to the final variable (saveList)
    that contains both merged lists.'''
    
    outList = []
    with open(inCSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            outList.append(row)

    saveList = []
    for i in range(len(AddressData)):
        TempAddressDict = dict(AddressData[i][0])
        NewDict = dict(TempAddressDict.items()+ outList[i].items())
        saveList.append(NewDict)
    print "Your data has been sucessfully merged and is now ready for output."
    return saveList

def ReadCSV(inCSV):
    '''This function reads the input CSV and returns a list of columns that are available to
    choose from. By using a loop, the function reads the input CSV and assigns it to a variable.
    Next, the function reads the first row of the CSV and prints them as options.'''
    
    with open(inCSV, "rb") as infile:
        CSV = csv.reader(infile)
        for i in range(1):
            RowID = CSV.next()
            print "Your column options are:"
            print("\n")
            for i, val in enumerate(RowID):
                print "# %s %s" % (i, val)
        return RowID

def userSelectColumn(CSV):
    '''This function inputs the available column options and lets the user select a column to
       edit and then returns their selection.'''
    
    SelectColumn = int(raw_input("Please select the column containing the addresses: "))
    return SelectColumn

def ColumnEdit(theColumn, inCSV):
    '''This function reads the input CSV and the user selected column and uses the Usaddress
       module to parse through the column of addresses. Then, the function prints a message
       confirm that the data was formatted and returns a list of dictionaries which include
       the parsed data.'''
    
    returnList = []
    with open(inCSV, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            data = row[theColumn]
            ALL2 = usaddress.tag(data)
            returnList.append(ALL2)
        print "I have read your CSV file and formatted the addresses."
        print("\n")
    return returnList

def OutCSV(saveList):
    '''This function asks the user to define a new file name where the parsed addresses and
       the original csv data will be written to. Then, the function writes this data to the
       file and prints a message to confirm this.'''
    
    userInput = raw_input("Please enter a new file name. Example: myfile.csv : ")
    keys = saveList[0].keys()
    with open(userInput, 'wb') as outFile:
        dict_writer = csv.DictWriter(outFile, keys, extrasaction='ignore')
        sorted(dict_writer.writeheader())
        sorted(dict_writer.writerows(saveList))
        print "Your new file can be found at: %s" %(userInput)
        print("\n")
    return keys

# This is where the program "starts". It prints a message to the user and immediately runs the
# initialize function. Depending on if the user would like to continue or not, their response
# 'Y' or 'N' is run through the loop to continue the program or to exit.

print ("Hello, this program reads your CSV and parses columns of addresses so they " +
        "are ready to be geocoded. Before you begin, assure that your csv file has " +
        "the columns labeled and the addresses are merged together into on column.")
print("\n")

Continue = initialize()
while Continue == 'Y':
    Continue = initialize()
sys.exit()

             
