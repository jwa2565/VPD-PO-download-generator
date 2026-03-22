#I'll have stuff related to optimizing the panel file unit order here
from SturtzFileFormats import lengthCorrectSturtzFormatConverter

from dataclasses import dataclass, field

from datetime import date
today = str(date.today())

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
    
#variables that I don't think will change
stockLength_panelLineal = 157 #   157", 13'-1"   192 #
stockLength_frameLineal = 197 #   197", 16'-5"
stockLength_minLength = 3 #3     #   3" min, the shortest material machine can hold before it fucks up
trim_initial = 1  # 1" initial cut trim   4.5 #
trim_inBetweenCuts =   2  # 2" to account for blade thickness and nailfin offsets #JO VERIFY IN THE GEOMETRYYYYYYYYYY   1 #

componentList = [
    "Active Horizontal", #0
    "Active Vertical",    #1
    "Inactive Horizontal",  #2
    "Inactive Vertical",   #3
]

def calcPanelWidth(frameWidth):
    return (frameWidth / 2.0) - 0.188 +.25 #DELETE THE +.25! Don't add til the end cause it causes headaches and confusion and chaos TRUST ME DUDE

def calcPanelHeight(frameHeight):
    return frameHeight - 2.625 +.25 #DELETE THE +.25! Don't add til the end cause it causes headaches and confusion and chaos TRUST ME DUDE

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

def addRows_VPD(fullOrderNumIn, frameWidth, frameHeight, colorIn, positionIn, typeIn, unsortedOrders):
    panelWidth = calcPanelWidth(frameWidth)
    panelHeight = calcPanelHeight(frameHeight)
    
    #############################component stuff
    #"Active Horizontal", #0
    #"Active Vertical",    #1
    #"Inactive Horizontal",  #2
    #"Inactive Vertical",   #3
    componentsToUse = []
    
    if typeIn == "VPD (P2)": #Active Horizontal, Active Vertical, Inactive Horizontal, Inactive Vertical
        componentsToUse = [0,1,2,3]  
        
    elif typeIn == "VPD Transom":
        componentsToUse = [0] ###########Not correct riht now
        
    elif typeIn == "VPD FrameOnly":
        componentsToUse = [] ########### No panel will be made
        
    elif typeIn == "VPD ActivePanelOnly (ACT PAN)":
        componentsToUse = [0,1] #Active Horizontal, Active Vertical

    elif typeIn == "VPD InactivePanelOnly (INA PAN)":
        componentsToUse = [2,3] #Inactive Horizontal, Inactive Vertical
        
    else: componentsToUse = [0,1,2,3] #if nothing matches, defaults to normal "VPD (P2)"
        
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
        
    return len(componentsToUse)
        
def addDataToOrderLists(pairFound, order1in, matchPosition, unsortedOrders, orderLists):
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
                break

def generateOrderLists(colorsInOrders, orderLists):  # makes all the lists needed, but they're empty 

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

def fillOrderLists(unsortedOrders, orderLists, colorsInOrders): ##Make sure we only use this if there are items in unsortedOrders

    generateOrderLists(colorsInOrders, orderLists)
    
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
        
        addDataToOrderLists(pairFound, order1, matchPosition, unsortedOrders, orderLists)  

def detPanelQRCode(type, color, frameWidthString, frameHeightString):
    panelQRCode = ""
    frameWidth = detFrameWidth(frameWidthString)
    frameHeight = detFrameHeight(frameHeightString)
    
    panelWidth = calcPanelWidth(frameWidth) -.25 #SEEEEEEEEE This is already creating headaches but I'm too lazy to fix everything rn, soooo this is a bandaid for now
    panelHeight = calcPanelHeight(frameHeight) -.25 #SEEEEEEEEE This is already creating headaches but I'm too lazy to fix everything rn, soooo this is a bandaid for now

    if type == "VPD (P2)":
        panelQRCode = panelQRCode + "VPAS"

    elif type == "VPD InactivePanelOnly (INA PAN)":
        panelQRCode = panelQRCode + "VPNS"

    elif type == "VPD ActivePanelOnly (ACT PAN)":
        panelQRCode = panelQRCode + "VPAN"
        
    elif type == "VPD Transom": #For now, assume all transoms are singles
        panelQRCode = panelQRCode + "VPNT"
        
    else: panelQRCode = panelQRCode + "VPAS"
    
    panelQRCode = panelQRCode + color
    panelQRCode = panelQRCode + "****"
    panelQRCode = panelQRCode + lengthCorrectSturtzFormatConverter(panelHeight)
    panelQRCode = panelQRCode + lengthCorrectSturtzFormatConverter(panelWidth)

    return panelQRCode

def fillUnsortedOrders(df, unsortedOrders): 
    for i, rows in df.iterrows():
        
        if df.iloc[i]["Full Scannable Order Number"] == "empty": ##Also mooching off of this function to go ahead and adjust some dataframe parameters if needed
            df.loc[i, "Full Scannable Order Number"] = "order" + str(i + 1)
            
        if df.iloc[i]["Schedule Date"] == "###": #ya ik its not good practice but my brain is exhausted! :')
            df.loc[i, "Schedule Date"] = today
            
        numOfComponents = addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                detFrameWidth(df.iloc[i]["Frame Width"]),
                detFrameHeight(df.iloc[i]["Frame Height"]),
                df.iloc[i]["Color"],
                i + 1,
                df.iloc[i]["Type"],
                unsortedOrders
            ) 
        df.loc[i, "panelComponentsNeeded"] = numOfComponents
        df.loc[i, "panelWelderQRCode"] = detPanelQRCode(df.iloc[i]["Type"], df.iloc[i]["Color"], df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"])

def initializeHighestUsedPosition(orderLists): #the lowest SHOULD be the first position, but I'm checking all just to be safe. Initialization sets Highest Used Position to lowest position
    
    for i in range(len(orderLists)):
        
        if len(orderLists[i].orders) > 0:
            currentLowestUsedPosition = orderLists[i].orders[0].order1.position
        
            for j in range(len(orderLists[i].orders)):
                if orderLists[i].orders[j].order1.position > -1 and orderLists[i].orders[j].order1.position < currentLowestUsedPosition:
                     currentLowestUsedPosition =  orderLists[i].orders[j].order1.position
        
                if orderLists[i].orders[j].order2.position > -1 and orderLists[i].orders[j].order2.position < currentLowestUsedPosition:
                     currentLowestUsedPosition =  orderLists[i].orders[j].order2.position


            orderLists[i].highestUsedPosition = currentLowestUsedPosition

def updateHighestUsedPosition(listToUpdate, position1in, position2in, orderLists):

    highestUsedPosition = position2in
    
    
    if position1in > position2in:
        highestUsedPosition = position1in
        
    orderLists[listToUpdate].highestUsedPosition = highestUsedPosition
    
def mergeToBOTHList(colorsInOrders, orderLists):
    
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

        if orderLists[listIndicesToCheck[0]].highestUsedPosition > 0 and orderLists[listIndicesToCheck[1]].highestUsedPosition > 0:
  
            jToDelete = []
            for j in range(len(orderLists[listIndicesToCheck[0]].orders )  ):
                
                for k in range(len(orderLists[listIndicesToCheck[1]].orders) ):
                    if orderLists[listIndicesToCheck[0]].orders[j].order1.length == orderLists[listIndicesToCheck[1]].orders[k].order1.length:
                        tempOrderSet = OrderSet(order1 = orderLists[listIndicesToCheck[0]].orders[j].order1, order2 = orderLists[listIndicesToCheck[1]].orders[k].order1) 
                        orderLists[listBOTHindex].orders.append(tempOrderSet)   
                        updateHighestUsedPosition(listBOTHindex, tempOrderSet.order1.position, tempOrderSet.order2.position, orderLists)
                        
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
                        updateHighestUsedPosition(listBOTHindex, tempOrderSet.order1.position, tempOrderSet.order2.position, orderLists)

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
              
def cutHorizontalStuff(currentIndex, orderLists, cutList):
    
    panelBarLength = stockLength_panelLineal
    panelBarLength = panelBarLength - trim_initial
    panelBarLength = panelBarLength - trim_inBetweenCuts
    
    horizontalIndeces = [] #Lists that are both horizontal and same color
    for i in range(len(orderLists)):
        tempOrientation = orderLists[i].profileID[5]
        tempQTY = orderLists[i].profileID[6]

        if (orderLists[i].highestUsedPosition > 0 and #has items in the list
        orderLists[i].color == orderLists[currentIndex].color and #same color
        tempOrientation == "H" and           #same orientation
        tempQTY == orderLists[currentIndex].profileID[6]):   #same num of panels, 1 or 2
             horizontalIndeces.append(i)

    tempList = OrderList(
            color = orderLists[currentIndex].color,
            profileID = orderLists[currentIndex].profileID,
            orders = [],
            highestUsedPosition = orderLists[currentIndex].highestUsedPosition)
            

    while ((orderLists[currentIndex].highestUsedPosition > 0) and #orderList has items
    (len(horizontalIndeces) > 0) and #still have horizontalIndeces
    (panelBarLength - orderLists[currentIndex].orders[0].order1.length) > stockLength_minLength): #its a valid cut
     
        panelBarLength = panelBarLength - orderLists[currentIndex].orders[0].order1.length - trim_inBetweenCuts
        updateHighestUsedPosition(currentIndex, orderLists[currentIndex].orders[0].order1.position, orderLists[currentIndex].orders[0].order2.position, orderLists)
        tempSet = OrderSet(
             order1 = orderLists[currentIndex].orders[0].order1,
             order2 = orderLists[currentIndex].orders[0].order2,
             profileID = orderLists[currentIndex].profileID ,
             length = orderLists[currentIndex].orders[0].order1.length)
            

        tempList.orders.append(tempSet)
        orderLists[currentIndex].orders.pop(0)
       
        if len(orderLists[currentIndex].orders) == 0:
            orderLists[currentIndex].highestUsedPosition = -1
            horizontalIndeces.remove(currentIndex)
            
        if len(horizontalIndeces) == 0: #exit while loop like RN
            break 
                
        lowestUsedPosition = orderLists[horizontalIndeces[0]].highestUsedPosition
        currentIndex = horizontalIndeces[0]
        
        for j in range(len(horizontalIndeces)): #find next horizontal index to use
                
            if orderLists[horizontalIndeces[j]].highestUsedPosition > 0 and orderLists[horizontalIndeces[j]].highestUsedPosition < lowestUsedPosition:
                lowestUsedPosition = orderLists[horizontalIndeces[j]].highestUsedPosition
                currentIndex = horizontalIndeces[j]

    if len(tempList.orders) > 0:
        cutList.append(tempList)
        
def cutVerticalStuff(currentIndex, orderLists, cutList):
    
    panelBarLength = stockLength_panelLineal
    panelBarLength = panelBarLength - trim_initial
    #panelBarLength = panelBarLength - trim_inBetweenCuts  #I don't think this one is accurate, so I commented it out
    
    tempList = OrderList(
            color = orderLists[currentIndex].color,
            profileID = orderLists[currentIndex].profileID,
            orders = [],
            highestUsedPosition = orderLists[currentIndex].highestUsedPosition) #this highestUsedPosition might not be accurate, but might not be necessary
            
    while (orderLists[currentIndex].highestUsedPosition > 0 and  #orderList has items
    (panelBarLength - orderLists[currentIndex].orders[0].order1.length)  > stockLength_minLength):  #its a valid cut
        
        panelBarLength = panelBarLength - orderLists[currentIndex].orders[0].order1.length - trim_inBetweenCuts
        updateHighestUsedPosition(currentIndex, orderLists[currentIndex].orders[0].order1.position, orderLists[currentIndex].orders[0].order2.position, orderLists) 
        tempSet = OrderSet(
             order1 = orderLists[currentIndex].orders[0].order1,
             order2 = orderLists[currentIndex].orders[0].order2,
             profileID = orderLists[currentIndex].profileID,
             length = orderLists[currentIndex].orders[0].order1.length)
            
        tempList.orders.append(tempSet)
        orderLists[currentIndex].orders.pop(0)
        
        if len(orderLists[currentIndex].orders) == 0:
            orderLists[currentIndex].highestUsedPosition = -1    

    if len(tempList.orders) > 0:
        cutList.append(tempList)
                            
def beginCutting(orderLists, cutList):
    
    lowestUsedPosition = -1
    lowestUsedPositionIndex = -1

    cutsComplete = True 
    for i in range(len(orderLists)): #This asks if there are any orderLists with items remaining
        if orderLists[i].highestUsedPosition > 0:
                cutsComplete = False
                break
    
    while cutsComplete == False:

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
            cutHorizontalStuff(lowestUsedPositionIndex, orderLists, cutList)
         
        elif orientation == "V": #for vertical stuff
            cutVerticalStuff(lowestUsedPositionIndex, orderLists, cutList) 

        cutsComplete = True #It's like someone that keeps asking "We're done now.... RIGHT??"
        for i in range(len(orderLists)):
            if orderLists[i].highestUsedPosition > 0:
                cutsComplete = False
                break

def optimizeOrders(df):
    
    unsortedOrders: list[OrderInfo] = []
    orderLists: list[OrderList] = []
    cutList: list[OrderList] = []

    fillUnsortedOrders(df, unsortedOrders) #DONE
    colorsInOrders = list({order.color for order in unsortedOrders}) #DONE

    fillOrderLists(unsortedOrders, orderLists, colorsInOrders) #DONE
    initializeHighestUsedPosition(orderLists) #DONE
    mergeToBOTHList(colorsInOrders, orderLists) #I THINK DONE
    initializeHighestUsedPosition(orderLists)
    
    if len(orderLists) > 0:
        beginCutting(orderLists, cutList)

    return cutList