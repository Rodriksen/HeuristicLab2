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
    def __init__(self, bus, outside, heuristic, g=0, h=0):
        self.bus = bus
        self.outside = outside
        self.heuristic = heuristic
        self.g = g
        self.h = h
        self.f = self.g + self.h

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
        print("buses before operation")
        print(self.bus)
        new.bus.append(disabled.flag)
        new.bus.append(student.flag)
        new.outside.pop(self.outside.index(disabled))
        if (self.outside.index(disabled)) > self.outside.index(student):
            new.outside.pop(self.outside.index(student))
        else:
            new.outside.pop((self.outside.index(student))-1)
        new.g += 3
        new.findH()
        print("buses after operation")
        print(self.bus)
        print(new.bus)

        return new

    def moveNormal(self, student):
        new = copy.deepcopy(self)
        print("bus before operation")
        print(self.bus)
        new.bus.append(student.flag)
        new.outside.pop(self.outside.index(student))
        if student.trouble == "X":
            new.g += 1
        else:
            count = 0
            for st in new.outside:
                if st.seat > student.seat:
                    print(str(st.seat) + ">" + str(student.seat))
                    if st.reduced == "R":
                        count += 3
                    elif st.reduced == "X":
                        count += 1
            new.g += count + 1
            print(new.g)
        new.findH()
        print("after operation")
        print(self.bus)
        print(new.bus)

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
            final_cost = current_state.f
            final_expanded = expanded_counter
            final_time = end_time - start_time
            solution = current_state.bus
            print("The solution is: " + str(solution))
            return solution
        # If not final, expand node
        expanded_counter += 1
        print("Bus for iter " + str(expanded_counter))
        print(current_state.bus)
        children = []
        for student in current_state.outside:
            print("student being moved")
            print(student.flag)
            if student.reduced == "R":
                for other_student in current_state.outside:
                    if other_student.reduced == "X":
                        print(student.flag + " is moving with " + other_student.flag)
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
