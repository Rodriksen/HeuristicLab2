import sys


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


def main(inpath, heuristic):
    # Read file
    std_vec = readFile(inpath)

    # Algo tiene que estar mal
    # Initial state
    init = [std_vec, []]

    # Final state
    fin = [[], std_vec]

    state = init
    open_list = []
    open_list.append(state)
    closed_list = []
    # len(state[0]) == 0 => final state, we reach a solution
    while len(state[0]) and len(open_list):
        closed_list.append(state)
        open_list.remove(state)


    # f(n) = g(n) + h(n)

    if heuristic == "1":
        ...
    elif heuristic == "2":
        ...


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
