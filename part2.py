import sys
from time import time


class Student:
    def __init__(self, label, seat):
        self.label = label
        self.seat = seat
        self.trouble = label[2]
        self.reduced = label[3]

    def st_print(self):
        print("label: ", self.label)
        print("seat: ", self.seat)
        print("tr: ", self.trouble)
        print("mob: ", self.reduced)


class State:
    def __init__(self, bus, outside, g=0, h=0, parent=None):
        self.bus = bus
        self.outside = outside
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent

    def isFinal(self):
        if self.outside == []:
            return True
        return False

    def findH(self,heuristic):
        if heuristic == "1":
            ...
        elif heuristic == "2":
            ...

    def moveDisabled(state, disabled, student):
        ...

    def moveNormal(state, student):
        ...


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
    return vector

#Cuando guardemos en bus, no guardamos el objeto, sino ya la label y el seat




def main(inpath, heuristic):
    # Read file
    std_vec = readFile(inpath)

    start_time = time()
    # Initial state
    init = State([], std_vec, 0, 0)
    state = init
    open_list = []
    open_list.append(state)
    closed_list = []
    expanded_counter = 0
    # len(state[0]) == 0 => final state, we reach a solution
    while len(open_list):
        current_state = open_list[0]
        current_index = 0
        index = 0
        for node in open_list:
            if node.f < current_state.f:
                current_state = node
                current_index = index
            index += 1

        closed_list.append(current_state)
        open_list.pop(current_index)

        if current_state.isFinal():
            end_time = time()
            final_cost = current_state.f
            final_expanded = expanded_counter
            final_time = end_time - start_time
            solution = current_state.bus

        expanded_counter += 1
        children = []
        for student in current_state.outside:
            if student.reduced == "R":
                for other_student in current_state.outside:
                    if other_student.reduced == "X":
                        children.append(current_state.moveDisabled(student,other_student))
            else:
                children.append(current_state.moveNormal(student))







if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
