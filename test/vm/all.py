import unittest
from . import test_read_memory
from . import test_virt_machine
from . import test_execution
from . import test_word
from . import test_word_parser
from . import test_vm_vmtest

def suite():
  return unittest.TestSuite(
    (
      test_read_memory.suite,
      test_virt_machine.suite,
      test_execution.suite,
      test_word.suite,
      test_word_parser.suite,
      test_vm_vmtest.suite
    )
  )

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite())
