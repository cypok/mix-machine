from parse_line import Line

class ListingLine:
  def __init__(self, addr = None, word = None, line = None):
    self.addr = addr
    self.word = word
    self.line = line

  def addr2str(self):
    if self.addr is not None:
      return str(self.addr)
    else:
      return ""

  def word2str(self):
    sign = "+" if self.word[0] == 1 else "-"
    return "%s %02i %02i %02i %02i %02i" % tuple([sign] + self.word[1:])

  def word2str_addr_bytes(self):
    sign = "+" if self.word[0] == 1 else "-"
    return "%s %04i %02i %02i %02i" % tuple([sign] + [self.word[1]*64 + self.word[2]] + self.word[3:])

  def __str__(self):
    if self.addr is not None:
      return "%4s | %16s | %s" % (self.addr2str(), self.word2str(), self.line)
    else:
      return " "*4 + " | " + " "*16 + " | %s" % (self.addr2str(), self.word2str(), self.line)

  def __eq__(self, other):
    return self.addr == other.addr and self.word == other.word and self.line == other.line

class Listing:
  def __str__(self):
    return reduce(lambda x,y: x + str(y) + '\n', self.lines, "")

  def __init__(self, src_lines, asm_lines, memory, literals, literals_address):
    # None added: so first line will have index 1
    self.lines = list(map(lambda string: ListingLine(line = string.rstrip('\r\n')), src_lines))
    self.asm_lines = asm_lines
    self.memory = memory
    self.literals = literals
    self.literals_address = literals_address
    self.create_listing()

  def init_copy(self, listing):
    self.lines = listing.lines

  def create_listing(self):
    for asm_line in self.asm_lines:
      if asm_line.asm_address is not None:
        self.lines[asm_line.line_number-1].addr = asm_line.asm_address
        self.lines[asm_line.line_number-1].word = self.memory[asm_line.asm_address]
    for literal in self.literals:
      sign = "-" if literal[1] == -1 else ""
      self.lines.append(ListingLine(self.literals_address,  self.memory[self.literals_address], "\tCON\t%s%i" % (sign, literal[0])))
      self.literals_address += 1
