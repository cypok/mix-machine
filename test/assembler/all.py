# all.py

# run all tests

import unittest
from . import test_parse_argument
from . import test_parse_line
from . import test_parse_lines
from . import test_symbol_table
from . import test_memory
from . import test_operations
from . import test_assemble
from . import test_complete_programs
from . import test_listing

def suite():
  return unittest.TestSuite((
    test_parse_line.suite,
    test_parse_lines.suite,
    test_symbol_table.suite,
    test_memory.suite,
    test_operations.suite,
    test_parse_argument.suite,
    test_assemble.suite,
    test_complete_programs.suite,
    test_listing.suite
  ))

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite())
