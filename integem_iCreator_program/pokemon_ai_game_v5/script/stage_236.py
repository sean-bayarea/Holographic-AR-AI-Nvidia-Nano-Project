# this is a stage_236.py file

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
    # get the initial poistion and scale for pokemon and its weapon
    play_iterations +=1
    loginfoprint(printFilename,1,'----------------------------------- play iterations='+str(play_iterations))
    for i in range(pokemon_num):
       # reset all the parameters at the first iteration when entering the stage
       confirm_buffer=[0,0,0,0,0]
       pokemon_status=[0,0,0,0,0]
       pokemon_side=[0,0,0,0,0]
       overall_condition=0
       left_side_confirmed=0
       right_side_confirmed=0
       # flush the old message
       max_msg_size=4096
       loop_iteration=0
       while loop_iteration<50: 
           loginfoprint(printFilename,1,'loop iteration='+str(loop_iteration))
           chunk = s.recv(max_msg_size)
           loop_iteration+=1
           if not chunk:
               break


if timeIdx>1:
    # receive pokemon recognition message from nano client side
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    loginfoprint(printFilename,1,data)
    namesxy_pre=data.split('#')
    if len(namesxy_pre)>1:
        namesxy1=namesxy_pre[0]
        timestr1=namesxy_pre[1]
        stamp_time=float(timestr1)
        current_time=time()
        # calculate the time difference to sync between client and server to get the real-time data.
        time_diff=abs(stamp_time-current_time)
        loginfoprint(printFilename,1,'time diff='+str(time_diff))
        namesxy=namesxy1.split(';')
        loginfoprint(printFilename,1,'namesxy='+str(namesxy))

    current_status=[0,0,0,0,0]

    # only process the data when it is synced with server side and at least one pokemon is detected.
    if len(namesxy)>1 and len(namesxy_pre)>1 and time_diff < time_limit :
        for item in namesxy:
            names2=item.split(':')
            loginfoprint(printFilename,1,names2[0])
            nameStr=str(names2[0])
            if len(names2)>1:
                names3=str(names2[1])
                loginfoprint(printFilename,1,"name3="+names3)
                positions=names3.split(",")
                # record the pokemon x, y position to decide whether it is on the left or right sise.
                pos_x=float(positions[0])
                pos_y=float(positions[1])
                
                for idx1, name in enumerate(pokemon_names):
                    if name==nameStr:
                        pIdx=idx1

                # confirm_buffer to verify for consistant recognition of pokemon for a period of time, which avoids quick wrong recognition
                confirm_buffer[pIdx]+=1
                current_status[pIdx]=1
                loginfoprint(printFilename,1,"pokemon="+str(pokemon_names[pIdx])+",confirm_buffer="+str(confirm_buffer[pIdx]))

                if confirm_buffer[pIdx]> confrim_limit:
                    
                    # decide the pokemon is at left or right side with cetain buffer zone
                    # pokemon_side[pIdx]=2 is the right side, =1 is the left side
                    if pokemon_side[pIdx]==0:
                        if pos_x > mid_x_m:
                            pokemon_side[pIdx]=2
                        else:
                            pokemon_side[pIdx]=1
                    else: # decided before
                        if pokemon_side[pIdx]==1 and pos_x > mid_x_m+mid_x_buffer:
                            pokemon_side[pIdx]==2
                        if pokemon_side[pIdx]==2 and pos_x < mid_x_m-mid_x_buffer:
                            pokemon_side[pIdx]==1
                
                    loginfoprint(printFilename,1,"pokemon="+str(pokemon_names[pIdx])+",side="+str(pokemon_side[pIdx]))
                    if pokemon_status[pIdx]==0: # start to appear for pokemon
                        pokemon_status[pIdx]=1
                        iterations[pIdx]=0

    for i in range(pokemon_num):
        # to remove none existing pokemon
        pokemon_status[i]=pokemon_status[i]*current_status[i]
        loginfoprint(printFilename,1,"pokemon status="+str(pokemon_status))

        if pokemon_status[i]==1: # pokenmon is recognized
            iterations[i]+=1
            if iterations[i] >=1:
                if pokemon_side[i]==1:
                    if script_condition[i]>0: #no magmar pokemon
                        left_side_confirmed=script_condition[i]
                else:
                    if script_condition[i]>0: #no magmar poken
                        right_side_confirmed=script_condition[i]
                
    # when both sides pokemons are ready
    if left_side_confirmed >0 and right_side_confirmed >0:
        loginfoprint(printFilename,1,'first stage transition ='+str(left_side_confirmed))
        # overall_condition number shows the combination for two pokemons, left side pokemon shows in 2nd digit, right side pokemon shows in 1st digit.
        overall_condition=left_side_confirmed*10+right_side_confirmed
        loginfoprint(printFilename,1,'overall condition ='+str(overall_condition))
        # Based on left side pokemon, it will transition to the related stages.
        setSingleScriptTransition(currentStage,left_side_confirmed)
