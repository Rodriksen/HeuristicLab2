import sys
import copy
from time import time
from queue import PriorityQueue


class Student:
    def __init__(self, label, seat):
        self.label = label
        self.seat = seat
        self.trouble = label[2]
        self.reduced = label[3]
        self.flag = label + ": " + str(seat)

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

    def __lt__(self, other):
        if self.f < other.f:
            return True
        return False

    def isFinal(self):
        if self.outside == []:
            return True
        return False

    def findH(self):
        if self.heuristic == "1":
            self.h = len(self.outside)
        elif self.heuristic == "2":
            self.h = 0
            for i in self.outside:
                if i.reduced == "R":
                    self.h += 1

    def moveDisabled(self, disabled, student):
        new = copy.deepcopy(self)
        new.bus.append(disabled.flag)
        new.bus.append(student.flag)
        new.outside.pop(self.outside.index(disabled))
        if (self.outside.index(disabled)) > self.outside.index(student):
            new.outside.pop(self.outside.index(student))
        else:
            new.outside.pop((self.outside.index(student))-1)
        #Multipliers of previous troublesome for reduced mobility
        dis_multiplier = 1
        st_multiplier = 1
        for place in new.multipliers:
            if disabled.seat > place:
                dis_multiplier = dis_multiplier * 2
        #Calculate the cost
        if disabled.trouble == "C":
            new.multipliers.append(disabled.seat)
            for place in new.multipliers:
                if student.seat > place:
                    st_multiplier = st_multiplier * 2
            if student.trouble == "C":
                new.multipliers.append(student.seat)
                new.state_cost = 2 * (1 + new.carry) * 6 * dis_multiplier * st_multiplier + self.state_cost
                new.carry = 1
            else:
                new.state_cost = 2 * (1 + new.carry) * 3 * dis_multiplier * st_multiplier + self.state_cost
                new.carry = 0
        elif student.trouble == "C":
            for place in new.multipliers:
                if student.seat > place:
                    st_multiplier = st_multiplier * 2
            new.multipliers.append(student.seat)
            new.state_cost = 2 * (1 + new.carry) * 3 * dis_multiplier * st_multiplier
            new.carry = 1
        else:
            for place in new.multipliers:
                if student.seat > place:
                    st_multiplier = st_multiplier * 2
            new.state_cost = (1 + new.carry) * 3 * dis_multiplier * st_multiplier
            new.carry = 0

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
            new.g += self.state_cost
        new.state_cost = (self.carry + 1) * multiplier
        new.g += new.state_cost
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
    return vector, text


def main(inpath, heuristic):
    # Read file
    std_vec, input_text = readFile(inpath)

    # Counter for time, we start the timer when the algorithm starts
    start_time = time()

    # Initial state
    init = State([], std_vec, heuristic, 0, 0)
    init.findH()

    # A*
    open_list = PriorityQueue()
    open_list.put(init)

    # Counter for expanded nodes
    expanded_counter = 0
    while not open_list.empty():
        current_state = open_list.get()
        # Check if selected node is final

        if current_state.isFinal():
            end_time = time()
            student_string = inpath.replace(".prob", "") + "-" + heuristic + ".txt"
            stat_string = inpath.replace(".prob", "") + "-" + heuristic + ".stat"
            st_file = open(student_string, "w")
            stat_file = open(stat_string, "w")
            st_file.write("INPUT: {" + input_text + "}\n")
            st_file.write("OUTPUT: {")
            line = ""
            for i in current_state.bus:
                line = line + i + ", "
            line = line.rstrip(", ")
            st_file.write(line + "}")
            st_file.close()
            final_cost = current_state.g
            final_expanded = expanded_counter
            final_time = end_time - start_time
            solution = current_state.bus
            stat_file.write("Final cost: " + str(final_cost) + "\n")
            stat_file.write("Final time: " + str(final_time) + " seconds\n")
            stat_file.write("Expanded nodes: " + str(final_expanded) + "\n")
            stat_file.write("Solution length: " + str(len(current_state.bus)))
            stat_file.close()
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
            open_list.put(child)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
