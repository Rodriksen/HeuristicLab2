import sys
import copy
from time import time
from queue import PriorityQueue


class Student:
    def __init__(self, label, seat):
        self.label = label  # Identifier of the student, for example, '3XR'
        self.seat = seat  # Seat assigned to the student
        self.trouble = label[2]  # See if student is troublesome
        self.reduced = label[3]  # See if it has reduced mobility
        self.flag = label + ": " + str(seat)  # This has the format in which the students are shown in the output


class State:
    def __init__(self, bus, outside, heuristic, g=0, h=0, f=0):
        self.bus = bus  # This is a list of the order the students have entered the bus
        self.outside = outside  # This is a list containing the objects of the students that are outside
        self.carry = 0  # This is needed to make a troublesome produce double cost in the next student
        self.heuristic = heuristic  # This is the heuristic used during all the problem
        self.multipliers = []  # This contains seats of the troublesome that have entered the bus
        self.state_cost = 0  # This is the cost of this state, not the path to this state
        self.g = g  # Cost of the path to this state
        self.h = h  # Heuristic value of the state
        self.f = f  # F value to compare states

    def __lt__(self, other):  # Needed for priority queue
        if self.f < other.f:
            return True
        return False

    def isFinal(self):  # Checks if the state is final, seeing if there are no people outside
        if self.outside == []:
            return True
        return False

    def findH(self):  # Finds heuristic value depending on the selected heuristic function
        if self.heuristic == "1":  # This heuristic is number of students outside
            self.h = len(self.outside)
        elif self.heuristic == "2":  # This heuristic is number of reduced mobility outside
            self.h = 0
            for i in self.outside:
                if i.reduced == "R":
                    self.h += 1
        elif self.heuristic == "3":  # h=0 means that we are searching only based on cost
            self.h = 0

    def moveDisabled(self, disabled, student):
        new = copy.deepcopy(self)  # We need to copy by value because they will have different information
        new.bus.append(disabled.flag)  # Both students enter the bus, first the reduced mobility student
        new.bus.append(student.flag)
        new.outside.pop(self.outside.index(disabled))  # The students are no longer out
        if (self.outside.index(disabled)) > self.outside.index(student):
            new.outside.pop(self.outside.index(student))
        else:
            new.outside.pop((self.outside.index(student))-1)
        #Multipliers of previous troublesome for reduced mobility
        dis_multiplier = 1
        st_multiplier = 1
        for place in new.multipliers: # We need to multiply due to previous troublesome with lower seat
            if disabled.seat > place:
                dis_multiplier = dis_multiplier * 2
        #Calculate the cost
        if disabled.trouble == "C":
            new.multipliers.append(disabled.seat)  # Append the seat to the multipliers to penalize next students
            for place in new.multipliers:  # Now find multiplier of other student, because the other one may affect it
                if student.seat > place:
                    st_multiplier = st_multiplier * 2
            if student.trouble == "C":  # Find the cost for CC
                new.multipliers.append(student.seat)
                new.state_cost = 2 * (1 + new.carry) * 6 * dis_multiplier * st_multiplier + self.state_cost
                new.carry = 1  # Next student's cost will be doubled
            else:  # Find the cost of CX
                new.state_cost = 2 * (1 + new.carry) * 3 * dis_multiplier * st_multiplier + self.state_cost
                new.carry = 0  # Next student's cost will not be doubled
        elif student.trouble == "C":  # Find the cost for XC
            for place in new.multipliers:
                if student.seat > place:
                    st_multiplier = st_multiplier * 2
            new.multipliers.append(student.seat)
            new.state_cost = 2 * (1 + new.carry) * 3 * dis_multiplier * st_multiplier
            new.carry = 1
        else:  # Find the cost for XX
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
            student_string = inpath.replace(".prob", "") + "-" + heuristic + ".output"
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
    error_string = inpath.replace(".prob", "") + "-" + heuristic + ".output"
    error_file = open(error_string, "w")
    error_file.write("No solution was found")
    error_file.close()
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
