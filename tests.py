import unittest
from graphics import Maze, Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
        
    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._Maze__cells[0][0].has_bottom_wall,
            False,
        )
        self.assertEqual(
            m1._Maze__cells[num_cols - 1][num_rows - 1].has_top_wall,
            False,
        )
    
    def test_reset_cells_visited(self):
        win = Window(800, 600)
        maze = Maze(0, 0, 3, 3, 20, 20, win, seed=0)

            
        for i in range(maze.num_cols):
            for j in range(maze.num_rows):
                maze._Maze__cells[i][j].visited = True

            
            maze._Maze__reset_cells_visited()

            
        for i in range(maze.num_cols):
            for j in range(maze.num_rows):
                self.assertFalse(maze._Maze__cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()