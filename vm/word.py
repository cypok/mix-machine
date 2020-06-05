from functools import reduce

from vm_errors import *

MAX_BYTE = 64

class Word:
  @staticmethod
  def sign(x):
    return 1 if x >= 0 else -1

  @staticmethod
  def from_dec(num):
    mask = MAX_BYTE - 1  # 1<<6 - 1
    u_num = abs(num)
    return [Word.sign(num)] + [ int((u_num >> shift) & mask) for shift in range(24, -1, -6) ] # 24 = 6 * (5-1)

  @staticmethod
  def norm_2bytes(addr):
    return Word.sign(addr) * (abs(addr) % MAX_BYTE**2)

  def __int__(self):
    return self.word_list[0] * reduce(lambda x,y: (x << 6) | y, self.word_list[1:], 0)

  @staticmethod
  def is_word_list(word_list):
    return  len(word_list) == 6\
            and word_list[0] in (1, -1)\
            and all([ 0 <= byte < MAX_BYTE for byte in word_list[1:6]])

  def __getitem__(self, x):
    if isinstance(x, slice):
      l = max(x.start, 0) if x.start is not None else 0
      r = min(x.stop, 5) if x.stop is not None else 5
      if x.step is not None:
        raise ValueError("unsupported operation")
      new = Word()
      if l == 0:
        new[0] = self[0]
      for i in range(r, max(l - 1, 0), -1):
        new[5 - r + i] = self[i]
      return new
    else:
      return self.word_list[x]

  def __setitem__(self, x, value):
    if isinstance(x, slice):
      l = max(x.start, 0)
      r = min(x.stop, 5)
      word = Word(value)
      if l == 0:
        self[0] = word[0]
      for i in range(r, max(l-1, 0), -1):
        self[i] = word[5 - r + i]
    else:
      self.word_list[x] = value

  def is_zero(self):
    return self.word_list[1:] == ([0] * 5)


  def __eq__(self, cmp_word):
    return self.is_zero() and cmp_word.is_zero() or \
      all(self[i] == cmp_word[i] for i in range(0, 6))

  def __str__(self):
    return reduce(lambda x, y: "%s %02i" % (x, y), self.word_list[1:6], "+" if self[0] == 1 else "-")

  def addr_str(self):
    return "%s %04i %02i %02i %02i" % tuple(["+" if self[0] == 1 else "-", self[1]*MAX_BYTE + self[2]] + self.word_list[3:])

  def __init__(self, obj = None):
    if obj is None:
      self.word_list = [+1, 0, 0, 0, 0, 0]
    elif isinstance(obj, list) or isinstance(obj, tuple):
      self.word_list = list(obj)
    elif isinstance(obj, int):
      self.word_list = self.from_dec(obj)
    elif isinstance(obj, Word):
      self.word_list = obj.word_list[:]
