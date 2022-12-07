#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import sys
import argparse
import random
from datetime import datetime
import time
import socket

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, logUsage

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)


input=videoSource("/dev/video0")
output=videoOutput("display://0")
	
# load the object detection network
net=detectNet(argv=['--model=/home/nvidia/jetson-inference/python/training/detection/ssd/models/pokemon6_one/ssd-mobilenet.onnx','--labels=/home/nvidia/jetson-inference/python/training/detection/ssd/models/pokemon6_one/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'])

print('after load model')


# guess_status 0-> start, 1 -> time is up, 2 -> win
guess_status=0 
pokemon_names=['abomasnow', 'charizard', 'magmar', 'pikachu', 'sandslash']
current_pokemon=random.choice(pokemon_names)
start_time=datetime.now()
start_duration_ms=25000
show_win_time_ms=2000

host='192.168.0.80' #client ip
port = 4005
server = ('192.168.0.42', 4000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buff_size=256
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,buff_size) #limit send socket buffer size
s.bind((host,port))
s.setblocking(0)
send_data_option=True

while True:
	# capture the next image
	img = input.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=args.overlay)

	# print the detections
	#print("detected {:d} objects in image".format(len(detections)))
	msg=""
	for detection in detections:
		#print(detection)
		detected_name=pokemon_names[detection.ClassID-1]
		center_pos=str(detection.Center[0])+","+str(detection.Center[1])
		msg=msg+detected_name+":"+center_pos+";"
	time1=time.time()
	# add time stamp for the message to sync on the server side
	msg=msg+"#"+str(time1)
	if len(detections)>0 and send_data_option: #only send msg when item is detected
		try: # try to avoid sending too many in the buffer, when buffer is full, not sending
			sendnum=s.sendto(msg.encode('utf-8'), server)
			#print("send out number of characters:{:d}".format(sendnum))
			print(msg)
		except:
			print('------------------*********************  Blocking with data')
	

	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("Detected {:s} ".format(msg))
	# print out performance info
	#net.PrintProfilerTimes()

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break

time.sleep(2)
