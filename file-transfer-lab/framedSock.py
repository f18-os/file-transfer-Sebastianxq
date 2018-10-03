import re
import os

def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]
     
rbuf = b""                      # static receive buffer

def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf) # look for colon
             if match:
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr)
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 return payload
         r = sock.recv(100)
         rbuf += r
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))


def sendFile(sock, payload, debug=0):
     if debug: print("fileSend: sending %d byte file" % len(payload))
     #take out os to "smallPath" then attempt an open
     print("finding the path")
     testF = open("test.txt", "rb")
     javaF = open("javaTest.java", "rb")

     #smallPath = os.path.join(direct, "smallFile.txt")
     #smallF = open(smallPath, "rb")
     #emptyF = open(os.path.join(direct, "noSize.txt"), "rb")
     #largeF = open(os.path.join(direct, "large.txt"), "rb")

     print("reading file!")
     length = javaF.read(100)
     if (length == 0):
          print("error, empty or missing file!")
     while (length):
          sock.send(length)
          length = javaF.read(100)
     print("file has finished being sent")
     sock.close()
     javaF.close()

def getFile(sock, debug=0):

  readF = open("rFile.txt", "wb")
  length = sock.recv(100)
  while(length):
       readF.write(length)
       length = sock.recv(100)
  print("file copied!")
  readF.close()
  sock.close()
