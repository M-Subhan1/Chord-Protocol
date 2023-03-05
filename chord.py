class ChordNode:
    def __init__(self, id, bits):
      self.id = id
      self.bits = bits
      self.max_nodes = 2**bits
      self.finger_table = [self] * self.bits
      self.predecessor = self
      self.successor = self

    def __repr__(self):
      return str(self.id)
    
    def find_successor(self, id):
      curr_node = self
      difference = (id - curr_node.id) % self.max_nodes
      next_node = None

      if difference == 0:
        return curr_node
      
      if id > self.max_nodes - 1:
        return None

      for i in range(self.bits):
        jump = 2**i

        if curr_node.finger_table[i] is None:
          continue

        if jump > difference:
          break

        next_node = curr_node.finger_table[i]
      
      if next_node is None:
        return None
      
      if next_node.id == id:
        return next_node
      
      for i in range(self.bits):
        jump = 2**i
        n = next_node.find_successor((id + jump) % self.max_nodes)

        if n is not None:
          return n

      return None

    def fix_fingers(self):
      for i in range(self.bits):
        jump = 2**i
        self.finger_table[i] = self.successor.find_successor((self.id + jump) % self.max_nodes)

    def join(self, node):
      self.predecessor = None
      self.finger_table[0] = node.find_successor(self.id + 1)
      self.successor = self.finger_table[0]
      self.successor.notify(self)

    def notify(self, node):
      self.predecessor = node

    def stabilize(self):
      x = self.successor.predecessor

      if x is not None and self.id < x.id < self.successor.id:
        self.successor = x
      
      self.successor.notify(self)

class Chord:
  def __init__(self, bits):
    self.bits = bits
    self.max_nodes = 2**bits

  def create_node(self, id):
    return ChordNode(id, self.bits)