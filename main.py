import copy


columns = 6
rows = 6


class Car:
    def __init__(self, color, size, pos_y, pos_x, is_horizontal):
        self.color = color
        self.size = size
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.is_horizontal = is_horizontal


class StateNode:
    def __init__(self, state, instruction, prev):
        self.state = state
        self.instruction = instruction
        self.prev = prev


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
    # print("checking final state: pos x = " + str(red_car.pos_x))

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


def move_forward(prev_node, moving_car):
    prev_crossroad = create_crossroad(prev_node.state)

    if moving_car.is_horizontal is True:
        # move right
        if moving_car.pos_x + moving_car.size <= columns \
                and prev_crossroad[moving_car.pos_y - 1][moving_car.pos_x - 1 + moving_car.size - 1 + 1] is None:
            moving_car_index = prev_node.state.index(moving_car)
            new_state = copy.deepcopy(prev_node.state)

            new_state[moving_car_index].pos_x += 1

            new_instruction = Instruction("VPRAVO", moving_car.color, 1)

            new_node = StateNode(new_state, new_instruction, prev_node)

            return new_node
    else:
        # move down
        if moving_car.pos_y + moving_car.size <= rows \
                and prev_crossroad[moving_car.pos_y - 1 + moving_car.size - 1 + 1][moving_car.pos_x - 1] is None:
            moving_car_index = prev_node.state.index(moving_car)
            new_state = copy.deepcopy(prev_node.state)

            new_state[moving_car_index].pos_y += 1

            new_instruction = Instruction("DOLE", moving_car.color, 1)

            new_node = StateNode(new_state, new_instruction, prev_node)

            return new_node

    return None


def move_backward(prev_node, moving_car):
    prev_crossroad = create_crossroad(prev_node.state)

    if moving_car.is_horizontal is True:
        # move left
        if moving_car.pos_x > 1 and prev_crossroad[moving_car.pos_y - 1][moving_car.pos_x - 1 - 1] is None:
            moving_car_index = prev_node.state.index(moving_car)
            new_state = copy.deepcopy(prev_node.state)

            new_state[moving_car_index].pos_x -= 1

            new_instruction = Instruction("VLAVO", moving_car.color, 1)

            new_node = StateNode(new_state, new_instruction, prev_node)

            return new_node
    else:
        # move up
        if moving_car.pos_y > 1 and prev_crossroad[moving_car.pos_y - 1 - 1][moving_car.pos_x - 1] is None:
            moving_car_index = prev_node.state.index(moving_car)
            new_state = copy.deepcopy(prev_node.state)

            new_state[moving_car_index].pos_y -= 1

            new_instruction = Instruction("HORE", moving_car.color, 1)

            new_node = StateNode(new_state, new_instruction, prev_node)

            return new_node

    return None


def get_path_bfs(starting_state, red_car):
    visited_nodes = []
    explored_nodes = []

    # create first node and add its state to visited states
    first_state_node = StateNode(starting_state, None, None)
    visited_nodes.append(first_state_node)

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
            new_state_node = move_forward(cur_node, picked_car)

            if new_state_node is not None and state_in_node_arr(new_state_node.state, visited_nodes) is not True \
                    and state_in_node_arr(new_state_node.state, explored_nodes) is not True:
                visited_nodes.append(new_state_node)

            # move picked car backward
            new_state_node = move_backward(cur_node, picked_car)

            if new_state_node is not None and state_in_node_arr(new_state_node.state, visited_nodes) is not True \
                    and state_in_node_arr(new_state_node.state, explored_nodes) is not True:
                visited_nodes.append(new_state_node)

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
        print(picked_car.color + "[" + str(picked_car.pos_y) + ", " + str(picked_car.pos_x) + "]")


car1 = Car("cervene", 2, 3, 2, True)
car2 = Car("oranzove", 2, 1, 1, True)
car3 = Car("zlte", 3, 2, 1, False)
car4 = Car("fialove", 2, 5, 1, False)
car5 = Car("zelene", 3, 2, 4, False)
car6 = Car("svetlomodre", 3, 6, 3, True)
car7 = Car("sive", 2, 5, 5, True)
car8 = Car("tmavomodre", 3, 1, 6, False)

starting_state = [car1, car2, car3, car4, car5, car6, car7, car8]

red_car = find_car_by_color(starting_state, "cervene")

if red_car is not None:
    final_path_node = get_path_bfs(starting_state, red_car)

    if final_path_node is not None:
        print_path_instructions(final_path_node)
    else:
        print("no path was found")
