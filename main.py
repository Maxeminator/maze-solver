from graphics import Window, Line, Point

def main():

    win=Window(800,600)
    point_1=Point(50,50)
    point_2=Point(100,200)
    line=Line(point_1,point_2)
    win.draw_line(line,"red")
    win.wait_for_close()
    
if __name__ == "__main__":
    main()