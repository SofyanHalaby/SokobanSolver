from collections import deque


class Direction:
    up, right, down, left = 'u', 'r', 'd', 'l'

    @staticmethod
    def __iter__():
        return [Direction.right,Direction.left,Direction.up,Direction.down]


class CellType:
    wall, empty, box, goal, done = 'w', 'e', 'b', 'g', 'd'


class SokobanModel:
    def __init__(self, file_path=None, pad=False):
        self.__path = ''
        if file_path is None:
            return
        self.__matrix, self.__position = SokobanModel.__read_file(file_path)
        if pad:
            self.__matrix, self.__position = SokobanModel.__pad_map(self)

    def move(self, direction):
        matrix = SokobanModel.__copy_matrix(self.__matrix)
        r, c = self.__position
        path = self.__path
        new_model = SokobanModel()
        if direction == Direction.up:
            new_model.__matrix, new_model.__position, new_model.__path = \
                SokobanModel.__step_up(matrix, r, c, path)
        if direction == Direction.down:
            new_model.__matrix, new_model.__position, new_model.__path = \
                SokobanModel.__step_down(matrix, r, c, path)
        if direction == Direction.left:
            new_model.__matrix, new_model.__position, new_model.__path = \
                SokobanModel.__step_left(matrix, r, c, path)
        if direction == Direction.right:
            new_model.__matrix, new_model.__position, new_model.__path = \
                SokobanModel.__step_right(matrix, r, c, path)
        return new_model

    def is_goal(self):
        for row in self.__matrix:
            for item in row:
                if item == CellType.goal:
                    return False
        return True

    def identical(self, other):
        return self.__position == other.__position and self.__matrix == other.__matrix

    @property
    def path(self):
        return self.__path

    @property
    def matrix(self):
        return self.__matrix

    @property
    def position(self):
        return self.__position

    @staticmethod
    def __step_right(matrix, r, c, path):
        c1, c2 = c + 1, c + 2
        point1, point2 = (r, c1), (r, c2)
        item1, item2 = matrix[r][c1], matrix[r][c2]
        matrix = SokobanModel.__move(matrix, point1, point2, item1, item2)
        return matrix, point1, path+Direction.right

    @staticmethod
    def __step_left(matrix, r, c, path):
        c1, c2 = c - 1, c - 2
        point1, point2 = (r, c1), (r, c2)
        item1, item2 = matrix[r][c1], matrix[r][c2]
        matrix = SokobanModel.__move(matrix, point1, point2, item1, item2)
        return matrix, point1, path+Direction.left

    @staticmethod
    def __step_up(matrix, r, c, path):
        r1, r2 = r - 1, r - 2
        point1, point2 = (r1, c), (r2, c)
        item1, item2 = matrix[r1][c], matrix[r2][c]
        matrix = SokobanModel.__move(matrix, point1, point2, item1, item2)
        return matrix, point1, path+Direction.up

    @staticmethod
    def __step_down(matrix, r, c, path):
        r1, r2 = r + 1, r + 2
        point1, point2 = (r1, c), (r2, c)
        item1, item2 = matrix[r1][c], matrix[r2][c]
        matrix = SokobanModel.__move(matrix, point1, point2, item1, item2)
        return matrix, point1, path+Direction.down

    @staticmethod
    def __move(matrix, point1, point2, item1, item2):
        (x1, y1), (x2, y2) = point1, point2
        if item1 == CellType.wall:
            matrix = None
        elif item1 == CellType.box:
            matrix[x1][y1] = CellType.empty
            if item2 == CellType.empty:
                matrix[x2][y2] = CellType.box
            elif item2 == CellType.goal:
                matrix[x2][y2] = CellType.done
            else:
                matrix = None
        elif item1 == CellType.done:
            matrix[x1][y1] = CellType.goal
            if item2 == CellType.empty:
                matrix[x2][y2] = CellType.box
            elif item2 == CellType.goal:
                matrix[x2][y2] = CellType.done
            else:
                matrix = None
        return matrix

    @staticmethod
    def __read_file(file_name):
        file = open(file_name)
        lines = file.read().splitlines()
        matrix = [list(line) for line in lines[1:]]
        position = lines[0].split(' ')
        position = (int(position[0]), int(position[1]))
        return matrix, position

    @staticmethod
    def __pad_map(model):
        matrix = SokobanModel.__copy_matrix(model.__matrix)
        for i in range(len(matrix)):
            matrix[i].insert(0, CellType.wall)
            matrix[i].insert(0, CellType.wall)
            matrix[i].append(CellType.wall)
            matrix[i].append(CellType.wall)
        walls = [CellType.wall for _ in range(len(matrix[0]))]
        matrix.insert(0, walls)
        matrix.insert(0, walls)
        matrix.append(walls)
        matrix.append(walls)
        position = (model.__position[0] + 2, model.__position[1] + 2)
        return matrix, position

    @staticmethod
    def __copy_matrix(matrix):
        return [row.copy() for row in matrix]


class SokobanSolver:
    def __init__(self):
        self.sokoban = None
        self.__visited = []
        self.__frontiers = deque()

    def __clear(self):
        self.__visited = []
        self.__frontiers = deque()

    def solve(self, filename='asd.txt'):
        self.sokoban = SokobanModel(filename, True)
        self.__frontiers.append(self.sokoban)
        path = self.__bfs()
        self.__clear()
        return path

    def __bfs(self):
        if len(self.__frontiers) == 0:
            return 'Cannot reach the goal'
        state = self.__frontiers.popleft()
        if state.is_goal():
            return state.path
        for direction in Direction.__iter__():
            new_state = state.move(direction)
            self.__append_state(new_state)
        return self.__bfs()

    def __append_state(self, state):
        if state.matrix is None:
            return
        for s in self.__visited:
            if state.identical(s):
                return
        self.__visited.append(state)
        self.__frontiers.append(state)


class Sokoban:
    def __init__(self, file_path):
        solver = SokobanSolver()
        self.path = solver.solve(file_path)
        self.file_path = file_path

    def __iter__(self):
        model = SokobanModel(self.file_path)
        yield model
        for direction in self.path:
            model = model.move(direction)
            yield model
        raise StopIteration

# glopals: self.sokoban_map, self.__visited, self.__frontiers
# path = solve()
# print("final result path : ", path)
