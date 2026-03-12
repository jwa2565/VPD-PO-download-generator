
# version notes
# BETA v0.1: Initial attempt

print("Starting VPD's PO Download Generator!")
print("Importing data...")

import time
from datetime import date

today = str(date.today())

import pandas as pd
import os
from dataclasses import dataclass, field

df = pd.read_excel("VPD PO Download Spreadsheet V0.1.xlsx")


#unSortedOrders = pd.DataFrame(
#    columns=["fullOrder#", "Component", "Length", "Position", "Color"]
#)
#orderLists = pd.DataFrame(
#    columns=["Color", "profileID", "orders", "highestUsedPosition"]
#)

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
    colorsInOrders = list({order.color for order in unsortedOrders})

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

def fillOrderLists():

    generateOrderLists()
    
    for i in range(len(unsortedOrders)): #might have to change this to a while loop if I plan on removing things from unsortedOrders
        pairFound = False
        searchPosition = i + 1
        searchEnd = len(unsortedOrders)
        matchPosition = -1
        
        while not pairFound and searchPosition < searchEnd:
            if (unsortedOrders[searchPosition].component == unsortedOrders[i].component
                and unsortedOrders[searchPosition].color == unsortedOrders[i].color
                and unsortedOrders[searchPosition].length == unsortedOrders[i].length
                ):

                pairFound = True
                matchPosition = searchPosition

            else:
                searchPosition = searchPosition + 1
                
        tempProfileID = ""
        tempOrder1 = OrderInfo(fullOrderNum = "", 
               component = "", 
               length = 0.0, 
               position = 0, 
               color = "")
        tempOrder2 = OrderInfo(fullOrderNum = "", 
               component = "", 
               length = 0.0, 
               position = 0, 
               color = "")
       # tempOrderSet = OrderSet()
        

        if unsortedOrders[i].component == componentList[0]: #    "Active Horizontal",
            if pairFound:  
                tempProfileID = "VPDPAH2"
                tempOrder1 = unsortedOrders[i]
                tempOrder2 = unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPAH1"
                tempOrder1 = unsortedOrders[i]
                
        elif unsortedOrders[i].component == componentList[1]: #    "Active Vertical",
            if pairFound:  
                tempProfileID = "VPDPAV2"
                tempOrder1 = unsortedOrders[i]
                tempOrder2 = unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPAV1"
                tempOrder1 = unsortedOrders[i]
                
        elif unsortedOrders[i].component == componentList[2]: #    "Inactive Horizontal",
            if pairFound:  
                tempProfileID = "VPDPSH2"
                tempOrder1 = unsortedOrders[i]
                tempOrder2 = unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPSH1"
                tempOrder1 = unsortedOrders[i]
                
        elif unsortedOrders[i].component == componentList[3]: #    "Inactive Vertical",
            if pairFound:  
                tempProfileID = "VPDPSV2"
                tempOrder1 = unsortedOrders[i]
                tempOrder2 = unsortedOrders[matchPosition]
                    
            else: 
                tempProfileID = "VPDPSV1"
                tempOrder1 = unsortedOrders[i]


                
        tempOrderSet = OrderSet(order1 = tempOrder1, order2 = tempOrder2)
        
        for k in range(len(orderLists)):
            if (orderLists[k].color == unsortedOrders[i].color
                and orderLists[k].profileID == tempProfileID):
                orderLists[k].orders.append(tempOrderSet)
                break
            
def del2():
    mhm = "yep"
    ##############################

    #    for i, rows in unSortedOrders.iterrows():

    #        pairFound = False
    #        searchPosition = i + 1
    #        searchEnd = len(unSortedOrders)
    #        matchPosition = -1

    #        while not pairFound and searchPosition < searchEnd:
    #            if (unSortedOrders.iloc[searchPosition]["Component"] == unSortedOrders.iloc[i]["Component"]
    #                and unSortedOrders.iloc[searchPosition]["Color"] == unSortedOrders.iloc[i]["Color"]
    #                and unSortedOrders.iloc[searchPosition]["Length"] == unSortedOrders.iloc[i]["Length"]
     #               ):
    #
    #                pairFound = True
    #                matchPosition = searchPosition
    #
    #            else:
    #                searchPosition = searchPosition + 1
    #                
    #        if unSortedOrders.iloc[i]["Component"] == componentList[0]: #    "Active Horizontal",
     #           if pairFound:
     #               location = (
    #                    (orderLists["Color"] == unSortedOrders.iloc[i]["Color"]) & 
    #                    (orderLists["profileID"] == "VPDPAH2") 
     #                   )
    #                #newOrders = [ unSortedOrders.iloc[i].tolist(),  unSortedOrders.iloc[matchPosition].tolist()   ]
    #                #order1 = [1, "b"]
    #                order1 = unSortedOrders.iloc[i]
    #                order2 = unSortedOrders.iloc[matchPosition]
    #                #orderLists.loc[location, "orders"] = [order1, order2]   #newOrders
    #                orderLists.loc[location, "orders"] = order1   #newOrders
    #                
    #            else:
    #                location = (
    #                    (orderLists["Color"] == unSortedOrders.iloc[i]["Color"]) & 
     #                   (orderLists["profileID"] == "VPDPAH1") 
    #                    )
                    #newOrder = [ unSortedOrders.iloc[i]]
                    #orderLists.loc[location, "orders"] = newOrder

                
            
    #        elif unSortedOrders.iloc[i]["Component"] == componentList[1]: #    "Active Vertical",
     #           jo1 = ""
     #           
     #       elif unSortedOrders.iloc[i]["Component"] == componentList[2]: #    "Inactive Horizontal",
     #           jo2 = ""
     #           
     #       elif unSortedOrders.iloc[i]["Component"] == componentList[3]: #    "Inactive Vertical",
     #           jo3 = ""
            
        
       


        

        # for i, rows in unSortedOrders.iterrows():
        #    print("fullOrder#", unSortedOrders.iloc[i]["fullOrder#"],
        #          "Component", unSortedOrders.iloc[i]["Component"],
        #          "Length", unSortedOrders.iloc[i]["Length"],
        #          "Position", unSortedOrders.iloc[i]["Position"],
        #         "Color", unSortedOrders.iloc[i]["Color"],
        #
        #     )

        # unSortedOrders = pd.DataFrame(columns = ["fullOrder#", "Component", "Length", "Position", "Color"])


    #    for i, rows in orderLists.iterrows():
    #        print("Color", orderLists.iloc[i]["Color"],
    #           "profileID", orderLists.iloc[i]["profileID"],
    #           "orders", orderLists.iloc[i]["orders"],
    #           "highestUsedPosition", orderLists.iloc[i]["highestUsedPosition"]
     #          )


    # orderLists = pd.DataFrame(columns = ["Color","profileID","orders","highestUsedPosition"])


cleanDataFrame()
fillUnsortedOrders()
fillOrderLists()



# print(df)
#print(unsortedOrders)

#for i in range(len(unsortedOrders)):
#    print("fullOrderNum", unsortedOrders[i].fullOrderNum,
#          "component", unsortedOrders[i].component,
#          "length", unsortedOrders[i].length,
#          "position", unsortedOrders[i].position,
#          "color", unsortedOrders[i].color)

for i in range(len(orderLists)):
    print("color", orderLists[i].color,
          "profileID", orderLists[i].profileID,
          "highestUsedPosition", orderLists[i].highestUsedPosition)
    for j in range(len(orderLists[i].orders)):
        print(j,
              "Order1:", orderLists[i].orders[j].order1.fullOrderNum,
              "Order2:", orderLists[i].orders[j].order2.fullOrderNum)
         

  