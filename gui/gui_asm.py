import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'assembler'))

from parse_line import *
from assemble import *
from listing import *
#from errors import *

# types of returning value
NO_ERRORS =         0
SYNTAX_ERRORS =     1
ASSEMBLER_ERRORS =  2

class AsmData:
  def __init__(self, mem_dict, start_addr, listing):
    self.mem_dict = mem_dict
    self.start_addr = start_addr
    self.listing = listing

def asm(text):
  src_lines = text.splitlines()

  lines, errors = parse_lines(src_lines)
  if len(errors) > 0: # we have errors
    return (SYNTAX_ERRORS, errors)

  asm = Assembler()
  asm.run(lines)

  memory_table = asm.memory
  start_address = asm.start_address
  errors = asm.errors

  if len(errors) > 0: # we have errors
    return (ASSEMBLER_ERRORS, errors)

  listing = Listing(src_lines, lines, memory_table.memory, asm.symtable.literals, asm.end_address)

  return (NO_ERRORS, AsmData(memory_table, start_address, listing))