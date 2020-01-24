from room import Room
from player import Player
from world import World

import sys
sys.path.append('../graph/')
from util import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


def get_neighbors(room, visited):
    # print(visited)
    delta = [
        ('w', (-1, 0)),
        ('e', (1, 0)),
        ('s', (0, -1)),
        ('n', (0, 1))
    ]
    neighbors = []
    for direction, (dx, dy) in delta:
        x2, y2 = room.x + dx, room.y + dy
        if (0 <= x2 < len(world.room_grid)) and (0 <= y2 < len(world.room_grid[room.x])):
            neighbor = world.room_grid[x2][y2]
            if not neighbor: continue
            if direction == 'n' and not room.n_to: continue
            elif direction == 's' and not room.s_to: continue
            elif direction == 'w' and not room.w_to: continue
            elif direction == 'e' and not room.e_to: continue
            if f'{neighbor.x},{neighbor.y}' not in visited:
                neighbors.append((direction, neighbor))
    return neighbors


traversal_path = []
reverse_dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', '-': '-'}
walk_stack = Stack()
# we always want to start with the starting room of the world
# walk_stack.push(('n', world.starting_room))
visited = {}
# if we start at any direction for current we wont get an accurate traversal
# we need to use a special identifier to know when to change it
# for that, current needs to be an array so we can change it
current = ['-', world.starting_room]
# print(f'start x: {current[1].x}, y: {current[1].y}')
n = len(room_graph)
nv = 1
while nv < n:
    visited[f'{current[1].x},{current[1].y}'] = current[1]
    neighbors = get_neighbors(current[1], visited)
    # print(neighbors)
    if not neighbors:
        current = walk_stack.pop()
        # current[0] is direction, current[1] is the room itself
        # print(reverse_dirs[current[0]])
        # print(current)
        traversal_path.append(reverse_dirs[current[0]])
        continue
    direction, next_room = random.choice(neighbors)
    current[0] = direction
    # print(direction)
    traversal_path.append(direction)
    # print(current)
    walk_stack.push(current)
    current = [direction, next_room]
    nv += 1

print(traversal_path)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
