from graphics import Window, Maze

def main():

    win=Window(800,600)
    maze_test=Maze(0,0,10,10,10,10,win)
    maze_test.solve()
    win.wait_for_close()
    
if __name__ == "__main__":
    main()