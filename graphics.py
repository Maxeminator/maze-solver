from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
    

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win

    def draw(self, x1, y1, x2, y2):
        if self.__win is None:
            return
        self.__x1, self.__y1 = x1, y1
        self.__x2, self.__y2 = x2, y2

        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)))
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), "white")

        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)))
        else:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")

        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)))
        else:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")

        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)))
        else:
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), "white")

    def draw_move(self, to_cell, undo=False):
        cx1 = (self.__x1 + self.__x2) // 2
        cy1 = (self.__y1 + self.__y2) // 2
        cx2 = (to_cell.__x1 + to_cell.__x2) // 2
        cy2 = (to_cell.__y1 + to_cell.__y2) // 2
        color = "gray" if undo else "red"
        self.__win.draw_line(Line(Point(cx1, cy1), Point(cx2, cy2)), color)

class Maze:
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win=None,seed=None):
        self.x1=x1
        self.y1=y1
        self.num_rows=num_rows
        self.num_cols=num_cols
        self.cell_size_x=cell_size_x
        self.cell_size_y=cell_size_y
        self.win=win
        if seed is not None:
            random.seed(seed)
        self.seed=seed
        self.__cells=[]
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()
        
    def __create_cells(self):
        for i in range(self.num_cols):
            cols=[]
            for j in range(self.num_rows):
                cell=Cell(self.win)
                cols.append(cell)
            self.__cells.append(cols)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i,j)

    def __draw_cell(self,i,j):
        x1=self.x1+i*self.cell_size_x
        y1=self.y1+j*self.cell_size_y
        x2=x1+self.cell_size_x
        y2=y1+self.cell_size_y
        if self.win is None:
            return
        self.__cells[i][j].draw(x1,y1,x2,y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        sleep(0.05)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_bottom_wall=False
        self.__draw_cell(0,0)
        self.__cells[-1][-1].has_top_wall=False
        self.__draw_cell(len(self.__cells)-1,len(self.__cells[0])-1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True

        while True:
            next_cells = []

            # проверка непосещённых соседей
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_cells.append((i - 1, j))  # left
            if i < self.num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_cells.append((i + 1, j))  # right
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_cells.append((i, j - 1))  # up
            if j < self.num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_cells.append((i, j + 1))  # down

            if len(next_cells) == 0:
                self.__draw_cell(i, j)
                return

            next_i, next_j = random.choice(next_cells)

            # разрушение стены между текущей и следующей ячейкой
            if next_i == i - 1:  # left
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            elif next_i == i + 1:  # right
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            elif next_j == j - 1:  # up
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            elif next_j == j + 1:  # down
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False

            self.__draw_cell(i, j)
            self.__draw_cell(next_i, next_j)
            self.__break_walls_r(next_i, next_j)
            return

    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__cells[i][j].visited=False

    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        self.__cells[i][j].visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # left
        if i > 0 and not self.__cells[i][j].has_left_wall and not self.__cells[i - 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)

        # right
        if i < self.num_cols - 1 and not self.__cells[i][j].has_right_wall and not self.__cells[i + 1][j].visited:
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)

        # up
        if j > 0 and not self.__cells[i][j].has_top_wall and not self.__cells[i][j - 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)

        # down
        if j < self.num_rows - 1 and not self.__cells[i][j].has_bottom_wall and not self.__cells[i][j + 1].visited:
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j + 1], undo=True)

        return False