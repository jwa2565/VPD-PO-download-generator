#I'll put stuff related to generating panel files here

from SturtzFileFormats import generateSawFileLine, generatePanelLa1FileLine
from PanelOptimization import optimizeOrders
from JoDebugTools import oFileCutListString, printCutList

from dataclasses import dataclass, field

joDebugMode = False

@dataclass
class OrderInfo:
    fullOrderNum: str
    component: str
    length: float
    position: int
    color: str

@dataclass
class OrderSet:
    order1: OrderInfo
    order2: OrderInfo
    profileID: str = ""
    length: float = 0.0
    
@dataclass
class OrderList:
    color: str
    profileID: str
    orders: list[OrderSet] = field(default_factory=list)
    highestUsedPosition: int = -1

def sawString(incomingOrderSet, profileID, color, cartID, cartBin, length):
    sawString = ""
    
    orderNum1 = incomingOrderSet.order1.fullOrderNum
    orderNum2 = incomingOrderSet.order2.fullOrderNum
    qty = 1 #Always 1 but adding this in case something changes
    
    sawString = generateSawFileLine(orderNum1, profileID, color, cartID, cartBin, qty, orderNum2, length)
    
    return sawString

def labelString(incomingOrderSet, df, count):
    labelString = ""

    orderNum1 = incomingOrderSet.order1.fullOrderNum
    orderNum2 = incomingOrderSet.order2.fullOrderNum

    labelString = generatePanelLa1FileLine(orderNum1, orderNum2, df, count)

    return labelString

def findCartID(df, orderNum):
    cartID = ""
    
    for i, rows in df.iterrows():
        if df.iloc[i]["Full Scannable Order Number"] == orderNum:
            cartID = df.iloc[i]["cartID"]
            break

    return cartID

def findCartBin(df, orderNum):
    cartBin = ""
    
    for i, rows in df.iterrows():
        if df.iloc[i]["Full Scannable Order Number"] == orderNum:
            cartBin = df.iloc[i]["cartBin"]
            break

    return cartBin
    

def PanelGenerator(df, fileNameDate, fileCounter):
    cutList: list[OrderList] = optimizeOrders(df)
    
    file_panelSaw = open(fileCounter + " PanelSaw-" + fileNameDate + ".SAW", "w")
    file_panelLabel = open(fileCounter + " PanelSaw-" + fileNameDate + ".la1", "w")
    
    countForLabel = 1
    
    for i in range(len(cutList)):
        
        barLength = 157 #this is just for testing purposes, will delete later
        
        if joDebugMode: #this is just for testing purposes, will delete later
            
            file_panelSaw.write("**DEBUGGING LINE**  ")
            file_panelSaw.write("NewBar length: " + str("%.3f" % round(barLength, 3)) )
            file_panelSaw.write("  **END DEBUGGING LINE**" + "\n")
        
        trim_initial = 1  #this is just for testing purposes, will delete later
        trim_inBetweenCuts =  2  #this is just for testing purposes, will delete later
        trimLoss = trim_initial  #this is just for testing purposes, will delete later
        cutLoss = 0#this is just for testing purposes, will delete later
        
        for j in range(len(cutList[i].orders)):
            
            file_panelSaw.write(sawString(cutList[i].orders[j], 
                                cutList[i].profileID, 
                                cutList[i].color,
                                findCartID(df, cutList[i].orders[j].order1.fullOrderNum),
                                findCartBin(df, cutList[i].orders[j].order1.fullOrderNum),
                                cutList[i].orders[j].length)
            )
            
            file_panelLabel.write(labelString(cutList[i].orders[j], df, countForLabel))
            countForLabel = countForLabel + 1
          
            for k, rows in df.iterrows(): #this is just for testing purposes, will delete later
                if df.iloc[k]["Full Scannable Order Number"] == cutList[i].orders[j].order1.fullOrderNum:
                    df.loc[k, "panelComponentsCut"] = df.iloc[k]["panelComponentsCut"] + 1
                    if joDebugMode:
                        if df.iloc[k]["panelComponentsCut"] == df.iloc[k]["panelComponentsNeeded"]:
                            file_panelSaw.write("**DEBUGGING LINE**  ")
                            file_panelSaw.write("Unit (" + str(k+1) + ") " +  df.iloc[k]["Full Scannable Order Number"] + " is Complete!")
                            file_panelSaw.write("  **END DEBUGGING LINE**" + "\n")
                    break
                
            if cutList[i].orders[j].order2.fullOrderNum != "": #this is just for testing purposes, will delete later
                for k, rows in df.iterrows():
                    if df.iloc[k]["Full Scannable Order Number"] == cutList[i].orders[j].order2.fullOrderNum:
                        df.loc[k, "panelComponentsCut"] = df.iloc[k]["panelComponentsCut"] + 1
                        if joDebugMode:
                            if df.iloc[k]["panelComponentsCut"] == df.iloc[k]["panelComponentsNeeded"]:
                                file_panelSaw.write("**DEBUGGING LINE**  ")
                                file_panelSaw.write("Unit (" + str(k+1) + ") " +  df.iloc[k]["Full Scannable Order Number"] + " is Complete!")
                                file_panelSaw.write("  **END DEBUGGING LINE**" + "\n")
                        break
                
                
            
            cutLoss = cutLoss + cutList[i].orders[j].length #this is just for testing purposes, will delete later
            trimLoss = trimLoss + trim_inBetweenCuts #this is just for testing purposes, will delete later
            #barLength = barLength - cutList[i].orders[j].length - trim_inBetweenCuts
         
        scrapLength = barLength - trimLoss - cutLoss #this is just for testing purposes, will delete later
        
        if joDebugMode: #this is just for testing purposes, will delete later
            file_panelSaw.write("**DEBUGGING LINE**  ")
            file_panelSaw.write("Theoretical remaining scrap length: " + 
                                "barLength(" + str("%.3f" % round(barLength, 3)) + ") - " +
                                "cutLoss(" + str("%.3f" % round(cutLoss, 3)) + ") - " +
                                "trimLoss(" + str("%.3f" % round(trimLoss, 3)) + ") = " +
                                "scrapLength(" + str("%.3f" % round(scrapLength, 3)) + ")"
                                )
            file_panelSaw.write("  **END DEBUGGING LINE**" + "\n") 

    file_panelSaw.close()
    file_panelLabel.close()