import sys
import copy
from time import time


class Student:
    def __init__(self, label, seat):
        self.label = label
        self.seat = seat
        self.trouble = label[2]
        self.reduced = label[3]
        self.flag = label + str(seat)

    def st_print(self):
        print("label: ", self.label)
        print("seat: ", self.seat)
        print("tr: ", self.trouble)
        print("mob: ", self.reduced)

class State:
    def __init__(self, bus, outside, heuristic, g=0, h=0, f=0):
        self.bus = bus
        self.outside = outside
        self.carry = 0
        self.heuristic = heuristic
        self.multipliers = []
        self.state_cost = 0
        self.g = g
        self.h = h
        self.f = f

    def isFinal(self):
        if self.outside == []:
            return True
        return False

    def findH(self):
        if self.heuristic == "1":
            self.h = len(self.outside)
        elif self.heuristic == "2":
            self.h = 0

    def moveDisabled(self, disabled, student):
        new = copy.deepcopy(self)
        new.bus.append(disabled.flag)
        new.bus.append(student.flag)
        new.outside.pop(self.outside.index(disabled))
        if (self.outside.index(disabled)) > self.outside.index(student):
            new.outside.pop(self.outside.index(student))
        else:
            new.outside.pop((self.outside.index(student))-1)
        #Multipliers of previous troublesome
        multiplier = 1
        for place in new.multipliers:
            if disabled.seat > place:
                multiplier = multiplier * 2
        #Calculate the cost
        if disabled.trouble == "C":
            ...
        elif student.trouble == "C":
            ...
        else:
            ...
        new.state_cost = (1+new.carry)+cost
        new.g += new.state_cost
        new.findH()
        new.f = new.g + new.h
        return new

    def moveNormal(self, student):
        new = copy.deepcopy(self)
        new.bus.append(student.flag)
        new.outside.pop(self.outside.index(student))
        multiplier = 1
        for place in new.multipliers:
            if student.seat > place:
                multiplier = multiplier * 2
        if student.trouble == "X":
            new.carry = 0
        else:
            new.carry = 1
            new.multipliers.append(student.seat)
        new.g += (self.carry+1)*multiplier
        new.findH()
        new.f = new.g + new.h
        return new

    def isEqual(self, other_state):
        if self.bus == other_state.bus:
            return True
        return False


def readFile(input_file):
    f = open(input_file)
    # Vector of objects from the class Students
    vector = []
    text = f.read()
    list_data = text.split(', ')
    # Save data from text file into the class and the vector
    for item in list_data:
        data = item.split(': ')
        my_student = Student(data[0], int(data[1]))
        vector.append(my_student)

    f.close()
    # Vector of students
    return vector


def main(inpath, heuristic):
    # Read file
    std_vec = readFile(inpath)

    # Counter for time
    start_time = time()

    # Initial state
    init = State([], std_vec, heuristic, 0, 0)
    init.findH()

    # A*
    state = init
    open_list = []
    open_list.append(state)
    closed_list = []

    # Counter for expanded nodes
    expanded_counter = 0
    while len(open_list):
        current_state = open_list[0]
        current_index = 0
        index = 0

        # Select node to expand
        for node in open_list:
            if node.f < current_state.f:
                current_state = node
                current_index = index
            index += 1

        closed_list.append(current_state)
        open_list.pop(current_index)

        # Check if selected node is final

        if current_state.isFinal():
            end_time = time()
            final_cost = current_state.g
            final_expanded = expanded_counter
            final_time = end_time - start_time
            solution = current_state.bus
            print("The solution is: " + str(solution))
            print("Final cost: ", final_cost)
            print("Final time: ", final_time)
            print("Expanded nodes: ", final_expanded)
            return solution
        # If not final, expand node
        expanded_counter += 1
        children = []
        for student in current_state.outside:
            if student.reduced == "R":
                for other_student in current_state.outside:
                    if other_student.reduced == "X":
                        children.append(current_state.moveDisabled(student, other_student))
            else:
                children.append(current_state.moveNormal(student))

        for child in children:
            for st in open_list:
                if child.isEqual(st):
                    if child.f < st.f:
                        open_list.remove(st)
            open_list.append(child)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
