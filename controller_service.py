#!/usr/bin/python3
import socket, os
from command_parser import command_parser

def encode(x): 
  s = str(x)
  s = s if s[-1]=="\n" else s + "\n"
  return bytes(s, encoding="ascii")

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/tmp/hat_controller_socket")
except OSError:
    pass
s.bind("/tmp/hat_controller_socket")
s.listen(1)
while True:
  conn, addr = s.accept()
  def send(x):
    conn.send(encode(x))
  try:
    while True:
      line = conn.recv(20).decode(encoding="ascii")
      if not line: break

      if len(line) > 0 and line[-1] == '\n':
        line = line[:-1]
      if len(line) < 1:
        continue
      try:
        command = command_parser.parse(line)
        ret = command()
        if ret != None:
          send("OK " + str(ret))
        else:
          send("OK")
      except Exception as e:
        send("ERROR " + str(e))

  finally:
    conn.close()
