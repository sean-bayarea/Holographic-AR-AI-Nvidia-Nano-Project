# initial_setup.py, write the initial setup code here

from userUtils import *
from main import *

''' sample initial setup
stageNoforChange=22
elementsIn22 = [1, 1, 1, 1, 1 ,0] # ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber, ObjNumber, BGNumber
elements = Elements()
elements.addStage(22, elementsIn22)
loginfoprint(printFilename,1,"start")
'''

''' sample initial setup for multiple stages
stageNoforChange=[22, 23]
    elements = Elements()
    elementsIn22 = [1, 1, 1, 1, 1 ,0]# ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber, ObjNumber, BGNumber
    elements.addStage(22, elementsIn22) # to set element for stage_22 with FG change
    elementsIn23 = [1, 1, 1, 1, 1 ,0] # ScriptConditionNumber, GoodyNumber, FGNumber, CUSNumber, ObjNumber, BGNumber
    elements.addStage(23, elementsIn23) # to set element for stage_23 with FG and Cus change.
    loginfoprint(printFilename,1,"start")
'''

##**##

import socket


stageNoforChange=[236, 272, 274, 275, 276]
elements = Elements()
elementsIn236 = [4, 4, 1, 1, 1, 0]
elements.addStage(236, elementsIn236)
elementsIn272 = [4, 4, 1, 1, 1, 0]
elements.addStage(272, elementsIn272)
elementsIn274 = [4, 4, 1, 1, 1, 0]
elements.addStage(274, elementsIn274)
elementsIn275 = [4, 4, 1, 1, 1, 0]
elements.addStage(275, elementsIn275)
elementsIn276 = [4, 4, 1, 1, 1, 0]
elements.addStage(276, elementsIn276)
ele = elements.ElementsDict

# loginfoprint(printFilename,1,'start elements, ele ='+str(ele))
loginfoprint(printFilename, 1, "start")

init_cg_x=[0,0,0,0,0]
init_cg_y=[0,0,0,0,0]
init_fg_x=[0,0,0,0,0]
init_fg_y=[0,0,0,0,0]
init_fg_xScale=[0,0,0,0,0]
init_fg_yScale=[0,0,0,0,0]
#status 0 not selected, 1 selected and moving, 2 ready
pokemon_status=[0,0,0,0,0]
last_pokemon_status=[0,0,0,0,0]
# 0 is undecided, 1 is left side, 2 is right side
pokemon_side=[0,0,0,0,0]
current_status=[0,0,0,0,0]
weapon_status=[0,0,0,0,0]
iterations=[0,0,0,0,0]
error_buffer=[0,0,0,0,0]
confirm_buffer=[0,0,0,0,0]
weapon_speed=[0,0,0,0,0]
last_cg_x=[0,0,0,0,0]
last_fg_x=[0,0,0,0,0]
last_fg_y=[0,0,0,0,0]
script_condition=[1,2,0,3,4]
script_A_condition=[0,0,1,2,3] #B, C, D, ->2,3,4
script_B_condition=[0,1,0,2,3] #A, C, D, -> 1, 3, 4
script_C_condition=[0,1,2,0,3] #A, B, D, -> 1, 2, 4
script_D_condition=[0,1,2,3,0] #A, B, C, -> 1, 2, 3
overall_condition=0
confrim_limit=5
error_limit=20
pokemon_names=['abomasnow', 'charizard', 'magmar', 'pikachu', 'sandslash']
pokemon_score=[140, 170, 80, 50, 70]
move_speed=50
pokemon_num=5
iteration_limit=10
left_x=-580
left_y=0
right_x=580
right_y=0
weapon_left_x=-100
weapon_left_y=-300
weapon_right_x=100
weapon_right_y=-300
# make it a buffer between left and right
mid_x_buffer=8
mid_x_m=330
play_iterations=0
left_side_confirmed=0
right_side_confirmed=0


fg_x=0
fg_y=0
cg_x=0
cg_y=0
time_limit=2
host = '192.168.0.42' #Server ip
port = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_buffer_size=256
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,recv_buffer_size)
s.bind((host, port))
