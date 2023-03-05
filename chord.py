from threading import Thread
import time

class ChordNode:
    def __init__(self, id, bits):
        self.state = True
        self.id = id
        self.bits = bits
        self.max_nodes = 2**bits
        self.finger_table = [None] * self.max_nodes
        self.predecessor = None
        self.successor = None
        self.thread = Thread(target=self.start)
        self.thread.start()

    def start(self):
        while True:
            print(f"Node {self.id} is running stabilize and fix_fingers.")
            self.stabilize()
            self.fix_fingers()
            # Run stabilize and fix_fingers every 3 seconds
            time.sleep(3)
        
    def find_successor(self, id):
        if self.id >= self.successor.id:
            if id >= self.id: 
                return self.successor
        elif id > self.id and id <= self.successor.id:
            return self.successor        
        elif self.successor == self:
            return self
        
        for i in range(self.max_nodes-1,1,-1):
            if self.finger_table[i] is not None and self.finger_table[i].id < self.id and self.finger_table[i].id > id:
                node =  self.finger_table[i]
            
        node =  self.successor
        return node.find_successor(id)
    
    def notify(self, node):
        if self.predecessor == None:
            self.predecessor = node
            return
    
        if node.id > self.predecessor.id and node.id < self.id:
            self.predecessor = node

    def join(self, joining_node):
        self.successor = joining_node.find_successor(self.id)
        self.successor.predecessor = self
        
    def stabilize(self):
        node = self.successor.predecessor
        if node == None:
            self.successor.predecessor = self
        else:
            if node.id > self.id and node.id < self.successor.id:
                self.successor = node
            elif self.id > self.successor.id and node.id > self.id:
                self.successor = node
            elif self.id == self.successor.id:
                self.successor = node
        self.successor.notify(self)

    def fix_fingers(self):        
        for i in range(self.bits):
            id = (self.id + 2**i) % self.max_nodes
            self.finger_table[i] = self.find_successor(id)

    def print_finger_table(self):
        print(f"Node {self.id} finger table:")

        for i in range(4):
            if self.finger_table[i] is not None:
                print(f"{self.id} + {2**i} = {self.finger_table[i].id}")

        print("")

class Chord:
    def __init__(self, bits):
        self.bits = bits
        self.root = None
    
    def create_node(self, id):
        node = ChordNode(id, self.bits)

        if self.root == None:
            self.root = node
            node.successor = node
        else:
            node.join(self.root)
            node.stabilize()
            self.root.stabilize()

        print(f"Node {node.id} has joined a Chord network")
        return node

