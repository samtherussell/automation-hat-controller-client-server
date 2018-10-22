#!/usr/bin/python3
import automationhat as hat
from parsy import *
import socket, os

def encode(x): 
  s = str(x)
  s = s if s[-1]=="\n" else s + "\n"
  return bytes(s, encoding="ascii")

space = string(" ").desc("a space")

analog = string("analog").result(hat.analog)
input = string("input").result(hat.input)
output = string("output").result(hat.output)
relay = string("relay").result(hat.relay)

@generate("read only action")
def read_only():
  port_type = yield (analog | input)
  yield space
  port_number = yield digit.map(int)
  yield space
  yield string("read")
  return port_type[port_number].read

def is_on(port):
  return string("is_on").result(lambda: int(port.is_on()))

def write(port):
  @generate("write action")
  def f():
    yield string("write")
    yield space
    value = yield digit
    return lambda: port.write(int(value))
  return f

@generate("read or write action")
def read_and_write():
  port_type = yield (output | relay)
  yield space
  port_number = yield digit.map(int)
  yield space
  port = port_type[port_number]
  action = yield (is_on(port) | write(port))
  return action

line_parser = read_only | read_and_write

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/tmp/hat_controller_socket")
except OSError:
    pass
s.bind("/tmp/hat_controller_socket")
s.listen(1)
while True:
  conn, addr = s.accept()
  conn.send = lambda x: conn.send(encode(x))
  try:
    while True:
      line = conn.recv(20).decode(encoding="ascii")
      if not line: break

      if len(line) > 0 and line[-1] == '\n':
        line = line[:-1]
      if len(line) < 1:
        continue
      try:
        command = line_parser.parse(line)
        ret = command()
        if ret != None:
          conn.send("OK " + str(ret))
        else:
          conn.send("OK")
      except Exception as e:
        conn.send("ERROR " + str(e))

  finally:
    conn.close()
