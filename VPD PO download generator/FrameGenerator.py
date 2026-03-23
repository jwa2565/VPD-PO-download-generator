#I'll put stuff related to generating frame files here

from SturtzFileFormats import generateSawFileLine, generateFrameLa1FileLine, lengthCorrectSturtzFormatConverter

#takes in frame width from spreadsheet and returns the correct float 
def detFrameWidth(frameWidthString):
    frameWidth = 0.0

    if frameWidthString == "2-6":
        frameWidth = 32.1875 

    elif frameWidthString == "3-0":
        frameWidth = 38.1875 
        
    elif frameWidthString == "4-0":
        frameWidth = 50.1875 

    elif frameWidthString == "5-0":
        frameWidth = 59.500 

    elif frameWidthString == "6-0":
        frameWidth = 71.500 

    elif frameWidthString == "8-0":
        frameWidth = 95.500

    else: frameWidth = float(frameWidthString) 
    
    return frameWidth

#takes in frame height from spreadsheet and returns the correct float
def detFrameHeight(frameHeightString):
    frameHeight = 0.0

    if frameHeightString == "1-2":
        frameHeight = 13.500 

    elif frameHeightString == "1-4":
        frameHeight = 15.500 
        
    elif frameHeightString == "1-8":
        frameHeight = 19.500 

    elif frameHeightString == "2-0":
        frameHeight = 23.500 

    elif frameHeightString == "6-8":
        frameHeight = 79.500 

    elif frameHeightString == "6-10":
        frameHeight = 81.500
        
    elif frameHeightString == "8-0":
        frameHeight = 95.500
        
    else: frameHeight = float(frameHeightString) 
    
    return frameHeight

def addMacro_JAMB_KEEPER_PLATE(callSize):
    macro = ""
    location = 0.0
    
    if callSize == "6-8":
        location = 39.875

    elif callSize == "6-10":
        location = 40.875
        
    elif callSize == "8-0":
        location = 39.875
        
    macro = macro + "Fab;JAMB_KEEPER_PLATE;"
    macro = macro + lengthCorrectSturtzFormatConverter(location)

    return macro

def addFrameMacros(callSize):
    frameMacros = ""
    
    frameMacros = frameMacros + addMacro_JAMB_KEEPER_PLATE(callSize) + ";\n"

    return frameMacros

def sawString(orderNum, color, cartID, cartBin, frameWidthString, frameHeightString, typeIn, profileID, cutLength):
    sawString = ""

    sawString = sawString + generateSawFileLine(orderNum, profileID, color, cartID, cartBin, 1, "", cutLength)

    if typeIn != "VPD Transom" and profileID == "VPDFJB": #cause transoms don't get fab macros
        sawString = sawString + addFrameMacros(frameHeightString)
            
    return sawString

def labelString(orderNum, count, date, customer, frameWidthString, frameHeightString, color, handing, cartID, cartBin, frameWelderQRCode):
    labelString = ""

    labelString = labelString + generateFrameLa1FileLine(count, date, orderNum, customer, frameWidthString,
                                                         frameHeightString, color, handing, cartID, cartBin, 
                                                         frameWelderQRCode)

    return labelString

def detFrameQRCode(frameWidthString, frameHeightString, color):
    frameQRCode = ""
    frameWidth = detFrameWidth(frameWidthString)
    frameHeight = detFrameHeight(frameHeightString)

    
    frameQRCode = frameQRCode + "NVFNN"
    frameQRCode = frameQRCode + color
    frameQRCode = frameQRCode + "***"
    frameQRCode = frameQRCode + lengthCorrectSturtzFormatConverter(frameHeight)
    frameQRCode = frameQRCode + lengthCorrectSturtzFormatConverter(frameWidth)

    return frameQRCode

def FrameGenerator(df, fileNameDate, fileCounter):
    print("Generating Frame Files...")

    file_frameSaw = open(fileCounter + " FrameSaw-" + fileNameDate + ".SAW", "w")
    file_frameLabel = open(fileCounter + " FrameSaw-" + fileNameDate + ".la1", "w")
    
    frameProfileIDs = ["VPDFJB", #VDP Frame, Jambs
                       "VPDFHS"  #VPD Frame, Head/Sill
        ]
    
    countForLabel = 1
     
    for i, rows in df.iterrows():

        df.loc[i, "frameWelderQRCode"] = detFrameQRCode(df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"], df.iloc[i]["Color"]) 
        #going ahead and adding framewelderQR code while I'm in a dataframe loop lol don't judge
        
        if df.iloc[i]["Type"] != "VPD ActivePanelOnly (ACT PAN)" and df.iloc[i]["Type"] != "VPD InactivePanelOnly (INA PAN)": #all other options require making a frame saw line
            frameWidth = detFrameWidth(df.iloc[i]["Frame Width"]) 
            frameHeight = detFrameHeight(df.iloc[i]["Frame Height"])
            cutLength = 0.0
            
            for j in range(len(frameProfileIDs)):
                profileID = frameProfileIDs[j]
                if profileID == "VPDFJB": cutLength = frameHeight + .25
                elif profileID == "VPDFHS": cutLength = frameWidth + .25

                file_frameSaw.write(sawString(df.iloc[i]["Full Scannable Order Number"],
                                              df.iloc[i]["Color"],
                                              df.iloc[i]["cartID"],
                                              df.iloc[i]["cartBin"],
                                              df.iloc[i]["Frame Width"],
                                              df.iloc[i]["Frame Height"],
                                              df.iloc[i]["Type"],
                                              profileID,          
                                              cutLength))       
                                    
                file_frameLabel.write(labelString(df.iloc[i]["Full Scannable Order Number"], 
                                                  countForLabel,
                                                  df.iloc[i]["Schedule Date"],
                                                  df.iloc[i]["Customer"],
                                                  df.iloc[i]["Frame Width"],
                                                  df.iloc[i]["Frame Height"],
                                                  df.iloc[i]["Color"],
                                                  df.iloc[i]["Handing"],
                                                  df.iloc[i]["cartID"],
                                                  df.iloc[i]["cartBin"],
                                                  df.iloc[i]["frameWelderQRCode"]))
            
                countForLabel = countForLabel + 1

    file_frameSaw.close()
    file_frameLabel.close()
    
    print("Frame Files done")
    
