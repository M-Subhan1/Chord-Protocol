class ChordNode:
    def __init__(self, id, bits):
      self.id = id
      self.bits = bits
      self.max_nodes = 2**bits
      self.finger_table = [self] * self.bits
      self.predecessor = self
      self.predecessors = []
      self.successor = self
      self.range_start = (self.id + 1) % self.max_nodes
      self.range_end = self.id

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

    def notify(self, candidate):
        """
        Update node's successor information with candidate node.
        """
        if self.successor is None or (self.range_end < candidate.id <= self.successor.range_start):
            # If node's current successor is None or candidate is between node and its current successor,
            # then set candidate as node's new successor.
            self.successor = candidate

        if candidate.predecessor is None or (candidate.predecessor.range_end < self.id <= candidate.id):
            # If candidate's current predecessor is None or node is between candidate and its current predecessor,
            # then set node as candidate's new predecessor.
            candidate.predecessor = self

        # Update predecessor list of node's successor if necessary.
        self.successor.update_predecessors(candidate)

    def update_predecessors(self, node):
        """
        Update predecessor list with node.
        """
        if node not in self.predecessors:
            self.predecessors.append(node)

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