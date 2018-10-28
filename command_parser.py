#!/usr/bin/python3
import automationhat as hat
from parsy import *

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

command_parser = read_only | read_and_write

