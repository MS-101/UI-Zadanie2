import copy
import time

rows: int
columns: int


class Car:
    def __init__(self, color, size, pos_y, pos_x, is_horizontal):
        self.color = color
        self.size = size
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.is_horizontal = is_horizontal


class StateNode:
    def __init__(self, state, instruction, prev, cost):
        self.state = state
        self.instruction = instruction
        self.prev = prev
        self.cost = cost


class Instruction:
    def __init__(self, direction, color, distance):
        self.direction = direction
        self.color = color
        self.distance = distance


def create_crossroad(state):
    labyrinth = []

    for i in range(0, rows):
        labyrinth.append([None for j in range(0, columns)])

    for picked_car in state:
        if picked_car.is_horizontal is True:
            for i in range(0, picked_car.size):
                labyrinth[picked_car.pos_y - 1][picked_car.pos_x - 1 + i] = picked_car
        else:
            for i in range(0, picked_car.size):
                labyrinth[picked_car.pos_y - 1 + i][picked_car.pos_x - 1] = picked_car

    return labyrinth


def print_crossroad(crossroad):
    for i in range(0, rows):
        for j in range(0, columns):
            if crossroad[i][j] is None:
                print("Empty ", end="")
            else:
                print(crossroad[i][j].color + " ", end="")
        print()


def find_car_by_color(state, color):
    for picked_car in state:
        if picked_car.color == color:
            return picked_car

    return None


def is_state_final(red_car):
    if red_car.pos_x + red_car.size == columns + 1:
        return True
    else:
        return False


def cars_equal(car1, car2):
    if car1.color != car2.color:
        return False

    if car1.size != car2.size:
        return False

    if car1.pos_x != car2.pos_x:
        return False

    if car1.pos_y != car2.pos_y:
        return False

    if car1.is_horizontal != car2.is_horizontal:
        return False

    return True


def states_equal(state1, state2):
    if len(state1) == len(state2):
        for i in range(0, len(state1)):
            if cars_equal(state1[i], state2[i]) is False:
                return False

        return True
    else:
        return False


def state_in_node_arr(state, node_arr):
    for picked_node in node_arr:
        if states_equal(state, picked_node.state) is True:
            return True

    return False


def move(direction, state, moving_car):
    crossroad = create_crossroad(state)

    if direction == "VPRAVO" and moving_car.is_horizontal is True:
        # move right
        if moving_car.pos_x + moving_car.size <= columns \
                and crossroad[moving_car.pos_y - 1][moving_car.pos_x - 1 + moving_car.size - 1 + 1] is None:
            moving_car_index = state.index(moving_car)

            new_state = copy.deepcopy(state)
            new_state[moving_car_index].pos_x += 1

            return new_state
    elif direction == "VLAVO" and moving_car.is_horizontal is True:
        # move left
        if moving_car.pos_x > 1 and crossroad[moving_car.pos_y - 1][moving_car.pos_x - 1 - 1] is None:
            moving_car_index = state.index(moving_car)

            new_state = copy.deepcopy(state)
            new_state[moving_car_index].pos_x -= 1

            return new_state
    elif direction == "DOLE" and moving_car.is_horizontal is False:
        # move down
        if moving_car.pos_y + moving_car.size <= rows \
                and crossroad[moving_car.pos_y - 1 + moving_car.size - 1 + 1][moving_car.pos_x - 1] is None:
            moving_car_index = state.index(moving_car)

            new_state = copy.deepcopy(state)
            new_state[moving_car_index].pos_y += 1

            return new_state
    elif direction == "HORE" and moving_car.is_horizontal is False:
        # move up
        if moving_car.pos_y > 1 and crossroad[moving_car.pos_y - 1 - 1][moving_car.pos_x - 1] is None:
            moving_car_index = state.index(moving_car)

            new_state = copy.deepcopy(state)
            new_state[moving_car_index].pos_y -= 1

            return new_state

    return None


def move_forward(node, moving_car):
    if moving_car.is_horizontal is True:
        # move right
        new_state = move("VPRAVO", node.state, moving_car)

        if new_state is None:
            return None

        new_instruction = Instruction("VPRAVO", moving_car.color, 1)

        new_node = StateNode(new_state, new_instruction, node, node.cost + 1)

        return new_node
    else:
        # move down
        new_state = move("DOLE", node.state, moving_car)

        if new_state is None:
            return None

        new_instruction = Instruction("DOLE", moving_car.color, 1)

        new_node = StateNode(new_state, new_instruction, node, node.cost + 1)

        return new_node


def move_backward(node, moving_car):
    if moving_car.is_horizontal is True:
        # move left
        new_state = move("VLAVO", node.state, moving_car)

        if new_state is None:
            return None

        new_instruction = Instruction("VLAVO", moving_car.color, 1)

        new_node = StateNode(new_state, new_instruction, node, node.cost + 1)

        return new_node
    else:
        # move up
        new_state = move("HORE", node.state, moving_car)

        if new_state is None:
            return None

        new_instruction = Instruction("HORE", moving_car.color, 1)

        new_node = StateNode(new_state, new_instruction, node, node.cost + 1)

        return new_node


def get_path_bfs(starting_state):
    visited_nodes = []
    explored_nodes = []

    # create first node and add its state to visited states
    first_node = StateNode(starting_state, None, None, 0)
    visited_nodes.append(first_node)

    while True:
        # check if there is any visited, unexplored node
        if len(visited_nodes) == 0:
            return None

        # pick visited node
        cur_node = visited_nodes[0]

        # if its state is final return this node
        cur_red_car = find_car_by_color(cur_node.state, "cervene")

        if is_state_final(cur_red_car) is True:
            return cur_node

        # explore node
        for picked_car in cur_node.state:
            # move picked car forward
            new_node = move_forward(cur_node, picked_car)

            if new_node is not None and state_in_node_arr(new_node.state, visited_nodes) is not True \
                    and state_in_node_arr(new_node.state, explored_nodes) is not True:
                visited_nodes.append(new_node)

            # move picked car backward
            new_node = move_backward(cur_node, picked_car)

            if new_node is not None and state_in_node_arr(new_node.state, visited_nodes) is not True \
                    and state_in_node_arr(new_node.state, explored_nodes) is not True:
                visited_nodes.append(new_node)

        # move current node from visited to explored nodes array
        visited_nodes.remove(cur_node)
        explored_nodes.append(cur_node)


def explore_node_dfs(cur_node, visited_nodes, explored_nodes):
    cur_red_car = find_car_by_color(cur_node.state, "cervene")

    if is_state_final(cur_red_car) is True:
        return cur_node

    # explore node
    for picked_car in cur_node.state:
        # move picked car forward
        new_node = move_forward(cur_node, picked_car)

        if new_node is not None and state_in_node_arr(new_node.state, visited_nodes) is not True \
                and state_in_node_arr(new_node.state, explored_nodes) is not True:
            visited_nodes.insert(0, new_node)
            final_node = explore_node_dfs(new_node, visited_nodes, explored_nodes)

            if final_node is not None:
                return final_node

        # move picked car backward
        new_node = move_backward(cur_node, picked_car)

        if new_node is not None and state_in_node_arr(new_node.state, visited_nodes) is not True \
                and state_in_node_arr(new_node.state, explored_nodes) is not True:
            visited_nodes.insert(0, new_node)
            final_node = explore_node_dfs(new_node, visited_nodes, explored_nodes)

            if final_node is not None:
                return final_node

    # move current node from visited to explored nodes array
    visited_nodes.remove(cur_node)
    explored_nodes.append(cur_node)

    return None


def get_path_dfs(starting_state):
    visited_nodes = []
    explored_nodes = []

    # create first node and add its state to visited states
    first_node = StateNode(starting_state, None, None, 0)
    visited_nodes.append(first_node)

    while True:
        # check if there is any visited, unexplored node
        if len(visited_nodes) == 0:
            return None

        # pick visited node
        cur_node = visited_nodes[0]

        # if its state is final return this node
        cur_red_car = find_car_by_color(cur_node.state, "cervene")

        if is_state_final(cur_red_car) is True:
            return cur_node

        # explore node
        for picked_car in cur_node.state:
            # move picked car forward
            new_node = move_forward(cur_node, picked_car)

            if new_node is not None and state_in_node_arr(new_node.state, visited_nodes) is not True \
                    and state_in_node_arr(new_node.state, explored_nodes) is not True:
                visited_nodes.insert(0, new_node)
                final_node = explore_node_dfs(new_node, visited_nodes, explored_nodes)

                if final_node is not None:
                    return final_node

            # move picked car backward
            new_node = move_backward(cur_node, picked_car)

            if new_node is not None and state_in_node_arr(new_node.state, visited_nodes) is not True \
                    and state_in_node_arr(new_node.state, explored_nodes) is not True:
                visited_nodes.insert(0, new_node)
                final_node = explore_node_dfs(new_node, visited_nodes, explored_nodes)

                if final_node is not None:
                    return final_node

        # move current node from visited to explored nodes array
        visited_nodes.remove(cur_node)
        explored_nodes.append(cur_node)


def print_path_instructions(final_path_node):
    cur_path_node = final_path_node

    instructions = []
    instructions_reverse = []

    # create reversed instruction array
    while cur_path_node.instruction is not None:
        instructions_reverse.append(cur_path_node.instruction)
        cur_path_node = cur_path_node.prev

    # reverse the instruction array
    for instruction_index in range(len(instructions_reverse) - 1, -1, -1):
        picked_instruction = instructions_reverse[instruction_index]
        instructions.append(picked_instruction)

    # unify identical instructions
    instruction_index = 0
    for picked_instruction in instructions:
        while instruction_index < len(instructions) - 1:
            next_instruction = instructions[instruction_index + 1]

            if picked_instruction.direction == next_instruction.direction \
                    and picked_instruction.color == next_instruction.color:
                picked_instruction.distance += next_instruction.distance
                instructions.remove(next_instruction)
            else:
                break

        instruction_index += 1

    # print all instructions in order
    for picked_instruction in instructions:
        print(picked_instruction.direction + "(" + picked_instruction.color + ", "
              + str(picked_instruction.distance) + ")")


def print_state(state):
    for picked_car in state:
        if picked_car.is_horizontal is True:
            horizontal_char = "h"
        else:
            horizontal_char = "v"

        print(picked_car.color + " " + str(picked_car.size) + " " + str(picked_car.pos_y) + " " + str(picked_car.pos_x)
              + " " + horizontal_char)


def is_state_legal(state):
    for picked_car in state:
        if picked_car.is_horizontal is True:
            if picked_car.pos_y < 1 or picked_car.pos_y > rows:
                return False

            if picked_car.pos_x < 1 or picked_car.pos_x + picked_car.size - 1 > columns:
                return False
        else:
            if picked_car.pos_y < 1 or picked_car.pos_y + picked_car.size - 1 > rows:
                return False

            if picked_car.pos_x < 1 or picked_car.pos_x > columns:
                return False

    return True


def read_state_from_file(file_name):
    input_file = open("Input/" + file_name, "r")

    state = []

    is_first_line = True
    for line in input_file:
        words = line.split()

        if is_first_line is True:
            global rows
            rows = int(words[0])

            global columns
            columns = int(words[1])

            is_first_line = False
            continue

        color = words[0]
        size = int(words[1])
        pos_y = int(words[2])
        pos_x = int(words[3])
        if words[4] == "h":
            is_horizontal = True
        else:
            is_horizontal = False

        new_car = Car(color, size, pos_y, pos_x, is_horizontal)

        state.append(new_car)

    input_file.close()

    if is_state_legal(state) is True:
        return state
    else:
        return None


startingState = None

while True:
    fileName = input("Zadajte názov vstupného súboru (aj s príponou): ")

    try:
        startingState = read_state_from_file(fileName)

        if startingState is None:
            print("Vstupný súbor je nesprávne sformátovaný.")
            continue
        else:
            break
    except IOError:
        print("Zadaný súbor neexistuje.")
        continue

while True:
    algorithm = input("Zadajte názov algoritmu: ")

    if algorithm == "bfs" or algorithm == "dfs":
        break
    else:
        print("Zadali ste nesprávny názov algoritmu.")
        continue

print()

start = time.time()

finalPathNode = None
if algorithm == "bfs":
    finalPathNode = get_path_bfs(startingState)
elif algorithm == "dfs":
    finalPathNode = get_path_dfs(startingState)

if finalPathNode is not None:
    print("Riešenie:")
    print_path_instructions(finalPathNode)
    print()

    print("Cena cesty: " + str(finalPathNode.cost))
else:
    print("Riešenie nebolo nájdené!")
    print()

end = time.time()

elapsedTime = end - start

print("Výpočet trval " + str(elapsedTime) + " sekúnd.")
