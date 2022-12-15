import random

from constraint import *
import sys


# This class stores the information for each student
class Student:
    def __init__(self, id, year, trouble, mobility, sibling) -> None:
        self.id = id
        self.year = year
        self.trouble = trouble
        self.mobility = mobility
        self.sibling = sibling
        self.values = []
        self.label = str(id) + trouble + mobility

    # Function to set the domain of students without siblings
    def setNoSibling(self):
        if self.year == 1:
            if self.mobility == "R":
                self.values = [1, 2, 3, 4, 13, 14, 15, 16]
            else:
                for i in range(1, 17):
                    self.values.append(i)
        else:
            if self.mobility == "R":
                self.values = [17, 18, 19, 20]
            else:
                for i in range(17, 33):
                    self.values.append(i)

    # Function to set domain of students with siblings
    def setSibling(self, std_vector):
        bro = std_vector[(self.sibling) - 1]
        if self.year > bro.year:
            self.values = [2, 3, 6, 7, 10, 11, 14, 15]
            bro.values = [1, 4, 5, 8, 9, 12, 13, 16]
            if self.mobility == "R":
                self.values = [2, 3, 14, 15]
            if bro.mobility == "R":
                bro.values = [1, 4, 13, 16]
        elif bro.year > self.year:
            bro.values = [2, 3, 6, 7, 10, 11, 14, 15]
            self.values = [1, 4, 5, 8, 9, 12, 13, 16]
            if bro.mobility == "R":
                bro.values = [2, 3, 14, 15]
            elif self.mobility == "R":
                self.values = [1, 4, 13, 16]
        elif self.year == bro.year:
            self.setNoSibling()

    def st_print(self):
        print("id: ", self.id)
        print("year: ", self.year)
        print("tr: ", self.trouble)
        print("mob: ", self.mobility)
        print("sib: ", self.sibling)
        print("values: ", self.values)


def setDomain(student_vector):
    for student in student_vector:
        if student.sibling == 0:
            student.setNoSibling()
        else:
            student.setSibling(student_vector)


# To store the information of the input file in a vector of students
def readFile(input_file):
    f = open(input_file)
    # Vector of objects from the class Students
    vector = []
    text = f.read()
    list_data = text.split('\n')
    # Save data from text file into the class and the vector
    for item in list_data:
        data = item.split(',')
        my_student = Student(int(data[0]), int(data[1]), data[2], data[3], int(data[4]))
        vector.append(my_student)

    f.close()
    return vector


# Constraint to leave seat next to a R.M. empty
def movSeat(seat1, seat2):
    # Consider seat1 is the corresponding to R.M
    if seat1 in (1, 3, 13, 15, 17, 19):
        empty_seat = seat1 + 1
    else:
        empty_seat = seat1 - 1

    return seat2 != empty_seat


# Constraint to avoid sitting R.M  or troublesome students close to troublesome
def trouble(seat1, seat2):
    # Seat1 -> troublesome seat
    # Seat2 -> it cannot be close to seat1
    # The empty_seat vector will be used to indicate all the seats that cannot be
    # occupied by R:M or other troublesome students
    if seat1 in (1, 5, 9, 13, 17, 21, 25, 29):
        empty_seat = [seat1 - 4, seat1 - 3, seat1 + 1, seat1 + 4, seat1 + 5]
    elif seat1 in (4, 8, 12, 16, 20, 24, 28, 32):
        empty_seat = [seat1 - 5, seat1 - 4, seat1 - 1, seat1 + 3, seat1 + 4]
    else:
        empty_seat = [seat1 - 5, seat1 - 4, seat1 - 3, seat1 - 1, seat1 + 1, seat1 + 3, seat1 + 4, seat1 + 5]

    for seat in empty_seat:
        if seat2 == seat:
            return False
    return True


# Constraint to sit siblings together
def sib_together(seat1, seat2):
    if seat1 % 2 == 0:
        sib = seat1 - 1
    else:
        sib = seat1 + 1
    return seat2 == sib


# MAIN FUNCTION
def main(inpath):
    # Vector of students
    student_vector = readFile(inpath)
    # Students domain
    setDomain(student_vector)

    problem = Problem()

    # Vectors of reduced and troublesome students to have simpler constraints
    reduced = []
    troublesome = []
    print("Add variables")
    # Add variables of the problem with corresponding domain
    for st in student_vector:
        problem.addVariable(st.label, st.values)
        if st.mobility == "R":
            reduced.append(st)
        if st.trouble == "C":
            troublesome.append(st)
    print("Add constraints")
    # Add constraints
    # One student per seat
    problem.addConstraint(AllDifferentConstraint())

    # Seat next to reduced student empty
    for red in reduced:
        for st in student_vector:
            problem.addConstraint(movSeat, (red.label, st.label))

    # Troublesome cannot be sit together or near RM
    for tr in troublesome:
        for tr2 in troublesome:
            # If tr and tr2 are siblings this cannot happen
            if tr.id != tr2.sibling:
                problem.addConstraint(trouble, (tr.label, tr2.label))
        for red in reduced:
            problem.addConstraint(trouble, (tr.label, red.label))

    # Siblings together
    for st1 in student_vector:
        for st2 in student_vector:
            if st1.id == st2.sibling:
                if st1.mobility == "X" and st2.mobility == "X":
                    problem.addConstraint(sib_together, (st1.label, st2.label))

    # Solution of the problem
    solutions = problem.getSolutions()
    num_sol = len(solutions)
    filename = inpath.replace(".txt", ".output")
    out = open(filename, "w")
    out.write("Number of solutions: " + str(num_sol) + "\n")
    if num_sol != 0:
        for i in range(0, 5):
            sol = random.randint(0, num_sol)
            out.write("Printing solution: " + str(sol) + "\n")
            out.write(str(solutions[sol]) + "\n")
    out.close()


if __name__ == "__main__":
    main(sys.argv[1])
