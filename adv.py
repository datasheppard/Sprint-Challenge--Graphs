from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# This is a debugging list to show the path of rooms
# that it is selecting as the nearest room
next_rooms = []

# Create a double ended queue
unvisited = list(range(0,len(world.rooms)))
# Append the starting room to the deque (room 0)
next_room = world.rooms[unvisited[0]]
# Remove the starting room from unvisited (room 0)
unvisited.remove(player.current_room.id)
# While there are still room id's in the unvisited list, loop
while len(unvisited) > 0:
    # Add rooms to a next_rooms list
    # This is for debugging purposes to see the path
    # of target rooms the algorithm takes
    next_rooms.append(next_room)
    # Create a deque for the BFS
    d = deque()
    # Create a visited set for the BFS
    # This will store room id's of visited rooms
    visited = set()
    # Start off by appending the next room as a list
    # This will be the beginning of the path to the next
    # closest unexplored room
    d.append([next_room])
    # While this deque is not empty, loop
    while len(d) > 0:
        # Pop the left side of the deque (Queue like)
        path = d.popleft()
        # Get the last room in the list of the path
        last = path[-1]
        # If the last room in the path is an unvisited room
        # We need to reconstruct the moves in cardinal directions
        # to be able to get to this room through path
        if last.id in unvisited:
            # current room is the first room in the path
            c_room = path[0]
            # For each room in the path following the first
            # We determine the direction to get from the current room in the
            # to the next room in the path
            for room in path[1:]:
                # Create a dictionary where the key is the room in a certain
                # direction, and the value is the direction that room is in
                dic = {world.rooms[c_room.id].get_room_in_direction(x).id:x for x in world.rooms[c_room.id].get_exits()}
                # Using this reversed dictionary, we can pass the room.id to
                # get the direction to move to get to that room id
                # Therefore we can append to the travel path that direction
                traversal_path.append(dic[room.id])
                # Lastly, set the current room to the current target room
                c_room = room
            # Remove the last room's id from unvisited as we have now visited
            # that room and do not need to visit it again
            unvisited.remove(last.id)
            # now the next room will be the last room in the path
            # This moves the source room to the new room that was unvisited
            next_room = last
            # Break the BFS while loop
            break
        # If the last room in the path is NOT in unvisited
        # We need to create paths to all of its exit rooms to look for
        # the next closest unvisited room
        else:
            # So we add the last.id to the visited set so we don't move 
            # backwards and create an infinite loop
            visited.add(last.id)
            # Now we loop through each direction in the last room's exits
            for direction in world.rooms[last.id].get_exits():
                # For each direction, we get the room in that direction
                room_in_dir = last.get_room_in_direction(direction)
                # As long as that room's id is not in visited, we add
                # it to the end of the path, and add this new path to
                # the list of paths in the BFS to check for unvisited rooms
                if room_in_dir.id not in visited:
                    d.append(path+[room_in_dir])

# TRAVERSAL TEST - DO NOT MODIFY
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
