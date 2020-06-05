# error codes of interface:
ERR_INVALID_ARGS = (1, "Invalid command line arguments, required one real filename")
ERR_INVALID_INPUT_FILE = (2, "Can't open input file")
ERR_SYNTAX = (3, "Syntax errors in input file")
ERR_VM_INIT = (4, "Errors in input file, can't initialize virtual machine")
ERR_VM_RUN = (5, "Runtime errors occured")

class VMError(Exception):
  def __init__(self, info = None):
    self.info = info

  def __str__(self):
    if self.__doc__ is not None:
      try:
        return self.__doc__ % self.info
      except:
        return self.__doc__
    else:
      return str(self.info)

  def __eq__(self, another):
    return str(self) == str(another)


class InvalidStartAddressError(VMError):
  """Invalid start address in input file (%s)"""

class InvalidIntError(VMError):
  """Invalid integer in input file (%s)"""

class TooShortInputLineError(VMError):
  """Too short line in input, expected 7 integers (%s)"""

class RepeatedAddressError(VMError):
  """This address repeated in input file (%s)"""

class InvalidMixWordError(VMError):
  """Invalid mix-word (%s  %s %s %s %s %s)"""


class InvalidMemAddrError(VMError):
  """Invalid memory address (%s)"""


class UnknownInstructionError(VMError):
  """Invalid mix-instruction at this word (%+2i %02i %02i %02i %02i %02i)"""

class InvalidIndError(VMError):
  """Invalid index part (%s)"""

class InvalidFieldSpecError(VMError):
  """Invalid field specification (%s)"""

class NegativeShiftError(VMError):
  """Shift is invalid for negative number of bytes (%s)"""

class InvalidCurAddrError(VMError):
  """Mix-machine's current address is out of memory range (%s)"""

class InvalidMoveError(VMError):
  """Can't move %s words from %s to %s"""

class InvalidDeviceError(VMError):
  """Device #%s is unsupported"""

class UnsupportedDeviceModeError(VMError):
  """Device doesn't support %s"""

class InvalidCharError(VMError):
  """This char is invalid in mix-machine (%s)"""

class InvaliCharCodeError(VMError):
  """There is no char corresponding to this number (%s)"""

class IOMemRangeError(VMError):
  """Can't read/write %s words from %s to %s"""

class MemReadLockedError(VMError):
  """This memory range is locked for reading (%s..%s)"""

class MemWriteLockedError(VMError):
  """This memory range is locked for writing (%s..%s)"""
