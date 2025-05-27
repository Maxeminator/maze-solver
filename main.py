from graphics import Window, Maze

def main():

    win=Window(800,600)
    maze_test=Maze(10,10,10,10,10,10,win,0)
    win.wait_for_close()
    
if __name__ == "__main__":
    main()