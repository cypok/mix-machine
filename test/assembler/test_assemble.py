# test_assemble.py

# testing of assemle module

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'assembler'))
from parse_line import *
from assemble import *
from memory import *

def print_memory(mem):
  for idx in range(len(mem)):
    if mem[idx] != Memory.positive_zero():
      print(idx, ":", mem[idx])

class AssembleTestCase(unittest.TestCase):
  def check(self, lines, labels, local_labels, memory_part, start_address, errors,
            literals = None, end_address = None):
    symtable = SymbolTable(labels, local_labels)
    asm = Assembler(symtable)
    asm.end_address = end_address
    asm.run(lines, 2)

    #print_memory(asm.memory.memory)

    self.assertEqual(asm.memory, memory_part)
    self.assertEqual(asm.start_address, start_address)
    self.assertEqual(asm.errors, errors)

    literals = [] if literals is None else literals
    self.assertEqual(symtable.literals, literals)

  def testErrors(self):
    self.check(
      lines = [
        Line(None,          "ENTA", "8F",       1),
        Line(None,          "LDA",  "LABEL",    2),
        Line(None,          "LDA",  "(5)LABEL%",3),
        Line(None,          "HLT",  "64",       4),
        Line(None,          "CON",  "LABEL%",   5),
        Line(None,          "ORIG", "0",        6),
        Line(None,          "NOP",  None,       7),
        Line(None,          "END",  "7B",       8)
      ],
      labels = {},
      local_labels = {},
      memory_part = {
        0: [+1,  1,  0,  0, 2, 5]
      },
      start_address = None,
      errors = [
        (1, InvalidLocalLabelError("8F")),
        (2, InvalidAddrError("LABEL")),
        (3, UnexpectedStrInTheEndError("LABEL%")),
        (5, ExpectedWExpError("LABEL%")),
        (7, RepeatedCellError("0")),
        (8, InvalidLocalLabelError("7B"))
      ]
    )

  def testNoErrors(self):
    self.check(
      lines = [
        Line(None,          "ORIG", "30",                 1),
        Line("7H",          "ENTA", "15",                 2),
        Line(None,          "LD2", "=-2+2=",               3),
        Line("TEMP",        "EQU",  "-2",                 4),
        Line(None,          "HLT",  "=1(2:2)=",    5),
        Line(None,          "CON",  "17314053",           7),
        Line(None,          "END",  "7B",                 8)
      ],
      labels = {
        "TEMP": -2
      },
      local_labels = {
        "7H": [(30, 2)]
      },
      memory_part = {
        30: [+1,  0, 15,  0,  2, 48],
        31: [+1,  0, 34,  0,  5, 10],
        32: [+1,  0, 35,  0,  2,  5],
        33: [+1,  1,  2,  3,  4,  5],
        34: [-1,  0,  0,  0,  0, 0],
        35: [+1,  0,  1,  0,  0,  0]
      },
      start_address = 30,
      errors = [],
      literals = [ (0, -1), (262144, 1) ],
      end_address = 34
    )

  def testSmthSly(self):
    # one line program
    self.check(
      lines = [
        Line(None,          "END",  "0",       1)
      ],
      labels = {},
      local_labels = {},
      memory_part = {
         0: [+1,  0,  0,  0,  0,  0]
      },
      start_address = 0,
      errors = []
    )

    # test locals
    self.check(
      lines = [
        Line("2H",          "ORIG", "10",      1),
        Line("2H",          "ORIG", "2B",      2),
        Line("2H",          "CON",  "2B",      3),
        Line("2H",          "LDA",  "2B",      4),
        Line("2H",          "HLT",  None,      5),
        Line("2H",          "END",  "1",       6)
      ],
      labels = {},
      local_labels = {
        "2H": [(0, 1), (10, 2), (0, 3), (1, 4), (2, 5), (2, 6)]
      },
      memory_part = {
        0: [+1,  0,  0,  0,  0, 10],
        1: [+1,  0,  0,  0,  5,  8],
        2: [+1,  0,  0,  0,  2,  5]
      },
      start_address = 1,
      errors = []
    )

  def testInstructions(self):
    self.check(
      lines = [
        Line(None,  "NOP",    "0",  1  ),
        Line(None,  "ADD",    "0",  2  ),
        Line(None,  "SUB",    "0",  3  ),
        Line(None,  "MUL",    "0",  4  ),
        Line(None,  "DIV",    "0",  5  ),
        Line(None,  "NUM",    "0",  6  ),
        Line(None,  "CHAR",   "0",  7  ),
        Line(None,  "HLT",    "0",  8  ),
        Line(None,  "SLA",    "0",  9  ),
        Line(None,  "SRA",    "0",  10  ),
        Line(None,  "SLAX",   "0",  11  ),
        Line(None,  "SRAX",   "0",  12  ),
        Line(None,  "SLC",    "0",  13  ),
        Line(None,  "SRC",    "0",  14  ),
        Line(None,  "MOVE",   "0",  15  ),
        Line(None,  "LDA",    "0",  16  ),
        Line(None,  "LD1",    "0",  17  ),
        Line(None,  "LD2",    "0",  18  ),
        Line(None,  "LD3",    "0",  19  ),
        Line(None,  "LD4",    "0",  20  ),
        Line(None,  "LD5",    "0",  21  ),
        Line(None,  "LD6",    "0",  22  ),
        Line(None,  "LDX",    "0",  23  ),
        Line(None,  "LDAN",   "0",  24  ),
        Line(None,  "LD1N",   "0",  25  ),
        Line(None,  "LD2N",   "0",  26  ),
        Line(None,  "LD3N",   "0",  27  ),
        Line(None,  "LD4N",   "0",  28  ),
        Line(None,  "LD5N",   "0",  29  ),
        Line(None,  "LD6N",   "0",  30  ),
        Line(None,  "LDXN",   "0",  31  ),
        Line(None,  "STA",    "0",  32  ),
        Line(None,  "ST1",    "0",  33  ),
        Line(None,  "ST2",    "0",  34  ),
        Line(None,  "ST3",    "0",  35  ),
        Line(None,  "ST4",    "0",  36  ),
        Line(None,  "ST5",    "0",  37  ),
        Line(None,  "ST6",    "0",  38  ),
        Line(None,  "STX",    "0",  39  ),
        Line(None,  "STJ",    "0",  40  ),
        Line(None,  "STZ",    "0",  41  ),
        Line(None,  "JBUS",   "0",  42  ),
        Line(None,  "IOC",    "0",  43  ),
        Line(None,  "IN",     "0",  44  ),
        Line(None,  "OUT",    "0",  45  ),
        Line(None,  "JRED",   "0",  46  ),
        Line(None,  "JMP",    "0",  47  ),
        Line(None,  "JSJ",    "0",  48  ),
        Line(None,  "JOV",    "0",  49  ),
        Line(None,  "JNOV",   "0",  50  ),
        Line(None,  "JL",     "0",  51  ),
        Line(None,  "JE",     "0",  52  ),
        Line(None,  "JG",     "0",  53  ),
        Line(None,  "JGE",    "0",  54  ),
        Line(None,  "JNE",    "0",  55  ),
        Line(None,  "JLE",    "0",  56  ),
        Line(None,  "JAN",    "0",  57  ),
        Line(None,  "JAZ",    "0",  58  ),
        Line(None,  "JAP",    "0",  59  ),
        Line(None,  "JANN",   "0",  60  ),
        Line(None,  "JANZ",   "0",  61  ),
        Line(None,  "JANP",   "0",  62  ),
        Line(None,  "J1N",    "0",  63  ),
        Line(None,  "J1Z",    "0",  64  ),
        Line(None,  "J1P",    "0",  65  ),
        Line(None,  "J1NN",   "0",  66  ),
        Line(None,  "J1NZ",   "0",  67  ),
        Line(None,  "J1NP",   "0",  68  ),
        Line(None,  "J2N",    "0",  69  ),
        Line(None,  "J2Z",    "0",  70  ),
        Line(None,  "J2P",    "0",  71  ),
        Line(None,  "J2NN",   "0",  72  ),
        Line(None,  "J2NZ",   "0",  73  ),
        Line(None,  "J2NP",   "0",  74  ),
        Line(None,  "J3N",    "0",  75  ),
        Line(None,  "J3Z",    "0",  76  ),
        Line(None,  "J3P",    "0",  77  ),
        Line(None,  "J3NN",   "0",  78  ),
        Line(None,  "J3NZ",   "0",  79  ),
        Line(None,  "J3NP",   "0",  80  ),
        Line(None,  "J4N",    "0",  81  ),
        Line(None,  "J4Z",    "0",  82  ),
        Line(None,  "J4P",    "0",  83  ),
        Line(None,  "J4NN",   "0",  84  ),
        Line(None,  "J4NZ",   "0",  85  ),
        Line(None,  "J4NP",   "0",  86  ),
        Line(None,  "J5N",    "0",  87  ),
        Line(None,  "J5Z",    "0",  88  ),
        Line(None,  "J5P",    "0",  89  ),
        Line(None,  "J5NN",   "0",  90  ),
        Line(None,  "J5NZ",   "0",  91  ),
        Line(None,  "J5NP",   "0",  92  ),
        Line(None,  "J6N",    "0",  93  ),
        Line(None,  "J6Z",    "0",  94  ),
        Line(None,  "J6P",    "0",  95  ),
        Line(None,  "J6NN",   "0",  96  ),
        Line(None,  "J6NZ",   "0",  97  ),
        Line(None,  "J6NP",   "0",  98  ),
        Line(None,  "JXN",    "0",  99  ),
        Line(None,  "JXZ",    "0",  100  ),
        Line(None,  "JXP",    "0",  101  ),
        Line(None,  "JXNN",   "0",  102  ),
        Line(None,  "JXNZ",   "0",  103  ),
        Line(None,  "JXNP",   "0",  104  ),
        Line(None,  "INCA",   "0",  105  ),
        Line(None,  "DECA",   "0",  106  ),
        Line(None,  "ENTA",   "0",  107  ),
        Line(None,  "ENNA",   "0",  108  ),
        Line(None,  "INC1",   "0",  109  ),
        Line(None,  "DEC1",   "0",  110  ),
        Line(None,  "ENT1",   "0",  111  ),
        Line(None,  "ENN1",   "0",  112  ),
        Line(None,  "INC2",   "0",  113  ),
        Line(None,  "DEC2",   "0",  114  ),
        Line(None,  "ENT2",   "0",  115  ),
        Line(None,  "ENN2",   "0",  116  ),
        Line(None,  "INC3",   "0",  117  ),
        Line(None,  "DEC3",   "0",  118  ),
        Line(None,  "ENT3",   "0",  119  ),
        Line(None,  "ENN3",   "0",  120  ),
        Line(None,  "INC4",   "0",  121  ),
        Line(None,  "DEC4",   "0",  122  ),
        Line(None,  "ENT4",   "0",  123  ),
        Line(None,  "ENN4",   "0",  124  ),
        Line(None,  "INC5",   "0",  125  ),
        Line(None,  "DEC5",   "0",  126  ),
        Line(None,  "ENT5",   "0",  127  ),
        Line(None,  "ENN5",   "0",  128  ),
        Line(None,  "INC6",   "0",  129  ),
        Line(None,  "DEC6",   "0",  130  ),
        Line(None,  "ENT6",   "0",  131  ),
        Line(None,  "ENN6",   "0",  132  ),
        Line(None,  "INCX",   "0",  133  ),
        Line(None,  "DECX",   "0",  134  ),
        Line(None,  "ENTX",   "0",  135  ),
        Line(None,  "ENNX",   "0",  136  ),
        Line(None,  "CMPA",   "0",  137  ),
        Line(None,  "CMP1",   "0",  138  ),
        Line(None,  "CMP2",   "0",  139  ),
        Line(None,  "CMP3",   "0",  140  ),
        Line(None,  "CMP4",   "0",  141  ),
        Line(None,  "CMP5",   "0",  142  ),
        Line(None,  "CMP6",   "0",  143  ),
        Line(None,  "CMPX",   "0",  144  ),
        Line(None,  "FADD",   "0",  145  ),
        Line(None,  "FSUB",   "0",  146  ),
        Line(None,  "FMUL",   "0",  147  ),
        Line(None,  "FDIV",   "0",  148  ),
        Line(None,  "FLOT",   "0",  149  ),
        Line(None,  "FIX",    "0",  150  ),
        Line(None,  "SLB",    "0",  151  ),
        Line(None,  "SRB",    "0",  152  ),
        Line(None,  "JAE",    "0",  153  ),
        Line(None,  "JAO",    "0",  154  ),
        Line(None,  "JXE",    "0",  155  ),
        Line(None,  "JXO",    "0",  156  ),
        Line(None,  "END",    "0",  157  )
      ],
      labels = {},
      local_labels = {},
      memory_part = {
        0 : [+1, 0, 0, 0, 0, 0 ],
        1 : [+1, 0, 0, 0, 5, 1 ],
        2 : [+1, 0, 0, 0, 5, 2 ],
        3 : [+1, 0, 0, 0, 5, 3 ],
        4 : [+1, 0, 0, 0, 5, 4 ],
        5 : [+1, 0, 0, 0, 0, 5 ],
        6 : [+1, 0, 0, 0, 1, 5 ],
        7 : [+1, 0, 0, 0, 2, 5 ],
        8 : [+1, 0, 0, 0, 0, 6 ],
        9 : [+1, 0, 0, 0, 1, 6 ],
        10 : [+1, 0, 0, 0, 2, 6 ],
        11 : [+1, 0, 0, 0, 3, 6 ],
        12 : [+1, 0, 0, 0, 4, 6 ],
        13 : [+1, 0, 0, 0, 5, 6 ],
        14 : [+1, 0, 0, 0, 1, 7 ],
        15 : [+1, 0, 0, 0, 5, 8 ],
        16 : [+1, 0, 0, 0, 5, 9 ],
        17 : [+1, 0, 0, 0, 5, 10 ],
        18 : [+1, 0, 0, 0, 5, 11 ],
        19 : [+1, 0, 0, 0, 5, 12 ],
        20 : [+1, 0, 0, 0, 5, 13 ],
        21 : [+1, 0, 0, 0, 5, 14 ],
        22 : [+1, 0, 0, 0, 5, 15 ],
        23 : [+1, 0, 0, 0, 5, 16 ],
        24 : [+1, 0, 0, 0, 5, 17 ],
        25 : [+1, 0, 0, 0, 5, 18 ],
        26 : [+1, 0, 0, 0, 5, 19 ],
        27 : [+1, 0, 0, 0, 5, 20 ],
        28 : [+1, 0, 0, 0, 5, 21 ],
        29 : [+1, 0, 0, 0, 5, 22 ],
        30 : [+1, 0, 0, 0, 5, 23 ],
        31 : [+1, 0, 0, 0, 5, 24 ],
        32 : [+1, 0, 0, 0, 5, 25 ],
        33 : [+1, 0, 0, 0, 5, 26 ],
        34 : [+1, 0, 0, 0, 5, 27 ],
        35 : [+1, 0, 0, 0, 5, 28 ],
        36 : [+1, 0, 0, 0, 5, 29 ],
        37 : [+1, 0, 0, 0, 5, 30 ],
        38 : [+1, 0, 0, 0, 5, 31 ],
        39 : [+1, 0, 0, 0, 2, 32 ],
        40 : [+1, 0, 0, 0, 5, 33 ],
        41 : [+1, 0, 0, 0, 0, 34 ],
        42 : [+1, 0, 0, 0, 0, 35 ],
        43 : [+1, 0, 0, 0, 0, 36 ],
        44 : [+1, 0, 0, 0, 0, 37 ],
        45 : [+1, 0, 0, 0, 0, 38 ],
        46 : [+1, 0, 0, 0, 0, 39 ],
        47 : [+1, 0, 0, 0, 1, 39 ],
        48 : [+1, 0, 0, 0, 2, 39 ],
        49 : [+1, 0, 0, 0, 3, 39 ],
        50 : [+1, 0, 0, 0, 4, 39 ],
        51 : [+1, 0, 0, 0, 5, 39 ],
        52 : [+1, 0, 0, 0, 6, 39 ],
        53 : [+1, 0, 0, 0, 7, 39 ],
        54 : [+1, 0, 0, 0, 8, 39 ],
        55 : [+1, 0, 0, 0, 9, 39 ],
        56 : [+1, 0, 0, 0, 0, 40 ],
        57 : [+1, 0, 0, 0, 1, 40 ],
        58 : [+1, 0, 0, 0, 2, 40 ],
        59 : [+1, 0, 0, 0, 3, 40 ],
        60 : [+1, 0, 0, 0, 4, 40 ],
        61 : [+1, 0, 0, 0, 5, 40 ],
        62 : [+1, 0, 0, 0, 0, 41 ],
        63 : [+1, 0, 0, 0, 1, 41 ],
        64 : [+1, 0, 0, 0, 2, 41 ],
        65 : [+1, 0, 0, 0, 3, 41 ],
        66 : [+1, 0, 0, 0, 4, 41 ],
        67 : [+1, 0, 0, 0, 5, 41 ],
        68 : [+1, 0, 0, 0, 0, 42 ],
        69 : [+1, 0, 0, 0, 1, 42 ],
        70 : [+1, 0, 0, 0, 2, 42 ],
        71 : [+1, 0, 0, 0, 3, 42 ],
        72 : [+1, 0, 0, 0, 4, 42 ],
        73 : [+1, 0, 0, 0, 5, 42 ],
        74 : [+1, 0, 0, 0, 0, 43 ],
        75 : [+1, 0, 0, 0, 1, 43 ],
        76 : [+1, 0, 0, 0, 2, 43 ],
        77 : [+1, 0, 0, 0, 3, 43 ],
        78 : [+1, 0, 0, 0, 4, 43 ],
        79 : [+1, 0, 0, 0, 5, 43 ],
        80 : [+1, 0, 0, 0, 0, 44 ],
        81 : [+1, 0, 0, 0, 1, 44 ],
        82 : [+1, 0, 0, 0, 2, 44 ],
        83 : [+1, 0, 0, 0, 3, 44 ],
        84 : [+1, 0, 0, 0, 4, 44 ],
        85 : [+1, 0, 0, 0, 5, 44 ],
        86 : [+1, 0, 0, 0, 0, 45 ],
        87 : [+1, 0, 0, 0, 1, 45 ],
        88 : [+1, 0, 0, 0, 2, 45 ],
        89 : [+1, 0, 0, 0, 3, 45 ],
        90 : [+1, 0, 0, 0, 4, 45 ],
        91 : [+1, 0, 0, 0, 5, 45 ],
        92 : [+1, 0, 0, 0, 0, 46 ],
        93 : [+1, 0, 0, 0, 1, 46 ],
        94 : [+1, 0, 0, 0, 2, 46 ],
        95 : [+1, 0, 0, 0, 3, 46 ],
        96 : [+1, 0, 0, 0, 4, 46 ],
        97 : [+1, 0, 0, 0, 5, 46 ],
        98 : [+1, 0, 0, 0, 0, 47 ],
        99 : [+1, 0, 0, 0, 1, 47 ],
        100 : [+1, 0, 0, 0, 2, 47 ],
        101 : [+1, 0, 0, 0, 3, 47 ],
        102 : [+1, 0, 0, 0, 4, 47 ],
        103 : [+1, 0, 0, 0, 5, 47 ],
        104 : [+1, 0, 0, 0, 0, 48 ],
        105 : [+1, 0, 0, 0, 1, 48 ],
        106 : [+1, 0, 0, 0, 2, 48 ],
        107 : [+1, 0, 0, 0, 3, 48 ],
        108 : [+1, 0, 0, 0, 0, 49 ],
        109 : [+1, 0, 0, 0, 1, 49 ],
        110 : [+1, 0, 0, 0, 2, 49 ],
        111 : [+1, 0, 0, 0, 3, 49 ],
        112 : [+1, 0, 0, 0, 0, 50 ],
        113 : [+1, 0, 0, 0, 1, 50 ],
        114 : [+1, 0, 0, 0, 2, 50 ],
        115 : [+1, 0, 0, 0, 3, 50 ],
        116 : [+1, 0, 0, 0, 0, 51 ],
        117 : [+1, 0, 0, 0, 1, 51 ],
        118 : [+1, 0, 0, 0, 2, 51 ],
        119 : [+1, 0, 0, 0, 3, 51 ],
        120 : [+1, 0, 0, 0, 0, 52 ],
        121 : [+1, 0, 0, 0, 1, 52 ],
        122 : [+1, 0, 0, 0, 2, 52 ],
        123 : [+1, 0, 0, 0, 3, 52 ],
        124 : [+1, 0, 0, 0, 0, 53 ],
        125 : [+1, 0, 0, 0, 1, 53 ],
        126 : [+1, 0, 0, 0, 2, 53 ],
        127 : [+1, 0, 0, 0, 3, 53 ],
        128 : [+1, 0, 0, 0, 0, 54 ],
        129 : [+1, 0, 0, 0, 1, 54 ],
        130 : [+1, 0, 0, 0, 2, 54 ],
        131 : [+1, 0, 0, 0, 3, 54 ],
        132 : [+1, 0, 0, 0, 0, 55 ],
        133 : [+1, 0, 0, 0, 1, 55 ],
        134 : [+1, 0, 0, 0, 2, 55 ],
        135 : [+1, 0, 0, 0, 3, 55 ],
        136 : [+1, 0, 0, 0, 5, 56 ],
        137 : [+1, 0, 0, 0, 5, 57 ],
        138 : [+1, 0, 0, 0, 5, 58 ],
        139 : [+1, 0, 0, 0, 5, 59 ],
        140 : [+1, 0, 0, 0, 5, 60 ],
        141 : [+1, 0, 0, 0, 5, 61 ],
        142 : [+1, 0, 0, 0, 5, 62 ],
        143 : [+1, 0, 0, 0, 5, 63 ],
        144 : [+1, 0, 0, 0, 6,  1 ],
        145 : [+1, 0, 0, 0, 6,  2 ],
        146 : [+1, 0, 0, 0, 6,  3 ],
        147 : [+1, 0, 0, 0, 6,  4 ],
        148 : [+1, 0, 0, 0, 6,  5 ],
        149 : [+1, 0, 0, 0, 7,  5 ],
        150 : [+1, 0, 0, 0, 6,  6 ],
        151 : [+1, 0, 0, 0, 7,  6 ],
        152 : [+1, 0, 0, 0, 6, 40 ],
        153 : [+1, 0, 0, 0, 7, 40 ],
        154 : [+1, 0, 0, 0, 6, 47 ],
        155 : [+1, 0, 0, 0, 7, 47 ],
      },
      start_address = 0,
      errors = []
    )
  
  def checkLabels(self, lines, labels, local_labels = {}, literals = [], errors = [], end_address = None):
    symtable = SymbolTable()
    asm = Assembler(symtable)
    asm.run(lines)

    self.assertEqual(symtable.labels, labels)
    self.assertEqual(symtable.local_labels, local_labels)
    self.assertEqual(symtable.literals, literals)
    self.assertEqual(asm.errors, errors)

    if end_address is not None:
      self.assertEqual(asm.end_address, end_address)

  def testGoodLabels(self):
    self.checkLabels(
      lines = [
        Line("PRINTER","EQU","18",1),
        Line("NULL","ORIG","PRINTER",2),
        Line("START","ENTA","4",3),
        Line(None,"NOP",None,4),
        Line(None,"END","START",5)
      ],

      labels = {"NULL" : 0, "START" : 18, "PRINTER" : 18}
    )

    # test locals
    self.checkLabels(
      lines = [
        Line("PRINTER","EQU","18",1),
        Line("NULL","ORIG","PRINTER",2),
        Line("START","ENTA","4",3),
        Line("9H","EQU","547",4),
        Line(None,"ORIG","9B",5),
        Line("TESTLABEL","NOP",None,6),
        Line(None,"ORIG","TESTLABEL",7),
        Line("9H","EQU","745",8),
        Line(None,"ORIG","9B",9),
        Line("TESTLABEL2","NOP",None,10),
        Line(None,"END","START",11)
      ],

      labels = {
        "NULL" : 0,
        "START" : 18,
        "PRINTER" : 18,
        "TESTLABEL" : 547,
        "TESTLABEL2" : 745
      },

      local_labels = {
        "9H" : [(547, 4), (745, 8)]
      },
      
      literals = [],
      errors = [],
      
      end_address = 746
    )

    self.checkLabels(
      lines = [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("0LABEL",      "CON",  "19",         2),
        Line("1LABEL",      "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "0LABEL+10", 4),
        Line("9H",          "LDA",  "=357=",      5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "=357=",      7),
        Line(None,          "ORIG", "100",        8),
        Line("9H",          "HLT",  None,         9),
        Line(None,          "END",  "1000",       10),
      ],
      
      labels = {
        "PRINTER666" : 18,
        "0LABEL" : 0,
        "1LABEL" : 1,
        "9L" : 2,
        "123456789L" : 11
      },
      
      local_labels = {
        "0H" : [(12, 7)],
        "9H" : [(10, 5), (100, 9)]
      },

      literals = [ (357, 1), (357, 1) ],
      
      errors = [],

      end_address = 101
    )

  def testBadLabels(self):
    self.checkLabels(
      lines = [
        Line("NULL","ORIG","3000",1),
        Line("START","ENTA","4",2),
        Line("START","NOP",None,3),
        Line(None, "ORIG", "5000", 4),
        Line(None,"END","START",5)
      ],

      labels = {"NULL" : 0, "START" : 3000},
      
      local_labels = {},
      
      literals = [],

      errors = [
        (3, RepeatedLabelError("START")),
        (4, LineNumberError(5000))
      ]
    )

    self.checkLabels(
      lines = [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("OLABEL",      "CON",  "19",         2),
        Line("123456789L",  "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "1000",       4),
        Line("9H",          "NOP",  None,         5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "PRINTER666", 7),
        Line(None,          "ORIG", "3B",         8),
        Line(None,          "ORIG", "UNKNWN",     9),
        Line(None,          "ORIG", "18%",        10),
        Line("9H",          "HLT",  None,         11),
        Line(None,          "END",  "1000",       12),
      ],

      labels = {
        "PRINTER666" : 18,
        "OLABEL" : 0,
        "9L" : 2,
        "123456789L" : 1
      },
      
      local_labels = {
        "0H" : [(1002, 7)],
        "9H" : [(1000, 5), (1003, 11)]
      },
      
      literals = [],

      errors = [
        (6, RepeatedLabelError("123456789L")),
        (8, InvalidLocalLabelError("3B")),
        (9, ExpectedWExpError("UNKNWN")),
        (10, ExpectedWExpError("18%"))
      ]
    )

    self.checkLabels(
      lines = [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("OLABEL",      "CON",  "19",         2),
        Line("123456789L",  "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "1000",       4),
        Line("9H",          "NOP",  None,         5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "PRINTER666", 7),
        Line(None,          "ORIG", "3998",       8),
        Line("9H",          "NOP",  None,         9),
        Line(None,          "NOP",  "=2=",        10),
        Line(None,          "NOP",  None,         11),
        Line("4001LABEL",   "NOP",  None,         12),
        Line(None,          "END",  "1000",       13),
      ],
      
      labels = {
        "PRINTER666" : 18,
        "OLABEL" : 0,
        "9L" : 2,
        "123456789L" : 1,
        "4001LABEL" : 4001
      },
      
      local_labels = {
        "0H" : [(1002, 7)],
        "9H" : [(1000, 5), (3998, 9)]
      },
      
      literals = [ (2, 1) ],
      
      errors = [
        (6, RepeatedLabelError("123456789L")),
        (11, LineNumberError(4000)),
        (12, LineNumberError(4001)),
        (10, InvalidAddrError(4002)),
        (13, NoFreeSpaceForLiteralsError())
      ]
    )

suite = unittest.makeSuite(AssembleTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
