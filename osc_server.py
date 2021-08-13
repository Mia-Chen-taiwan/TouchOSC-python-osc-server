# python D:\TNUA\python\tuto\osc_server.py
import argparse
import math
import csv
import time
import threading
from pythonosc import dispatcher
from pythonosc import osc_server

############ saving acc data ###########
starttime = time.time()
data = [] # storing all data
# path to save the data
csv_path = 'D:/TNUA/python/tuto/machineLearning/LSTM/data/touchOSC_accxyz.txt'

def print_acc(address, *args):
  print("======================")
  print(f"{address}:{args}")
  data.clear()
  acc = list(args) # turn tuple into list
  # add timestamp to the data
  acc.insert(0, int((time.time() - starttime) * 1000)) 
  for i in acc:
  	data.append(i)

def save_acc():
  for i in range(10):
    time.sleep(0.5) # save data every 0.5 seconds
    print("save")
    print(data)
    with open(csv_path, 'a', encoding='UTF8', newline='') as f:
  	  writer = csv.writer(f)
  	  writer.writerow(data)
  	
t = threading.Thread(target = save_acc)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.0.149", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/accxyz", print_acc)
  t.start()

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
  	