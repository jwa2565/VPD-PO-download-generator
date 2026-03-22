#Stuff to generate Sturtz-specific machine file lines

def padAssWithSpaces(inString, n):  # n is how many characters the field needs to be
    while len(inString) < n:
        inString = inString + " "

    return inString

def padFrontWithZeros(inString, n):  # n is how many characters the field needs to be
    while len(inString) < n:
        inString = "0" + inString

    return inString

def lengthCorrectSturtzFormatConverter(length):
    
    length_string = str("%.2f" % round(length, 2)).replace(".", "")  # turn to string & remove decimal
    length_string = padFrontWithZeros(length_string, 5) # make it 5 characters
    
    return length_string

def fix_orderNum(orderNum, numOfChars):
    orderNumString = str(orderNum)
    orderNumString = orderNumString[-numOfChars:]
    
    orderNumString = padAssWithSpaces(orderNumString, numOfChars)

    return orderNumString

def fix_profileID(profileID, numOfChars):
    profileIDString = profileID
    profileIDString = profileIDString[-numOfChars:]
    
    profileIDString = padAssWithSpaces(profileIDString, numOfChars)

    return profileIDString
   
def fix_color(color, numOfChars):
    colorString = color
    colorString = colorString[-numOfChars:]
    
    colorString = padAssWithSpaces(colorString, numOfChars)
    
    return colorString
    
def fix_binNum(cartID, cartBin, numOfChars):
    cartBinString = str(cartBin)
    cartBinString = cartBinString[-2:] #If for some reason its larger than 2 digits
    cartBinString = padFrontWithZeros(cartBinString, 2)
    
    binNumString = cartID + cartBinString + cartID

    binNumString = binNumString[-numOfChars:]
    binNumString = padAssWithSpaces(binNumString, numOfChars) #theoritically shouldn't need this, but adding it anyways
    
    return binNumString

def fix_qty(qty, numOfChars):
    qtyString = str(qty)
    qtyString = qtyString[-numOfChars:] #If for some reason its larger than 999
    qtyString = padFrontWithZeros(qtyString, numOfChars)
    
    return qtyString
    
def fix_comment(order1, order2, numOfChars):
    order1String = str(order1)
    order2String = str(order2)
    
    commentString = order1String
    
    if len(order2String) != 0:
        commentString = commentString + ";" + order2String
        
    commentString = commentString[-numOfChars:]
    commentString = padAssWithSpaces(commentString, numOfChars)
    
    return commentString
    
def fix_length(length, numOfChars):
    lengthString = lengthCorrectSturtzFormatConverter(length)
    lengthString = lengthString[-numOfChars:]
    lengthString = padFrontWithZeros(lengthString, numOfChars) # make it 5 characters
    
    return lengthString

def adjustForDualTransoms(profileID):
    jo = "Hihi"
    if profileID == "": #Thing for dual transom
        code = "code to find both orders and change the QR code to begin with VPTT*"

def generateSawFileLine(orderNum1, profileID, color, cartID, cartBin, qty, orderNum2, length):
    
    sawFileLine = ""
    
    sawFileLine = sawFileLine + "K" + fix_orderNum(orderNum1, 10)            #orderNum
    sawFileLine = sawFileLine + "P" + fix_profileID(profileID, 10)           #profileID
    sawFileLine = sawFileLine + "T" + fix_color(color, 4)                    #color
    sawFileLine = sawFileLine + "N" + fix_binNum(cartID, cartBin, 4)         #binNum
    sawFileLine = sawFileLine + "A" + fix_qty(qty, 3)                        #qty
    sawFileLine = sawFileLine + "C" + fix_comment(orderNum1, orderNum2, 60)  #comment
    sawFileLine = sawFileLine + "L" + fix_length(length, 5)                  #length
    sawFileLine = sawFileLine + "\n"
    
    return sawFileLine

def generatePanelLa1FileLine(orderNum1, orderNum2, df, count):
    panelLa1FileLine = ""
    
    orderRow = -1
    
    for i, rows in df.iterrows():
        if df.iloc[i]["Full Scannable Order Number"] == orderNum1:
            orderRow = i
            break
        
    #add order1 info
    if orderRow != -1:
       panelLa1FileLine = panelLa1FileLine + "LabId;" + str(count) + ";\n"
       panelLa1FileLine = panelLa1FileLine + "FE=Sturtz1;\n"
       panelLa1FileLine = panelLa1FileLine + "S1=" + df.iloc[orderRow]["Frame Width"] + " x " + df.iloc[orderRow]["Frame Height"] + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S2=" + str(df.iloc[orderRow]["Schedule Date"].date()) + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S3=" + str(orderNum1) + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S4="  + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S5="  + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S6="  + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S7="  + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S8=" + df.iloc[orderRow]["Customer"] + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S9="  + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S10=" + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S11=" + df.iloc[orderRow]["Color"] + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S12=" + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S13=" + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S14=" + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S15=" + ";\n"
       panelLa1FileLine = panelLa1FileLine + "S16=" + fix_binNum(df.iloc[orderRow]["cartID"], df.iloc[orderRow]["cartBin"], 4) + ";\n"
       panelLa1FileLine = panelLa1FileLine + "BA1=" + df.iloc[orderRow]["panelWelderQRCode"] + "\n\n"
       
       if orderNum2 != "":
            orderRow = -1
       
            for i, rows in df.iterrows():
                if df.iloc[i]["Full Scannable Order Number"] == orderNum2:
                    orderRow = i
                    break
        
            #add order2 info
            if orderRow != -1:
               panelLa1FileLine = panelLa1FileLine + "FE=Sturtz1;\n"
               panelLa1FileLine = panelLa1FileLine + "S1=" + df.iloc[orderRow]["Frame Width"] + " x " + df.iloc[orderRow]["Frame Height"] + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S2=" + str(df.iloc[orderRow]["Schedule Date"].date()) + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S3=" + str(orderNum1) + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S4="  + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S5="  + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S6="  + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S7="  + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S8=" + df.iloc[orderRow]["Customer"] + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S9="  + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S10=" + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S11=" + df.iloc[orderRow]["Color"] + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S12=" + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S13=" + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S14=" + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S15=" + ";\n"
               panelLa1FileLine = panelLa1FileLine + "S16=" + fix_binNum(df.iloc[orderRow]["cartID"], df.iloc[orderRow]["cartBin"], 4) + ";\n"
               panelLa1FileLine = panelLa1FileLine + "BA1=" + df.iloc[orderRow]["panelWelderQRCode"] + ";\n\n"

    return panelLa1FileLine

def generateFrameLa1FileLine(count, date, orderNum, customer, frameWidth, frameHeight, color, handing, cartID, cartBin, frameWelderQRCode):
    frameLa1FileLine = ""

    frameLa1FileLine = frameLa1FileLine + "LabId;" + str(count) + ";\n"
    frameLa1FileLine = frameLa1FileLine + "FE=Sturtz1;\n"
    frameLa1FileLine = frameLa1FileLine + "S1=" + str(date.date()) + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S2=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S3=" + str(orderNum) + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S4=" + str(orderNum) + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S5=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S6=" + customer + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S7=" + frameWidth + " x " + frameHeight + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S8=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S9=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S10=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S11=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S12=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S13=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S14=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S15=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S16=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S17=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S18=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S19=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S20=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S21=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S22=" + color + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S23=" + handing + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S24=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S25=" + "" + ";\n"
    frameLa1FileLine = frameLa1FileLine + "S26=" + fix_binNum(cartID, cartBin, 4) + ";\n"
    frameLa1FileLine = frameLa1FileLine + "BA1=" + frameWelderQRCode + ";\n"
    frameLa1FileLine = frameLa1FileLine + "BA2=" + str(orderNum) + ";\n\n"

    return frameLa1FileLine