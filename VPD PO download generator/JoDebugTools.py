#ok this is me testing how to split code into different files. 
#This was a test but ima just go ahead and use this file tor printing stuff lol
#Calling this my debug toolz

from dataclasses import dataclass, field

@dataclass
class CompletionTrackerUnit:
    position: int
    count: int = 0
    

def printOrderList(orderLists):
    print("Printing orderLists")
    for i in range(len(orderLists)):
        print("color", orderLists[i].color,
              "profileID", orderLists[i].profileID,
              "highestUsedPosition", orderLists[i].highestUsedPosition)
        for j in range(len(orderLists[i].orders)):
            print(j,
                  "Order1:", orderLists[i].orders[j].order1.fullOrderNum,
                  "Order2:", orderLists[i].orders[j].order2.fullOrderNum)
            
def printCutList(cutList):
    
    completionTracker: list[CompletionTrackerUnit] = []
    print("Printing cutList")
    
    for i in range(len(cutList)):
        border = ""
        for j in range(70):
            border = border + str(i+1)
            
        border = border[:70]
            
        print(border)
        print("color", cutList[i].color)
        for j in range(len(cutList[i].orders)):
            print(j,
                  "profileID", cutList[i].orders[j].profileID,
                  "Order1:", cutList[i].orders[j].order1.fullOrderNum,
                  "Order2:", cutList[i].orders[j].order2.fullOrderNum)
            
            matchFound = False
            for k in range(len(completionTracker)):
                if completionTracker[k].position == cutList[i].orders[j].order1.position:
                    matchFound = True
                    completionTracker[k].count = completionTracker[k].count + 1
                    if completionTracker[k].count == 4:
                        print("Unit", completionTracker[k].position, "is Complete!")
                    break
                
            if matchFound == False:
                tempTracker = CompletionTrackerUnit(
                        position = cutList[i].orders[j].order1.position,
                        count = 1
                        )
                completionTracker.append(tempTracker)
                
            if cutList[i].orders[j].order2.fullOrderNum != "":
                matchFound = False
                for k in range(len(completionTracker)):
                    if completionTracker[k].position == cutList[i].orders[j].order2.position:
                        matchFound = True
                        completionTracker[k].count = completionTracker[k].count + 1
                        if completionTracker[k].count == 4:
                            print("Unit", completionTracker[k].position, "is Complete!")
                        break
                
                if matchFound == False:
                    tempTracker = CompletionTrackerUnit(
                            position = cutList[i].orders[j].order2.position,
                            count = 1
                            )
                    completionTracker.append(tempTracker)
        
            
        print(border)

def printUnsortedOrders(unsortedOrders):
    print("Printing unsortedOrders")
    for i in range(len(unsortedOrders)):
        print("fullOrderNum", unsortedOrders[i].fullOrderNum,
              "component", unsortedOrders[i].component,
              "length", unsortedOrders[i].length,
              "position", unsortedOrders[i].position,
              "color", unsortedOrders[i].color)
        
def oFileCutListString(cutList):
    
    completionTracker: list[CompletionTrackerUnit] = []
    
    oFileCutListString = ""
    
    for i in range(len(cutList)):
        border = ""
        for j in range(70):
            border = border + str(i+1)
            
        border = border[:70]
            
        
        oFileCutListString = oFileCutListString + border
        oFileCutListString = oFileCutListString + ";\n"
        
        
        oFileCutListString = oFileCutListString + "color " + cutList[i].color + ";\n"
        for j in range(len(cutList[i].orders)):
            
            oFileCutListString = oFileCutListString + str(j) 
            oFileCutListString = oFileCutListString + " profileID " + str(cutList[i].orders[j].profileID)
            oFileCutListString = oFileCutListString + " Order1: " + str(cutList[i].orders[j].order1.fullOrderNum)
            oFileCutListString = oFileCutListString + " Order2: " + str(cutList[i].orders[j].order2.fullOrderNum) 
            oFileCutListString = oFileCutListString + ";\n"
            
            matchFound = False
            for k in range(len(completionTracker)):
                if completionTracker[k].position == cutList[i].orders[j].order1.position:
                    matchFound = True
                    completionTracker[k].count = completionTracker[k].count + 1
                    if completionTracker[k].count == 4:
                        oFileCutListString = oFileCutListString + "Unit " + str(completionTracker[k].position) + " is Complete!"
                        oFileCutListString = oFileCutListString + ";\n"
                    break
                
            if matchFound == False:
                tempTracker = CompletionTrackerUnit(
                        position = cutList[i].orders[j].order1.position,
                        count = 1
                        )
                completionTracker.append(tempTracker)
                
            if cutList[i].orders[j].order2.fullOrderNum != "":
                matchFound = False
                for k in range(len(completionTracker)):
                    if completionTracker[k].position == cutList[i].orders[j].order2.position:
                        matchFound = True
                        completionTracker[k].count = completionTracker[k].count + 1
                        if completionTracker[k].count == 4:
                            oFileCutListString = oFileCutListString + "Unit " + str(completionTracker[k].position) + " is Complete!"
                            oFileCutListString = oFileCutListString + ";\n"
                        break
                
                if matchFound == False:
                    tempTracker = CompletionTrackerUnit(
                            position = cutList[i].orders[j].order2.position,
                            count = 1
                            )
                    completionTracker.append(tempTracker)

        oFileCutListString = oFileCutListString + str(border)
        oFileCutListString = oFileCutListString + ";\n"
        
    return oFileCutListString