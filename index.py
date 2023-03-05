from chord import Chord
from time import sleep

network = Chord(bits=4)
node1 = network.create_node(id=1)
node6 = network.create_node(id=6)
node1.print_finger_table()
node6.print_finger_table()
sleep(3)
# create more nodes and join them to the network
# print the finger tables of all nodes

node10 = network.create_node(id=10)
node10.print_finger_table()
sleep(3)
node11 = network.create_node(id=11)
node11.print_finger_table()
