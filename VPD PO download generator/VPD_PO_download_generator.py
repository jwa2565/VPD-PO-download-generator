
# version notes
# BETA v0.1: Initial attempt

print("Starting VPD's PO Download Generator!")
print("Importing data...")

from re import I
import time
from datetime import date

today = str(date.today())

import pandas as pd
import os
from dataclasses import dataclass, field

df = pd.read_excel("VPD PO Download Spreadsheet V0.1.xlsx")

# add "BIN" column to dataframe
# add "welder code" to dataframe

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
    
@dataclass
class OrderList:
    color: str
    profileID: str
    orders: list[OrderSet] = field(default_factory=list)
    highestUsedPosition: int = -1

unsortedOrders: list[OrderInfo] = []
orderLists: list[OrderList] = []
cutList: list[OrderList] = []

componentList = [
    "Active Horizontal", #0
    "Active Vertical",    #1
    "Inactive Horizontal",  #2
    "Inactive Vertical",   #3
]

#variables that I don't think will change
stockLength_panelLineal =192 #157 #   157", 13'-1"
stockLength_frameLineal = 197 #   197", 16'-5"
stockLength_minLength =3#3     #   3" min, the shortest material machine can hold before it fucks up
trim_initial =4.5 #1  # 1" initial cut trim
trim_inBetweenCuts =1 #2  # 2" to account for blade thickness and nailfin offsets #JO VERIFY IN THE GEOMETRYYYYYYYYYY


print("Data import successful!")
print("Generating PO download files...") 


def cleanDataFrame():

    # df["Order Number"] = df["Order Number"].fillna("empty") drop this one
    df["Type"] = df["Type"].fillna("VPD")
    # df["Frame Width"] = df["Frame Width"].fillna(12)
    # df["Frame Height"] = df["Frame Height"].fillna(12)
    # df["Color"] = df["Color"].fillna("WHWH")
    df["Customer"] = df["Customer"].fillna("###")
    df["Schedule Date"] = df["Schedule Date"].fillna("###")
    df["Destination"] = df["Destination"].fillna("###")
    df["Full Scannable Order Number"] = df["Full Scannable Order Number"].fillna(
        "empty"
    )

def printOrderList():
    print("Printing orderLists")
    for i in range(len(orderLists)):
        print("color", orderLists[i].color,
              "profileID", orderLists[i].profileID,
              "highestUsedPosition", orderLists[i].highestUsedPosition)
        for j in range(len(orderLists[i].orders)):
            print(j,
                  "Order1:", orderLists[i].orders[j].order1.fullOrderNum,
                  "Order2:", orderLists[i].orders[j].order2.fullOrderNum)
            
def printCutList():
    print("Printing cutList")
    for i in range(len(cutList)):
        print("color", cutList[i].color,
              "profileID", cutList[i].profileID,
              "highestUsedPosition", cutList[i].highestUsedPosition)
        for j in range(len(cutList[i].orders)):
            print(j,
                  "Order1:", cutList[i].orders[j].order1.fullOrderNum,
                  "Order2:", cutList[i].orders[j].order2.fullOrderNum)

def printUnsortedOrders():
    print("Printing unsortedOrders")
    for i in range(len(unsortedOrders)):
        print("fullOrderNum", unsortedOrders[i].fullOrderNum,
              "component", unsortedOrders[i].component,
              "length", unsortedOrders[i].length,
              "position", unsortedOrders[i].position,
              "color", unsortedOrders[i].color)
            

def calcPanelWidth(frameWidth):
    return (frameWidth / 2.0) - 0.188 +.25 #DELETE THE +.25! Don't add til the end cause it causes headaches and confusion and chaos TRUST ME DUDE

def calcPanelHeight(frameHeight):
    return frameHeight - 2.625 +.25 #DELETE THE +.25! Don't add til the end cause it causes headaches and confusion and chaos TRUST ME DUDE


def addRows_VPD(fullOrderNumIn, frameWidth, frameHeight, colorIn, positionIn, typeIn):

    panelWidth = calcPanelWidth(frameWidth)
    panelHeight = calcPanelHeight(frameHeight)
    
    #############################component stuff
    #"Active Horizontal", #0
    #"Active Vertical",    #1
    #"Inactive Horizontal",  #2
    #"Inactive Vertical",   #3
    componentsToUse = []
    
    if typeIn == "VPD": #Active Horizontal, Active Vertical, Inactive Horizontal, Inactive Vertical
        componentsToUse = [0,1,2,3]  
        
    elif typeIn == "VPD Transom":
        componentsToUse = [0] ###########Not correct riht now
        
    elif typeIn == "VPD FrameOnly":
        componentsToUse = [0] ###########Not correct riht now
        
    elif typeIn == "VPD ActivePanelOnly":
        componentsToUse = [0,1] #Active Horizontal, Active Vertical

    elif typeIn == "VPD InactivePanelOnly":
        componentsToUse = [2,3] #Inactive Horizontal, Inactive Vertical
        
    #############################component stuff    

    for i in range(len(componentsToUse)):
        if i == 0 or i == 2: #"Active Horizontal" or  "Inactive Horizontal"
            newRow = OrderInfo(fullOrderNum = fullOrderNumIn, 
                           component = componentList[componentsToUse[i]], 
                           length = panelWidth, 
                           position = positionIn, 
                           color = colorIn)
            
        if i == 1 or i == 3: #"Active Vertical" or "Inactive Vertical"
            newRow = OrderInfo(fullOrderNum = fullOrderNumIn, 
                           component = componentList[componentsToUse[i]], 
                           length = panelHeight, 
                           position = positionIn, 
                           color = colorIn)

        unsortedOrders.append(newRow)
        
        

def delThisProbs():
    jo = "hi"
    #def addRows_VPDTransom():
    #    hi = "hihi"


    #def addRows_VPDFrameOnly():
    #    hi = "hihi"


    #def addRows_VPDActPanOnly(fullOrderNumIn, frameWidth, frameHeight, colorIn, positionIn):
    #    panelWidth = calcPanelWidth(frameWidth)
    #    panelHeight = calcPanelHeight(frameHeight)

    #    componentsToUse = [0,1]  
    #    #"Active Horizontal", #0
    #    #"Active Vertical",    #1
    #    #"Inactive Horizontal",  #2
    #    #"Inactive Vertical",   #3

    #    for i in range(len(componentsToUse)):
    #        if i == 0 or i == 2: #"Active Horizontal" or  "Inactive Horizontal"
    #            newRow = OrderInfo(fullOrderNum = fullOrderNumIn, 
    #                           component = componentList[componentsToUse[i]], 
    #                           length = panelWidth, 
    #                           position = positionIn, 
    #                           color = colorIn)
    #            
    #        if i == 1 or i == 3: #"Active Vertical" or "Inactive Vertical"
    #            newRow = OrderInfo(fullOrderNum = fullOrderNumIn, 
    #                           component = componentList[componentsToUse[i]], 
    #                           length = panelHeight, 
    #                           position = positionIn, 
    #                           color = colorIn)#

    #        unsortedOrders.append(newRow)


    #def addRows_VPDInaPanOnly(fullOrderNum, frameWidth, frameHeight, color, position):
    #    panelWidth = calcPanelWidth(frameWidth)
    #    panelHeight = calcPanelHeight(frameHeight)#
    #
    #    newRow = [fullOrderNum, "Inactive Horizontal", panelWidth, position, color]
    #    unSortedOrders.loc[len(unSortedOrders)] = newRow
    #
    #    newRow = [fullOrderNum, "Inactive Vertical", panelHeight, position, color]
     #   unSortedOrders.loc[len(unSortedOrders)] = newRow


def fillUnsortedOrders():
    for i, rows in df.iterrows():
        addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                df.iloc[i]["Frame Width"],
                df.iloc[i]["Frame Height"],
                df.iloc[i]["Color"],
                i + 1,
                df.iloc[i]["Type"]
            )            


def generateOrderLists():  # makes all the lists needed, but they're empty 
    #colorsInOrders = unSortedOrders["Color"].unique()
    #colorsInOrders = list({order.color for order in unsortedOrders})

    panelProfileIDList = [
        "VPDPAH1",  # VPD Active Panel, Horizontal pieces, 1 unit
        "VPDPAH2",  # VPD Active Panel, Horizontal pieces, 2 units
        "VPDPAV1",  # VPD Active Panel, Vertical pieces, 1 unit
        "VPDPAV2",  # VPD Active Panel, Vertical pieces, 2 units
        "VPDPSH1",  # VPD Stationary Panel, Horizontal pieces, 1 unit
        "VPDPSH2",  # VPD Stationary Panel, Horizontal pieces, 2 units
        "VPDPSV1",  # VPD Stationary Panel, Vertical pieces, 1 unit
        "VPDPSV2",  # VPD Stationary Panel, Vertical pieces, 2 units
        "VPDPBH2",  # VPD Both Active & Stationary Panels, Horizontal pieces, 2 units
        "VPDPBV2",  # VPD Both Active & Stationary Panels, Vertical pieces, 2 units
    ]

    for i in range(len(colorsInOrders)):
        for j in range(len(panelProfileIDList)):
            newOrderList = OrderList(color = colorsInOrders[i], 
                                     profileID = panelProfileIDList[j],
                                     orders = [],
                                     highestUsedPosition = -1)
            orderLists.append(newOrderList)


def initializeHighestUsedPosition(): #the lowest SHOULD be the first position, but I'm checking all just to be safe. Initialization sets Highest Used Position to lowest position
    
    for i in range(len(orderLists)):
        
        if len(orderLists[i].orders) > 0:
            currentLowestUsedPosition = orderLists[i].orders[0].order1.position
        
            for j in range(len(orderLists[i].orders)):
                if orderLists[i].orders[j].order1.position > -1 and orderLists[i].orders[j].order1.position < currentLowestUsedPosition:
                     currentLowestUsedPosition =  orderLists[i].orders[j].order1.position
        
                if orderLists[i].orders[j].order2.position > -1 and orderLists[i].orders[j].order2.position < currentLowestUsedPosition:
                     currentLowestUsedPosition =  orderLists[i].orders[j].order2.position


            orderLists[i].highestUsedPosition = currentLowestUsedPosition

def updateHighestUsedPosition(listToUpdate, position1in, position2in):

    highestUsedPosition = position2in
    
    
    if position1in > position2in:
        highestUsedPosition = position1in
        
    orderLists[listToUpdate].highestUsedPosition = highestUsedPosition
    
    

def addDataToOrderLists(pairFound, order1in, matchPosition):
    
    tempProfileID = ""
    tempOrder2 = OrderInfo(fullOrderNum = "", 
               component = "", 
               length = 0.0, 
               position = -1, 
               color = "")

    if order1in.component == componentList[0]: #    "Active Horizontal",
        if pairFound:  
                tempProfileID = "VPDPAH2"
                tempOrder2 = unsortedOrders[matchPosition]
                del unsortedOrders[matchPosition]
                    
        else: 
                tempProfileID = "VPDPAH1"
                
    elif order1in.component == componentList[1]: #    "Active Vertical",
            if pairFound:  
                tempProfileID = "VPDPAV2"
                tempOrder2 = unsortedOrders[matchPosition]
                del unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPAV1"
                
    elif order1in.component == componentList[2]: #    "Inactive Horizontal",
            if pairFound:  
                tempProfileID = "VPDPSH2"
                tempOrder2 = unsortedOrders[matchPosition]
                del unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPSH1"
                
    elif order1in.component == componentList[3]: #    "Inactive Vertical",
            if pairFound:  
                tempProfileID = "VPDPSV2"
                tempOrder2 = unsortedOrders[matchPosition]
                del unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPSV1"
                
    tempOrderSet = OrderSet(order1 = order1in, order2 = tempOrder2)
        
    for k in range(len(orderLists)):
            if (orderLists[k].color == order1in.color
                and orderLists[k].profileID == tempProfileID):
                orderLists[k].orders.append(tempOrderSet)
                #orderLists[k].highestUsedPosition = orderLists[k].highestUsedPosition + 1  ##Just for testing, delete this later
                break

def fillOrderLists(): ##Make sure we only use this if there are items in unsortedOrders

    generateOrderLists()
    
    while len(unsortedOrders) != 0:
        
        order1 = unsortedOrders[0]
        del unsortedOrders[0]
        
        pairFound = False
        matchPosition = -1 
         
        if len(unsortedOrders) > 0: #look for pair

                searchPosition = 0
                searchEnd = len(unsortedOrders) 
        
                while not pairFound and searchPosition < searchEnd:
                    if (unsortedOrders[searchPosition].component == order1.component
                        and unsortedOrders[searchPosition].color == order1.color
                        and unsortedOrders[searchPosition].length == order1.length
                        ):

                        pairFound = True
                        matchPosition = searchPosition

                    else:
                        searchPosition = searchPosition + 1
        
        addDataToOrderLists(pairFound, order1, matchPosition)  
        
def mergeToBOTHList():

    listIndicesToCheck = []   
    listBOTHindex = -1

    for i in range(len(colorsInOrders)):
        
         ##horizontal
        for j in range(len(orderLists)): #find active horizontal 1
           if  orderLists[j].color == colorsInOrders[i] and orderLists[j].profileID == "VPDPAH1":
                listIndicesToCheck.append(j)
                break
           
        for j in range(len(orderLists)): #find stationary horizontal 1
           if  orderLists[j].color == colorsInOrders[i] and orderLists[j].profileID == "VPDPSH1":
                listIndicesToCheck.append(j)
                break

        for j in range(len(orderLists)): #find both active and stationary horizontal
           if  orderLists[j].color == colorsInOrders[i] and orderLists[j].profileID == "VPDPBH2":
                listBOTHindex = j
                break
           
        
        #printOrderList()


        if orderLists[listIndicesToCheck[0]].highestUsedPosition > 0 and orderLists[listIndicesToCheck[1]].highestUsedPosition > 0:
  
            jToDelete = []
            for j in range(len(orderLists[listIndicesToCheck[0]].orders )  ):
                
                for k in range(len(orderLists[listIndicesToCheck[1]].orders) ):
                    if orderLists[listIndicesToCheck[0]].orders[j].order1.length == orderLists[listIndicesToCheck[1]].orders[k].order1.length:
                        tempOrderSet = OrderSet(order1 = orderLists[listIndicesToCheck[0]].orders[j].order1, order2 = orderLists[listIndicesToCheck[1]].orders[k].order1) 
                        orderLists[listBOTHindex].orders.append(tempOrderSet)   
                        updateHighestUsedPosition(listBOTHindex, tempOrderSet.order1.position, tempOrderSet.order2.position)
                        
                        del orderLists[listIndicesToCheck[1]].orders[k]
                        if len(orderLists[listIndicesToCheck[1]].orders) == 0:
                            orderLists[listIndicesToCheck[1]].highestUsedPosition = -1
                        jToDelete.append(j)
                        break
              
            if len(jToDelete) > 0:            
                jToDelete.sort(reverse=True)
                for j in range(len(jToDelete)):
                     del orderLists[listIndicesToCheck[0]].orders[j]
                     if len(orderLists[listIndicesToCheck[0]].orders) == 0:
                            orderLists[listIndicesToCheck[0]].highestUsedPosition = -1

        #Vertical
        listIndicesToCheck.clear()
        for j in range(len(orderLists)): #find active Vertical 1
               if  orderLists[j].color == colorsInOrders[i] and orderLists[j].profileID == "VPDPAV1":
                    listIndicesToCheck.append(j)
                    break
           
        for j in range(len(orderLists)): #find stationary Vertical 1
               if  orderLists[j].color == colorsInOrders[i] and orderLists[j].profileID == "VPDPSV1":
                    listIndicesToCheck.append(j)
                    break

        for j in range(len(orderLists)): #find both active and stationary Vertical
               if  orderLists[j].color == colorsInOrders[i] and orderLists[j].profileID == "VPDPBV2":
                    listBOTHindex = j
                    break
           
       

        if orderLists[listIndicesToCheck[0]].highestUsedPosition > 0 and orderLists[listIndicesToCheck[1]].highestUsedPosition > 0:
            
            jToDelete = []
            for j in range(len(orderLists[listIndicesToCheck[0]].orders )  ):
                
               
                for k in range(len(orderLists[listIndicesToCheck[1]].orders) ):
                    if orderLists[listIndicesToCheck[0]].orders[j].order1.length == orderLists[listIndicesToCheck[1]].orders[k].order1.length:
                        tempOrderSet = OrderSet(order1 = orderLists[listIndicesToCheck[0]].orders[j].order1, order2 = orderLists[listIndicesToCheck[1]].orders[k].order1) 
                        orderLists[listBOTHindex].orders.append(tempOrderSet)   
                        updateHighestUsedPosition(listBOTHindex, tempOrderSet.order1.position, tempOrderSet.order2.position)

                        del orderLists[listIndicesToCheck[1]].orders[k]
                        if len(orderLists[listIndicesToCheck[1]].orders) == 0:
                            orderLists[listIndicesToCheck[1]].highestUsedPosition = -1
                        jToDelete.append(j)
                        break 
           
            if len(jToDelete) > 0:
                jToDelete.sort(reverse=True)
                for j in range(len(jToDelete)):
                     del orderLists[listIndicesToCheck[0]].orders[j]
                     if len(orderLists[listIndicesToCheck[0]].orders) == 0:
                            orderLists[listIndicesToCheck[0]].highestUsedPosition = -1

def cutHorizontalStuff(currentIndex):

    
    panelBarLength = stockLength_panelLineal
    panelBarLength = panelBarLength - trim_initial
    panelBarLength = panelBarLength - trim_inBetweenCuts
    
    horizontalIndeces = [] #Horizontal and same color
    
    for i in range(len(orderLists)):
        tempOrientation = orderLists[i].profileID[5]
        tempQTY = orderLists[i].profileID[6]
        
       
        

        if (orderLists[i].color == orderLists[currentIndex].color and #same color
        tempOrientation == "H" and           #same orientation
        tempQTY == orderLists[currentIndex].profileID[6]):   #same num of panels, 1 or 2
             horizontalIndeces.append(i)
             #print("inside the append JOOOOOOOOOOOOOOOOO")
             
        length = orderLists[currentIndex].orders[0].order1.length
        #print(length)
        
       # print("lenfffffffff of horizontalIndeces", len(horizontalIndeces))

    while (panelBarLength - orderLists[currentIndex].orders[0].order1.length)  > stockLength_minLength and len(horizontalIndeces) > 0:
        print("barlength, start =", panelBarLength)
        print("1")
        printOrderList()
        print("*************************************************************************************************************")
        panelBarLength = panelBarLength - orderLists[currentIndex].orders[0].order1.length - trim_inBetweenCuts
 

        updateHighestUsedPosition(currentIndex, orderLists[currentIndex].orders[0].order1.position, orderLists[currentIndex].orders[0].order2.position)
       
        tempSet = OrderSet(
             order1 = orderLists[currentIndex].orders[0].order1,
             order2 = orderLists[currentIndex].orders[0].order2
            )

        tempList = OrderList(
            color = orderLists[currentIndex].color,
            profileID = orderLists[currentIndex].profileID,
            orders = [],
            highestUsedPosition = orderLists[currentIndex].highestUsedPosition
            
            )
        #orderLists[currentIndex].orders.pop(0)
       
        cutList.append(tempList)


        cutList[len(cutList)-1].orders.append(tempSet) 
        #print("2")
        #printOrderList()
        #print("*************************************************************************************************************")
        orderLists[currentIndex].orders.pop(0)
        print("3")
        printOrderList()
        print("*************************************************************************************************************")
        

        print(len(orderLists[currentIndex].orders))
        if len(orderLists[currentIndex].orders) == 0:
            orderLists[currentIndex].highestUsedPosition = -1
            horizontalIndeces.remove(currentIndex)
            
            #print("4")
            #printOrderList()
            #print("*************************************************************************************************************")

       # lowestUsedPosition = orderLists[currentIndex].highestUsedPosition

        
        
        #print("1) currentIndex =", currentIndex)
        #print("len horizontalIndeces: ", len(horizontalIndeces))
        #for j in range(len(horizontalIndeces)):
        #    if orderLists[j].highestUsedPosition > 0:
        #        lowestUsedPosition = orderLists[j].highestUsedPosition
        #        currentIndex = j
                
        lowestUsedPosition = orderLists[horizontalIndeces[0]].highestUsedPosition
        currentIndex = horizontalIndeces[0]
                
        #print("lowestUsedPosition =", lowestUsedPosition)
        
        for j in range(len(horizontalIndeces)):
            #print("1) currentIndex =", currentIndex)
            #print("current highestUsedPosition", orderLists[currentIndex].highestUsedPosition)
            #print("jth highest position:", orderLists[horizontalIndeces[j]].highestUsedPosition)
            
            #if orderLists[j].highestUsedPosition > 0 and orderLists[j].highestUsedPosition < lowestUsedPosition:
            #    lowestUsedPosition = orderLists[j].highestUsedPosition
            #    currentIndex = j
                
            if orderLists[horizontalIndeces[j]].highestUsedPosition > 0 and orderLists[horizontalIndeces[j]].highestUsedPosition < lowestUsedPosition:
                lowestUsedPosition = orderLists[horizontalIndeces[j]].highestUsedPosition
                currentIndex = horizontalIndeces[j]
                
            #print("2) currentIndex =", currentIndex)
                
        #print("2) currentIndex =", currentIndex)

        print("barlength, end =", panelBarLength)
        print((panelBarLength - orderLists[currentIndex].orders[0].order1.length))
             
            
def beginCutting():
    
    
    
    lowestUsedPosition = -1
    lowestUsedPositionIndex = -1
    
    for i in range(len(orderLists)): #to find the first lowestUsedPosition
        if orderLists[i].highestUsedPosition > 0:
            lowestUsedPosition = orderLists[i].highestUsedPosition
            lowestUsedPositionIndex = i
            break

    for i in range(len(orderLists)): #to find the overall lowestUsedPoistion
        if orderLists[i].highestUsedPosition > 0 and orderLists[i].highestUsedPosition < lowestUsedPosition:
            lowestUsedPosition = orderLists[i].highestUsedPosition
            lowestUsedPositionIndex = i
            
    
    orientation = orderLists[lowestUsedPositionIndex].profileID[5] #gets the 5th character from the profileID, either H for horizontal or V for vertical
    if orientation == "H": ##This is gunna be horizontal stuff
         cutHorizontalStuff(lowestUsedPositionIndex)
         
    elif orientation == "V":
        jo = "hihihiii" 


#jToDelete = [] 
#print("jToDelete Size:", len(jToDelete))

cleanDataFrame()
fillUnsortedOrders()
colorsInOrders = list({order.color for order in unsortedOrders})

#printUnsortedOrders()
fillOrderLists()
initializeHighestUsedPosition()
#printOrderList()
mergeToBOTHList()
#printOrderList()
initializeHighestUsedPosition()


#printOrderList()

#print("!!!!!!!!!!!!!!!!!!!!!", len(orderLists) )
if len(orderLists) > 0:
    beginCutting()

#printOrderList()
printCutList()




