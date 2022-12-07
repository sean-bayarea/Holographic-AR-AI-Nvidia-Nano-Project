# this is a stage_275.py file

from userUtils import *
from main import *
from initial_setup import *

''' Function description
#### def gestureRecognize(gestureslist):
# return [verified, gestureLabel, confidenceLevel] Determine gesture based on gesture array
#### def gameJudge(hand1, hand2):    # first arg is label of first hand, return 0 as winner
# return [winnerID] Judge the outcome
#### def recognizeGesture(StageID, ObjID, handID, timePeriod):
# return [verified, GestureId, confidenceLevel] recognize hand gesture in a period, for example 0.1 second.
#### def setSingleScriptTransition(StageID, scriptNo):
# return [verified] set single script transition
#### def ScaleChange(StageID, ObjID, itemID, xScale, yScale):
# return [verified] change scale of picture
#### def TransparencyChange(StageID, ObjID, itemID, transparency):
# return [verified] changes transparency of picture
#### def SetStartLocation(StageID, ObjID, itemID, xstart, ystart):
# return [verified] set the position of one item
#### def SetStartrotAngle(StageID, ObjID, itemID, rotAngle):
# return [verified] Set rotate angle of picture.
#### def GetStartLocation(StageID, ObjID, itemID):
# return [verified,x,y] return position of item
#### def GetStartScale(StageID, ObjID, itemID):
# return [verified,xscale,yscale] return scale of item
#### def GetStartTransparency(StageID, ObjID, itemID):
# return [verified,Transparency] of item
#### def GetTimeIndex(StageID):
# return [verified, TimeIndex] in a stage
#### def GetTime(StageID):
# return [verified, t] in a stage
#### def SetElementNumber(elements,currentStage):
# set element number of different stage into elements class.
#### def getString(cTypeName):
# return [stringName] return a string of goody name
#### def GetGoodyNumList(goodyNumList,modifyByUser):
# return from input goodyNumList, a list contain all the goody num
#### def SetGoodyNum(goodyNumList, modifyByUser):
# no return, set goody number for goody changed by user
#### def SetGoodyNumByName(goodyString,num):
# no return, set the number in the list contains all the goodynumber
#### def increaseGoodyNum(goodyString,num):
# no return, increase the number in the list contains all the goodynumber
#### def decreaseGoodyNum(goodyString,num):
# no return, decrease the number in the list contains all the goodynumber
#### def SetGoodyNum(goodyNumList, modifyByUser):
# no return, set goody number for goody changed by user
#### def GetGoodyNum(goodyString):
# return [goodyNum] get goody number with name
#### def setObjstartLocation(StageID, PI, ObjNo, startx, starty):
# return [verified] set the position of one object, player window
#### def getObjstartLocation(StageID, PI, ObjNo):
# return [verified, x, y] get the position of one object, player window
#### def playSound(soundSrc, status, loop, delay, volume, repeatTimes, repeatIntervalTime):
# soundSrc The absolute address of the sound file
'''

# use BG, FG, CUS or Person?

##**##

verified, timeIdx=GetTimeIndex(currentStage)

if timeIdx==1:
    right_side_confirmed=0

if timeIdx>1:
    right_side_confirmed=overall_condition%10
    script_num1= script_C_condition[right_side_confirmed]
    loginfoprint(printFilename,1,'second stage transition ='+str(right_side_confirmed)+ ",script num="+str(script_num1)+ ",currentStage="+str(currentStage))
    setSingleScriptTransition(currentStage,script_num1)