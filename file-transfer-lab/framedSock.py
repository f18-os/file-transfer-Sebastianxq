import re
import os

def sendFile(sock, payload, debug=0):
     if debug:
          print("fileSend: sending %d byte file" % len(payload))
          print("the file name typed in is: ",payload)
          print("finding the path")
     try:
          writePayload = open(payload, "rb")

          #debugging
          #print("and that file path is: ", rFilePath)
          #print("reading file!")
     
          length = writePayload.read(100)
          print("length is", length)
          empty = os.stat(payload).st_size == 0
          if (empty):
               print("error, empty file!")
          while (length and not (empty)):
               sock.send(length)
               length = writePayload.read(100)
          #print("file has finished being sent")
          sock.close()
          writePayload.close()
     except IOError:
          print ("File not found, please check your input")

def getFile(sock, debug=0):

  readF = open("CopyFile.txt", "wb")
  length = sock.recv(100)
  while(length):
       readF.write(length)
       length = sock.recv(100)
  print("file copied!")
  readF.close()
  sock.close()
