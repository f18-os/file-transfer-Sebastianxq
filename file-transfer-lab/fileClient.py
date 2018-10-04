#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive, sendFile, getFile

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("error")
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        sock = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        sock = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        sock.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        sock.close()
        sock = None
        continue
    break

if sock is None:
    print('could not open socket')
    sys.exit(1)


#have the file input be from here?
fileName = input("What is the name of the file you would like to send? (Format like: file.txt")
sendFile(sock,fileName, debug)
