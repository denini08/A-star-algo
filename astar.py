"""
Ref:
https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
https://datawookie.dev/blog/2019/04/sliding-puzzle-solvable/
https://blog.goodaudience.com/solving-8-puzzle-using-a-algorithm-7b509c331288
http://repositorio.roca.utfpr.edu.br/jspui/bitstream/1/10221/1/PG_COELE_2018_1_03.pdf pag 38
"""


class Node:
    def __init__(self, data, level, fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.level = level
        self.fval = fval
        self.gval = 0
        self.hval = 0

    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x, y = self.find(self.data, '_')
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        val_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level+1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            # swap
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def copy(self, root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find(self, puz, x):
        """ Specifically used to find the position of the blank space """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, size):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """ Accepts the puzzle from the user """
        puz = []
        for _ in range(0, self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self, start, goal):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        h = self.h(start.data, goal)
        g = start.level
        return h, g

    def h(self, start, goal):
        """ Calculates the different between the given puzzles,
        e.g. number of elements out of position """
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def is_solvable(self, matrix):
        # convert the matrix into a list (arr)
        inv_count = 0
        arr = []
        for l in matrix:
            for n in l:
                if n == "_":
                    arr.append(0)
                else:
                    arr.append(n)

        for i in range(len(arr) - 1):
            for j in range(i+1, len(arr)):
                if arr[j] and arr[i] and arr[i] > arr[j]:
                    inv_count += 1

        if (inv_count % 2) == 0:
            print("Puzzle is solvable\n")
        else:
            print("Puzzle is not solvable\n")
            exit(1)

    def done(self):
        print("\n-------DONE-------")
        print("number of steps from beginning to end=%d, f=%d" %
              ((self.closed[-1].gval), self.closed[-1].fval))

        print("Solution:")
        for n in self.closed:
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in n.data:
                for j in i:
                    print(j, end=" ")
                print("")
        print("tam %d" % (len(self.open)))

    def process(self):
        """ Accept Start and Goal Puzzle state"""
        print("Enter the start state matrix, line by line. Use `_` to refer empty space\n")
        ####
        start = self.accept()
        ####
        #start = [['1', '8', '2'], ['_', '4', '3'], ['7', '6', '5']]
        self.is_solvable(start)
        print("Do you want to use the default goal matrix? Y/n")
        if input() in ["S", "s", "Y", "y"]:
            goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '_']]
        else:
            print(
                "Enter the goal state matrix, line by line. Use `_` to refer empty space \n")
            goal = self.accept()

        print("-------START-------")
        for i in start:
            for j in i:
                print(j, end=" ")
            print("")

        start = Node(start, 0, 0)
        h, g = self.f(start, goal)
        start.gval = g
        start.hval = h
        start.fval = g+h
        """ Put the start node in the open list"""
        self.open.append(start)
        print("\n\n")
        while True:
            cur = self.open[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in cur.data:
                for j in i:
                    print(j, end=" ")
                print("")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if(self.h(cur.data, goal) == 0):
                self.closed.append(cur)
                self.done()
                break
            for i in cur.generate_child():
                h, g = self.f(i, goal)
                i.gval = g
                i.hval = h
                i.fval = g+h
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]

            """ sort the opne list based on f value. to get the smallest in the next interation of while True"""
            self.open.sort(key=lambda x: x.fval, reverse=False)


puz = Puzzle(3)
puz.process()
