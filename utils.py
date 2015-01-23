def tuple_add(a,b):
  return tuple(map(lambda x, y: x + y, a, b))

def tuple_sub(a,b):
  return tuple(map(lambda x, y: x - y, a, b))

def plural(n, s1):
  if n > 1 or n == 0:
    return s1 + 's'
  else:
    return s1

def bits(char, nbits):
  b = ''
  for i in reversed(xrange(nbits)):
    b += str((char >> i) & 1)
  return b