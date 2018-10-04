#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("Waiting for a file on:", bindAddr)

#Support for multiple clients
while True:
    sock, addr = lsock.accept()

    print("connection rec'd from", addr)


    from framedSock import sendFile, getFile

    if not os.fork():
        print("New child proces, connecting from", addr)
        while True:
            
            dlFile = getFile(sock,debug)
            
            #if debug: print("rec'd: ", f)
            ty = b"thanks for the file!"             # make emphatic!
            framedSend(sock, ty, debug)
            break #takes in one file and calls it a day
        break #needed to break out of temp loop
