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

    def genVariable(self):

        if self.mobility == "R":
            self.values = ["1", "2", "3", "4", "13", "14", "15", "16", "17", "18", "19", "20"]
        else:
            for i in range(1, 32):
                self.values.append(str(i))

    def st_print(self):
        print("id: ", self.id)
        print("year: ", self.year)
        print("tr: ", self.trouble)
        print("mob: ", self.mobility)
        print("sib: ", self.sibling)


def readFile(input_file):
    f = open(input_file)
    # Vector of objects from the class Students
    vector = []
    text = f.read()
    list_data = text.split('\n')
    # Save data from text file into the class and the vector
    for item in list_data:
        data = item.split(',')
        my_student = Student(data[0], data[1], data[2], data[3], data[4])
        vector.append(my_student)

    f.close()


def main(inpath):
    readFile(inpath)


if __name__ == "__main__":
    main(sys.argv[1])