#from constraint import *
import sys

class Student:
    def __init__(self, id, year, trouble, mobility, sibling) -> None:
        self.id = id
        self.year = year
        self.trouble = trouble
        self.mobility = mobility
        self.sibling = sibling
        self.values = []

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

    def setSibling(self, std_vector):  # We only execute it if the student has a sibling
        bro = std_vector[(self.sibling)-1]
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


def main(inpath):
    student_vector = readFile(inpath)
    setDomain(student_vector)
    for i in student_vector:
        i.st_print()


if __name__ == "__main__":
    main(sys.argv[1])
