
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
    highestUsedPosition: int = 0

unsortedOrders: list[OrderInfo] = []
orderLists: list[OrderList] = []

componentList = [
    "Active Horizontal", #0
    "Active Vertical",    #1
    "Inactive Horizontal",  #2
    "Inactive Vertical",   #3
]

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

def printUnsortedOrders():
    print("Printing unsortedOrders")
    for i in range(len(unsortedOrders)):
        print("fullOrderNum", unsortedOrders[i].fullOrderNum,
              "component", unsortedOrders[i].component,
              "length", unsortedOrders[i].length,
              "position", unsortedOrders[i].position,
              "color", unsortedOrders[i].color)
            

def calcPanelWidth(frameWidth):
    return (frameWidth / 2.0) - 0.188

def calcPanelHeight(frameHeight):
    return frameHeight - 2.625


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
                                     highestUsedPosition = 0)
            orderLists.append(newOrderList)


def initializeHighestUsedPosition():
    location = (
                    (orderLists["Color"] == unSortedOrders.iloc[0]["Color"]) & 
                    (orderLists["profileID"] == "VPDPAH2") 
                    )
    orderLists.loc[location, "highestUsedPosition"] = 1

def addDataToOrderLists(pairFound, order1in, matchPosition):
    
    tempProfileID = ""
    tempOrder2 = OrderInfo(fullOrderNum = "", 
               component = "", 
               length = 0.0, 
               position = 0, 
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
                orderLists[k].highestUsedPosition = orderLists[k].highestUsedPosition + 1  ##Just for testing, delete this later
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
    jo = "do tha merge" 

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
           
        k = 0
        
        print("orderlist row 0, orders, first list, length: ", orderLists[listIndicesToCheck[0]].orders[k].order1.length)
        if orderLists[listIndicesToCheck[0]].orders[k].order1.length == orderLists[listIndicesToCheck[1]].orders[k].order1.length:
            tempOrderSet = OrderSet(order1 = orderLists[listIndicesToCheck[0]].orders[k].order1, order2 = orderLists[listIndicesToCheck[1]].orders[k].order1)
            
            ##del unsortedOrders[matchPosition]
            
            orderLists[listBOTHindex].orders.append(tempOrderSet)
            orderLists[listBOTHindex].highestUsedPosition = orderLists[listBOTHindex].highestUsedPosition + 1 #JUST USED FOR TESTING< DELETE AFTER
            del orderLists[listIndicesToCheck[0]].orders[k]
            orderLists[listIndicesToCheck[0]].highestUsedPosition = orderLists[listIndicesToCheck[0]].highestUsedPosition - 1 #JUST USED FOR TESTING< DELETE AFTER
            del orderLists[listIndicesToCheck[1]].orders[k]
            orderLists[listIndicesToCheck[1]].highestUsedPosition = orderLists[listIndicesToCheck[1]].highestUsedPosition - 1 #JUST USED FOR TESTING< DELETE AFTER
###################################
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
           
        k = 0
        
        print("orderlist row 0, orders, first list, length: ", orderLists[listIndicesToCheck[0]].orders[k].order1.length)
        if orderLists[listIndicesToCheck[0]].orders[k].order1.length == orderLists[listIndicesToCheck[1]].orders[k].order1.length:
                tempOrderSet = OrderSet(order1 = orderLists[listIndicesToCheck[0]].orders[k].order1, order2 = orderLists[listIndicesToCheck[1]].orders[k].order1)
            
                ##del unsortedOrders[matchPosition]
            
                orderLists[listBOTHindex].orders.append(tempOrderSet)
                orderLists[listBOTHindex].highestUsedPosition = orderLists[listBOTHindex].highestUsedPosition + 1 #JUST USED FOR TESTING< DELETE AFTER
                del orderLists[listIndicesToCheck[0]].orders[k]
                orderLists[listIndicesToCheck[0]].highestUsedPosition = orderLists[listIndicesToCheck[0]].highestUsedPosition - 1 #JUST USED FOR TESTING< DELETE AFTER
                del orderLists[listIndicesToCheck[1]].orders[k]
                orderLists[listIndicesToCheck[1]].highestUsedPosition = orderLists[listIndicesToCheck[1]].highestUsedPosition - 1 #JUST USED FOR TESTING< DELETE AFTER
            




cleanDataFrame()
fillUnsortedOrders()
colorsInOrders = list({order.color for order in unsortedOrders})

printUnsortedOrders()
fillOrderLists()
mergeToBOTHList()


printOrderList()
printUnsortedOrders()



