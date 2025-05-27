from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.__root=Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas=Canvas(self.__root, bg="white",width=self.width,height=self.height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running=False


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running=True
        while self.__running:
            self.redraw()
        print("window closed...")
    
    def close(self):
        self.__running=False
    
    def draw_line(self,line,fill_color):
        line.draw(self.__canvas,fill_color)

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Line:
    def __init__(self,point_1,point_2):
        self.point_1=point_1
        self.point_2=point_2

    def draw(self,canvas,fill_color):
        canvas.create_line(self.point_1.x,self.point_1.y,self.point_2.x,self.point_2.y,fill=fill_color,width=2)

class Cell:
    def __init__(self,win=None):
        self.has_left_wall=True
        self.has_right_wall=True
        self.has_top_wall=True
        self.has_bottom_wall=True
        self.visited=False
        self.__x1=-1
        self.__y1=-1
        self.__x2=-1
        self.__y2=-1
        self.__win=win
    
    def draw(self,x1,y1,x2,y2):
        self.__x1=x1
        self.__y1=y1
        self.__x2=x2
        self.__y2=y2
        if self.__win is None:
            return    
        if self.has_left_wall:
            wall=Line(Point(self.__x1,self.__y1),Point(self.__x1,self.__y2))
            self.__win.draw_line(wall,"black")
        else:
            wall=Line(Point(self.__x1,self.__y1),Point(self.__x1,self.__y2))
            self.__win.draw_line(wall,"white")
        if self.has_top_wall:
            wall=Line(Point(self.__x1,self.__y2),Point(self.__x2,self.__y2))
            self.__win.draw_line(wall,"black")
        else:
            wall=Line(Point(self.__x1,self.__y2),Point(self.__x2,self.__y2))
            self.__win.draw_line(wall,"white")
        if self.has_right_wall:
            wall=Line(Point(self.__x2,self.__y1),Point(self.__x2,self.__y2))
            self.__win.draw_line(wall,"black")
        else:
            wall=Line(Point(self.__x2,self.__y1),Point(self.__x2,self.__y2))
            self.__win.draw_line(wall,"white")
        if self.has_bottom_wall:
            wall=Line(Point(self.__x1,self.__y1),Point(self.__x2,self.__y1))
            self.__win.draw_line(wall,"black")
        else:
            wall=Line(Point(self.__x1,self.__y1),Point(self.__x2,self.__y1))
            self.__win.draw_line(wall,"white")

    def draw_move(self,to_cell,undo=False):
        line=Line(Point((self.__x1+self.__x2)/2,(self.__y1+self.__y2)/2),Point((to_cell.__x1+to_cell.__x2)/2,(to_cell.__y1+to_cell.__y2)/2))
        if self.__win is None:
            return
        if undo is False:
            self.__win.draw_line(line,"red")
        else:
            self.__win.draw_line(line,"gray")

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
        self.__cells[i][j].visited=True
        while True:
            next=[]
            if j + 1 < self.num_rows and not self.__cells[i][j+1].visited:
                next.append(("up",i,j+1))
            if j-1>=0 and not self.__cells[i][j-1].visited:
                next.append(("down",i,j-1))
            if i - 1 >= 0 and not self.__cells[i - 1][j].visited:
                next.append(("left", i - 1, j))
            if i+1 < self.num_cols and not self.__cells[i+1][j].visited:
                next.append(("right",i+1,j))
            if len(next)==0:
                self.__draw_cell(i,j)
                return
            else:
                direction,ni,nj=random.choice(next)
                match direction:
                    case "up":
                        self.__cells[i][j].has_top_wall=False
                        self.__cells[ni][nj].has_bottom_wall=False
                    case "right":
                        self.__cells[i][j].has_right_wall=False
                        self.__cells[ni][nj].has_left_wall=False
                    case "left":
                        self.__cells[i][j].has_left_wall=False
                        self.__cells[ni][nj].has_right_wall=False
                    case "down":
                        self.__cells[i][j].has_bottom_wall=False
                        self.__cells[ni][nj].has_top_wall=False
                    case _:
                        return
                    
                self.__draw_cell(i,j)
                self.__draw_cell(ni,nj)
                self.__break_walls_r(ni, nj)
                return

