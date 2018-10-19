#!/usr/bin/python3
import automationhat as hat
from parsec import *
import socket, os

def ft(x): 
  s = str(x)
  s = s if s[-1]=="\n" else s + "\n"
  return bytes(s, encoding="ascii")

line_parser = choice(
    choice(result(string("analog"), hat.analog), result(string("input"), hat.input))
      .skip(space())
      .bind(lambda o: digit()
        .skip(space())
        .bind(lambda i: result(string("read"), o[int(i)].read))),
    choice(result(string("output"), hat.output), result(string("relay"), hat.relay))
      .skip(space())
      .bind(lambda o: digit().parsecmap(lambda i: o[int(i)]))
        .skip(space())
        .bind(lambda o: choice(
            result(string("is_on"), lambda: int(o.is_on())),
          string("write")
            .skip(space())
            .compose(digit().parsecmap(lambda x: lambda: o.write(int(x))))
          ))
    ).skip(eof())

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/tmp/hat_controller_socket")
except OSError:
    pass
s.bind("/tmp/hat_controller_socket")
s.listen(1)
while True:
  conn, addr = s.accept()
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
          conn.send(ft("OK " + str(ret)))
        else:
          conn.send(ft("OK"))
      except Exception as e:
        conn.send(ft("ERROR " + str(e)))

  finally:
    conn.close()

