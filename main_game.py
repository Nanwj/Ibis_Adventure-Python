"""
Nan Yang 
"""
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
from tkinter import filedialog

__author__ = "{{Nan Yang}}"
__email__ = "nan0406021179@gmail.com"
__date__ = "06/10/2020"


TASK_ONE = "TASK_ONE"
TASK_TWO = "TASK_TWO"
MASTER = "MASTER"
DIRECTIONS = {"W":(-1, 0), "S":(1, 0), "D":(0, 1), "A":(0, -1)}
GAME_LEVELS = {"game1.txt":7,"game2.txt":12,"game3.txt": 19}
PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
 
def load_game(filename):
    """Create a 2D array of string representing the dungeon to display.
    
    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the 
            dungeon.
    """
    dungeon_layout = []

    with open(filename, 'r') as file:
        file_contents = file.readlines()

    for i in range(len(file_contents)):
        line = file_contents[i].strip()
        row = []
        for j in range(len(file_contents)):
            row.append(line[j])
        dungeon_layout.append(row)
    
    return dungeon_layout

class Entity(object):
    """ """
    def __init__(self):
        """
        Something the player can interact with
        """
        super().__init__()
        self._id = "Entity"
        self._collide = True
        
    def get_id(self):
        """ """
        return self._id

    def set_collide(self, collidable):
        """ """
        self._collide = collidable

    def can_collide(self):
        """ """
        return self._collide

    def get_text(self):
        """ """
        return self._text

    def __str__(self):
        return f"{self.__class__.__name__}({self._id!r})"

    def __repr__(self):
        return str(self)

class Wall(Entity):
    """ """
    def __init__(self):
        """ """
        super().__init__()
        self._id = "#"
        self._text = ""
        self._collide = False
    
class Item(Entity):
    """ """
    def on_hit(self, game):
        """ """
        raise NotImplementedError
    
class Key(Item):
    """ """    
    def __init__(self):
        """ """
        super().__init__()
        self._id = "K"
        self._text = "Trash"
        
    def on_hit(self, game):
        """ """
        game.get_player().add_item(self)
        game._game_information.pop(game.get_positions(KEY)[0])
        
class MoveIncrease(Item):
    """ """   
    def __init__(self, moves = 5):
        """ """
        super().__init__()
        self._id = "M"
        self._text = "Banana"
        self._moves = moves
        
    def on_hit(self, game):
        """ """
        game.get_player().change_move_count(self._moves)
        game._game_information.pop(game.get_positions(MOVE_INCREASE)[0])
        
class Door(Entity):
    """ """
    def __init__(self):
        """ """
        super().__init__()
        self._id = "D"
        self._text = "Nest"
        
    def on_hit(self, game):
        """ """
        player = game.get_player()
        for item in player.get_inventory():
            if item.get_id() == KEY:
                game._game_information.pop(game.get_positions(DOOR)[0])
                game.set_win(True)
                return None
        tk.messagebox.showinfo("Prompt","You don't have the key")
            
class Player(Entity):
    """ """   
    def __init__(self, move_count):
        """ """
        super().__init__()
        self._id = "O"
        self._text = "Ibis"
        self._move_count = move_count
        self._inventory = []
        self._position = None
        
    def set_position(self, position):
        """ """
        self._position = position
        
    def get_position(self):
        """ """
        return self._position
    
    def change_move_count(self, number):
        """
        Parameters:
            number (int): number to be added to move count
        """
        self._move_count += number
        
    def moves_remaining(self):
        """ """
        return self._move_count
    
    def add_item(self, item):
        """Adds item (Item) to inventory
        """
        self._inventory.append(item)
        
    def get_inventory(self):
        """ """
        return self._inventory
    
class GameLogic(object):
    """ """
    def __init__(self, dungeon_name = "game1.txt"):
        """ """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False
        
    def get_positions(self, entity):
        """ """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))
        return positions
    
    def get_dungeon_size(self):
        """ """
        return self._dungeon_size
    
    def init_game_information(self):
        """ """
        self._player.set_position(self.get_positions(PLAYER)[0])
        dictionary = {}
        dictionary[self.get_positions(KEY)[0]] = Key()
        dictionary[self.get_positions(DOOR)[0]] = Door()
        for x,lines in enumerate(self._dungeon):
            for y,entity in enumerate(lines):
                if entity == "#":
                    dictionary[(x,y)] = Wall()
        try:
            dictionary[self.get_positions(MOVE_INCREASE)[0]] = MoveIncrease()
        except:
            pass
        return dictionary
    
    def get_game_information(self):
        """ """
        return self._game_information
    
    def get_player(self):
        """ """
        return self._player
    
    def get_entity(self, position):
        """ """
        return self._game_information.get(position)
        
    def get_entity_in_direction(self, direction):
        """ """
        return self.get_entity(self.new_position(direction))
    
    def collision_check(self, direction):
        """
        Check to see if a player can travel in a given direction
        Parameters:
            direction (str): A direction for the player to travel in.

        Returns:
            (bool): False if the player can travel in that direction without colliding otherwise True.
        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True
        
        return not (0 <= new_pos[0] < self._dungeon_size and 0 <= new_pos[1] < self._dungeon_size)
    
    def new_position(self, direction):
        """ """
        now_position = self.get_player().get_position()      
        moving = DIRECTIONS[direction]
        return (now_position[0] + moving[0], now_position[1] + moving[1])
    
    def move_player(self, direction):
        """ """        
        self._player.set_position(self.new_position(direction))
        
    def check_game_over(self):
        """ """
        return self.get_player().moves_remaining() <= 0
    
    def set_win(self,win):
        """ """
        self._win = win
        
    def won(self):
        """ """
        return self._win


class AbstractGrid(tk.Canvas):
    """An abstract class that won't be instanced"""
        
    def direction_to_pixel(self, direction):
        """
        Converts the (row, col) position to x, y pixel position.

        Parameter:
            direction (tup<int, int>): A (row, col) position.

        Return:
            (tup<int, int>): A pixel position.
        """
        return (direction[1] * 50, direction[0] * 50)

    def get_position_center(self, position):
        """
        Return the entity center with its position of left-top corner.

        Parameter:
            position (tup<int, int>): A pixel position.

        Return:
            (tup<int, int>): A pixel position.
        """
        return (position[0] + 25, position[1] + 25)

    def annotate_position(self, position, text):
        """
        Create text in the canvas widget.

        Parameters:
            position (tup<int, int>): A pixel position of the left-top
                corner of the entity.
            text (str): The text content that will be added in the
                entity centre.
        """
        self.create_text(position[0], position[1], text = text)

class DungeonMap(AbstractGrid):
    """Draw the game map with rectangles and text."""
    
    def __init__(self, master, size, width=600, **kwards):
        """
        Constructor of the DungeonMap class.

        Parameters:
            master (tk.Tk()): The root window of the game.
            size (int): The dungeon size
            width (int): The pixel size of the canvas width.
        """
        super().__init__(master=master,width=width, height=width,bg = 'light gray')        

    def draw_grid(self, dungeon, player_position):
        """
        Draw the rectangles and write text on the canvas.

        Parameters:
            dungeon (dic<tup<int, int>:instance of class>): A dictionary
                that contains  game information except for player position.
            Player_position (tup<int, int>): A (row, col) position.
        """
        try:
            ##  Delete previous map and redraw with immediate information.
            self.delete(tk.ALL)
            
            ##  Draw entities except for player.
            for pos in dungeon:
                entity = dungeon[pos]
                entity_position = self.direction_to_pixel(pos)
                entity_center = self.get_position_center(entity_position)
                entity_text = entity.get_text()
                if entity.get_id() == "K":
                    self.create_rectangle(entity_position[0], entity_position[1],
                        entity_position[0] + 50, entity_position[1] + 50, fill = "yellow")
                elif entity.get_id() == "M":
                    self.create_rectangle(entity_position[0], entity_position[1],
                        entity_position[0] + 50, entity_position[1] + 50, fill = "orange")
                elif entity.get_id() == "D":
                    self.create_rectangle(entity_position[0], entity_position[1],
                        entity_position[0] + 50, entity_position[1] + 50, fill = "brown")
                elif entity.get_id() == "#":
                    self.create_rectangle(entity_position[0], entity_position[1],
                        entity_position[0] + 50, entity_position[1] + 50, fill = "dark gray")
                if entity_text:
                    self.annotate_position(entity_center, entity_text)

            ##  Draw player.
            player_pos = self.direction_to_pixel(player_position)
            player_center = self.get_position_center(player_pos)
            self.create_rectangle(player_pos[0],player_pos[1],\
                                  player_pos[0]+50,player_pos[1]+50, fill = "green")
            self.annotate_position(player_center, "Ibis")
        except:
            pass

class AdvancedDungeonMap(AbstractGrid):
    """Draw the game map with images."""

    def __init__(self, master, size, width=600, **kwards):
        """
        Constructor of the AdvancedDungeonMap class.

        Parameters:
            master (tk.Tk()): The root window of the game.
            size (int): The dungeon size
            width (int): The pixel size of the canvas width.
        """
        super().__init__(master = master, width=width, height=width)
        self._size = size
        ##  Create a dictionary stored all the images that are resized.
        self._images = {'O':ImageTk.PhotoImage(Image.open('images/player.png').resize((50,50))),
                        '#':ImageTk.PhotoImage(Image.open('images/wall.png').resize((50,50))),
                        'grass':ImageTk.PhotoImage(Image.open('images/empty.png').resize((50,50))),
                        'K':ImageTk.PhotoImage(Image.open('images/key.png').resize((50,50))),
                        'M':ImageTk.PhotoImage(Image.open('images/moveincrease.png').resize((50,50))),
                        'D':ImageTk.PhotoImage(Image.open('images/door.png').resize((50,50))),}

    def draw_grid(self, dungeon, player_position):
        """
        Draw the images on the canvas.

        Parameters:
            dungeon (dic<tup<int, int>:instance of class>): A dictionary
                that contains  game information except for player position.
            Player_position (tup<int, int>): A (row, col) position.
        """
        try:
            ##  Delete previous map and redraw with immediate information.
            self.delete(tk.ALL)
            ##  Draw the grass on the canvas.
            for x in range(self._size):
                for y in range(self._size):
                    grass_center = self.get_position_center(self.direction_to_pixel((x, y)))
                    self.create_image(grass_center[0],grass_center[1],image=self._images["grass"])

            ##  Draw the entities on the canvas, except for the player.
            for pos in dungeon:
                entity = dungeon[pos]
                entity_center = self.get_position_center(self.direction_to_pixel(pos))
                self.create_image(entity_center[0],entity_center[1],image=self._images[entity.get_id()])

            ##  Draw the player on the canvas.
            player_center = self.get_position_center(self.direction_to_pixel(player_position))
            self.create_image(player_center[0],player_center[1],image=self._images["O"])
        except:
            pass

class KeyPad(tk.Canvas):
    """Draw the GUI key pad with rectangles and text."""
    
    def __init__(self, master, width=200, height=100, **kwards):
        """
        Constructor of the KeyPad class.

        Parameters:
            master (tk.Tk()): The root window of the game.
            width (int): The pixel size of the canvas width.
            height (int): The pixel size of the canvas height.
        """
        super().__init__(master = master, width = 200, height = 100, bg="white")
        ##  Create the key pad on the canvas.
        up_rect = self.create_rectangle(67,0,134,50, fill = "dark gray")
        N = self.create_text((100,25),text="N")
        left_rect = self.create_rectangle(0,50,67,100, fill = "dark gray")
        W = self.create_text((33,75),text="W")
        down_rect = self.create_rectangle(67,50,134,100, fill = "dark gray")
        S = self.create_text((100,75),text="S")
        right_rect = self.create_rectangle(134,50,200,100, fill = "dark gray")
        E = self.create_text((167,75),text="E")

    def pixel_to_direction(self, pixel):
        """
        Return the direction with the position of mouse click event.

        Parameter:
            pixel (tup<int, int>): A pixel position.

        Return:
            (str): The direction represents the command from the user.
        """
        if (pixel[1]<50) and (pixel[0]>67) and (pixel[0]<134):
            return "W"
        else:
            if pixel[0]<67:
                return "A"
            elif pixel[0] > 134:
                return "D"
            else:
                return "S"

class StatusBar(tk.Frame):
    """A Frame contains some game status information."""
    
    def __init__(self, master, new_game, quit_game, moves):
        """
        Constructor of the StatusBar class.

        Parameters:
            master (tk.Tk()): The root window of the game.
            new_game (method): A method combinded with a button.
            quite_game (method): A method combinded with a button.
            moves (int): The moves left.
        """
        super().__init__()
        ##  Part 1: Two buttons in one frame.
        Part_1 = tk.Frame(self)
        
        btn1 = tk.Button(Part_1, text = "New game", command = new_game)
        btn1.pack(side = tk.TOP, expand = 1)

        btn2 = tk.Button(Part_1, text = "Quit", command = quit_game)
        btn2.pack(side = tk.TOP, expand = 1)

        Part_1.pack(side = tk.LEFT, expand = 1)

        ##  Part 2: timing area.
        Part_2 = tk.Frame(self)
        ##  image:    
        self.clock_image = Image.open('images/clock.png')
        self.clock_image = self.clock_image.resize((35,50))
        self.clock = ImageTk.PhotoImage(image = self.clock_image)
        self.image_1 = tk.Label(Part_2, image = self.clock)
        self.image_1.pack(side = tk.LEFT)
        ## two rows of text in one frame:
        part2_text = tk.Frame(Part_2)
        time_title = tk.Label(part2_text, text = "Time elapsed")
        time_title.pack(side = tk.TOP)
        self._label_time = tk.Label(part2_text, text = "0m 0s")
        self._label_time.pack(side = tk.TOP)
        part2_text.pack(side = tk.LEFT)
        Part_2.pack(side = tk.LEFT, padx=10, expand = 1)

        ##  Part 3: moves area.
        part_3 = tk.Frame(self)
        ##  image:    
        self.moves_image = Image.open('images/lightning.png')
        self.moves_image = self.moves_image.resize((35,50))
        self.lightning = ImageTk.PhotoImage(image = self.moves_image)
        self.image_2 = tk.Label(part_3, image = self.lightning)
        self.image_2.pack(side = tk.LEFT)
        ## two rows of text in one frame:
        part3_text = tk.Frame(part_3)
        label_move = tk.Label(part3_text, text = "Time elapsed")
        label_move.pack(side = tk.TOP, padx=30)
        self._number = tk.Label(part3_text, text = "{} moves remaining".format(moves))
        self._number.pack(side = tk.TOP)
        part3_text.pack(side = tk.LEFT)
        part_3.pack(side = tk.LEFT, expand = 1)

class StatusBarWithLife(StatusBar):
    """A advanced Frame contains some game status information."""

    def __init__(self, master, new_game, quit_game, moves, lives, use_life):
        """
        Constructor of the StatusBar class.

        Parameters:
            master (tk.Tk()): The root window of the game.
            new_game (method): A method combinded with a button.
            quite_game (method): A method combinded with a button.
            moves (int): The moves left.
            lives (int): The number of chances to undo.
            use_life (method): A method combinded with a button.
        """
        super().__init__(master, new_game, quit_game, moves)
        ##  Part 4: lives area.
        part_4 = tk.Frame(self)
        ##  image:    
        self.lives_image = Image.open('images/lives.png')
        self.lives_image = self.lives_image.resize((40,50))
        self.lives = ImageTk.PhotoImage(image = self.lives_image)
        self.label_3 = tk.Label(part_4, image = self.lives)
        self.label_3.pack(side = tk.LEFT)
        ## a row of text and a button in one frame:
        part4_text = tk.Frame(part_4)
        self._lives = tk.Label(part4_text, text = "Lives remaining: {}".format(lives))
        self._lives.pack(side = tk.TOP)
        lives_btn = tk.Button(part4_text, text = "Use life", command = use_life)
        lives_btn.pack(side = tk.TOP)
        part4_text.pack(side = tk.LEFT)
        part_4.pack(side = tk.LEFT, expand = 1)

        
class GameApp(object):
    """
    Define game information and decide how does game implement.
    """
    
    def __init__(self, master, task=TASK_ONE, dungeon_name="game2.txt"):
        """
        Constructor of the GameLogic class.

        Parameters:
            master (tk.Tk()): The root window of the game.
            task (str): An argument decided the game mode.
            dungeon_name (str): The name of the level.
            
        """
        
        self._task = task
        self._dungeon_name = dungeon_name
        self._game = GameLogic(self._dungeon_name)
        ##  set the title of the game.
        self._root = master
        self._root.title("Key Cave Adventure Game")
        self._label = tk.Label(self._root, text = "Key Cave AdventureGame",
                               bg = "green", font=(None, 35))
        ##  somes arguments for task two and master.
        self._lives = 3
        self._minutes = 0
        self._seconds = 0
        self._time_right_now = None         #A tuple to store the time that event occured.
        self._score = 0
        self._record = []                   #A list to store information of top three players.
        self._top_level_window = None       #A toplevel widget to ask user enter name.
        self._entry = None                  #A text widget to ask user enter name.
        self._filename = None   
        self._player_name = ''
        self._top3 = None                   #A toplevel widget show the top three records.
        self._recent_move_direction = []    #A list to store move direction for undo(lives).
        self._calculate_time = False
        self._hit_wall = False
        ##  Instance the view classes.
        self._up_frame = tk.Frame(self._root)
        self._screen = DungeonMap(self._up_frame, self.get_game().get_dungeon_size(),
                                  self.get_game().get_dungeon_size()*50)        
        self._ADM = AdvancedDungeonMap(self._up_frame, self.get_game().get_dungeon_size(),
                                       self.get_game().get_dungeon_size()*50)
        self._keypad = KeyPad(self._up_frame)
        self._keypad.bind('<Button-1>', self.mouse_press)
        self._root.bind("<Key>",self.key_press)
        self._statusbar = StatusBar(self._root, self.new_game, self.quit_game,
                                    self.get_game().get_player().moves_remaining())
        self._statusbar_with_lives = StatusBarWithLife(self._root, self.new_game, self.quit_game,
                    self.get_game().get_player().moves_remaining(), self._lives, self.use_life)

    def play(self):
        """"
        Show the view class in the root window.
        """
        ##  adjust the size of GUI window.
        if self._task == TASK_ONE:
            self._root.geometry("{}x{}".format(self.get_game().get_dungeon_size()*50 + 210,
                                self.get_game().get_dungeon_size()*50 + 55))
        elif self._task == TASK_TWO:
            self._root.geometry("{}x{}".format(self.get_game().get_dungeon_size()*50 + 210,
                                self.get_game().get_dungeon_size()*50 + 120))
        else:
            if self._dungeon_name == "game1.txt":
                print(1)
                self._root.geometry("{}x{}".format(self.get_game().get_dungeon_size()*50 + 350,
                                    self.get_game().get_dungeon_size()*50 + 120))
            else:
                self._root.geometry("{}x{}".format(self.get_game().get_dungeon_size()*50 + 250,
                                    self.get_game().get_dungeon_size()*50 + 120))

        ##  show the view class in the GUI windw.
        if self._task != TASK_ONE:
            menubar = tk.Menu(self._root)
            self._root.config(menu=menubar)
            filemenu=tk.Menu(menubar)
            menubar.add_cascade(label='File',menu=filemenu)
            filemenu.add_command(label='Save Game',command=self.save_game)
            filemenu.add_command(label='Load Game',command=self.load_game)
            filemenu.add_command(label='New Game',command=self.new_game)
            if self._task == MASTER:
                filemenu.add_command(label='High scores',command=self.high_score)
            filemenu.add_command(label='Quit',command=self.quit_game)

        self._label.pack(side = tk.TOP, fill = tk.X)

        if self._task == TASK_ONE:
            self._screen.draw_grid(self.get_game().get_game_information(),
                                   self.get_game().get_player().get_position())
            self._screen.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        else:
            self._ADM.draw_grid(self.get_game().get_game_information(),
                             self.get_game().get_player().get_position())
            self._ADM.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        self._keypad.pack(side = tk.LEFT)
        self._up_frame.pack(side = tk.TOP)
        if self._task == TASK_TWO:
            self._statusbar.pack(side = tk.TOP, expand = 1, fill = tk.BOTH)
        elif self._task == MASTER:
            self._statusbar_with_lives.pack(side = tk.TOP, expand = 1, fill = tk.BOTH)
        self._root.after(1000, self.calculate_time)
        self._root.mainloop()

    def move_action(self, direction):
        """
        Loop the game and pop up information.

        Parameter:
            direction (str): The direction represents the command from the user
        """
        if not self._game.collision_check(direction):
            self._game.move_player(direction)
            entity = self._game.get_entity(self._game._player.get_position())
            if entity is not None:
                entity.on_hit(self._game)
                
                if self._game.won():

                    ##  In task one and two mode, pup up message box after winning.
                    if self._task != "MASTER":
                        self.ask_win()

                    ##  check whether in top three in master mode.
                    else:
                        self.read_high_score()

                        ##  There are already three records and your score is greater than one of them
                        if self._record[0] != 0 and self._record[1] != 0 and self._record[2] != 0 and \
                                               self._score >  self._record[2][1]*60+self._record[2][2]:  
                            self.ask_win()

                        ##  Your score is within top three.
                        else:
                            self._top_level_window = tk.Toplevel()
                            self._top_level_window.title("You win")
                            self._top_level_window.geometry("300x100")
                            win_label = tk.Label(self._top_level_window,
                                        text = "You win in {}m and {}s! Enter your name:".format\
                                                 (self._time_right_now[0],self._time_right_now[1]))
                            win_label.pack(side = tk.TOP)
                            self._entry = tk.Entry(self._top_level_window, width = 20)
                            self._entry.pack(side=tk.TOP)
                            enter_btn = tk.Button(self._top_level_window, text = "Enter",
                                                  command = self.enter_name)
                            enter_btn.pack(side = tk.TOP)
                            self._top_level_window.mainloop()
                            

            ##  Draw the grid.
            self._screen.draw_grid(self.get_game().get_game_information(),
                                   self.get_game().get_player().get_position())
            self._ADM.draw_grid(self.get_game().get_game_information(),
                                self.get_game().get_player().get_position())


        else:
            self._hit_wall = True


        ##  reduce move_count and check whether loss the game.
        self.get_game().get_player().change_move_count(-1)
        if self._game.check_game_over() and not self._game._win:
            ans_loss = tk.messagebox.askyesno("You lost!", "You haven't finished the level with \
                            a score of {}. Would you like to play again?".format(self._score))
            if ans_loss:
                self.new_game()
            else:
                self._root.destroy()

        ##  try to update the immediate information.
        try:
            moves_left = self.get_game().get_player().moves_remaining()
            self._statusbar._number.config(text = "{} moves remaining".format(moves_left))
            self._statusbar_with_lives._number.config(text = "{} moves remaining".format(moves_left))
        except:
            pass


    def read_high_score(self):
        """
        Get the records from 'High score' file.
        """
        open_file = open("High score", 'a')

        try:
            open_file = open("High score", 'r')
            records = open_file.readlines()
        except:
            records = None

        for i in range(3):
            try:
                name,_,score = records[i].partition(":")
                mins,_,secs = score.partition(",")
                mins = int(mins)
                secs = int(secs[0:len(secs)-1])
                self._record.append((name, mins, secs))
            except:
                self._record.append(0)

    def key_press(self, event):
        """
        Set the direction of movement of player

        Parameter:
            event (tk.Event): Selection event with key press.
        """
        self._time_right_now = (self._minutes, self._seconds)
        self._score = self._seconds + self._minutes*60
        self._hit_wall = False
        self.store_move_dir(event.char.upper())         
        
    def mouse_press(self, event):
        """
        Set the direction of movement of player

        Parameter:
            event (tk.Event): Selection event with mouse coordinates.
        """
        self._time_right_now = (self._minutes, self._seconds)
        self._score = self._seconds + self._minutes*60
        self._hit_wall = False
        self.store_move_dir(self._keypad.pixel_to_direction((event.x, event.y)))            

    def ask_win(self):
        """
        Pop up a message box to ask user whether to start a new game or quit.
        """
        ans_win = tk.messagebox.askyesno('You won!', 'You have finished the level with a score of {}. \
                                         Would you like to play again?'.format(self._score))
        if ans_win:
            self.new_game()
        else:
            self._root.destroy()

    def enter_name(self):
        """
        Enter the name and store it as well as score into the 'High score' file.
        """
        self._player_name = self._entry.get()
        file = open("High score", 'r')
        info = file.readlines()

        ##  There is no record stored yet.
        if self._record[0] == 0:
            record_1 = self._player_name + ":" + "{},{}".format(\
                        self._time_right_now[0],self._time_right_now[1]) + "\n"
            with open("High score","w",encoding="utf-8") as write_file:
                for line in info:
                    if True:
                        continue
                write_file.write(record_1)

        ##  There is only one record stored in the file.
        elif self._record[1] == 0:
            if self._score < self._record[0][1]*60+self._record[0][2]:      ##  You are num 1.
                record_1 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(record_1)
                    write_file.write(info[0])
            else:                                                           ##  You are num 2.
                record_2 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(info[0])
                    write_file.write(record_2)
                    
        ##  There are two records stored in the file.
        elif self._record[2] == 0:          
            if self._score < self._record[0][1]*60+self._record[0][2]:      ##  You are num 1.
                record_1 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(record_1)
                    write_file.write(info[0])
                    write_file.write(info[1])                   
            elif self._score < self._record[1][1]*60+self._record[1][2]:    ##  You are num 2.
                record_2 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(info[0])
                    write_file.write(record_2)
                    write_file.write(info[1])
            else:                                                           ##  You are num 3.
                record_3 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(info[0])
                    write_file.write(info[1])
                    write_file.write(record_3)        

        ##  There are three records stored in the file.
        else:
            if self._score < self._record[0][1]*60+self._record[0][2]:      ##  You are num 1.
                record_1 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(record_1)
                    write_file.write(info[0])
                    write_file.write(info[1])
            elif self._score < self._record[1][1]*60+self._record[1][2]:    ##  You are num 2.
                record_2 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(info[0])
                    write_file.write(record_2)
                    write_file.write(info[1])
            elif self._score < self._record[2][1]*60+self._record[2][2]:    ##  You are num 3.
                record_3 = self._player_name + ":" + "{},{}".format(\
                            self._time_right_now[0],self._time_right_now[1]) + "\n"
                with open("High score","w",encoding="utf-8") as write_file:
                    for line in info:
                        if True:
                            continue
                    write_file.write(info[0])
                    write_file.write(info[1])
                    write_file.write(record_3)

        self._top_level_window.destroy()
        self.ask_win()
        
    def high_score(self):
        """
        Show the high score window with top three players' information.
        """
        self.read_high_score()

        self._top3 = tk.Toplevel()
        self._top3.title("Top 3")
        self._top3.geometry("200x150")
        label_1 = tk.Label(self._top3, text = "High Scores", bg = "green", font=(None, 35))
        label_1.pack(side = tk.TOP)
        for num in range(3):
            if self._record[num] != 0:
                if self._record[num][1] != 0:
                    record = tk.Label(self._top3, text="{}: {}m {}s".\
                                      format(self._record[num][0],self._record[num][1],self._record[0][2]))
                    record.pack(side = tk.TOP)
                else:
                    record = tk.Label(self._top3, text="{}: {}s".\
                                      format(self._record[num][0],self._record[num][2]))
                    record.pack(side = tk.TOP)    
        enter_btn = tk.Button(self._top3, text = "Done", command = self._top3.destroy)
        enter_btn.pack(side = tk.BOTTOM)
        
    def done(self):
        """
        Close the high score window.
        """
        self._top3.destroy()

    def use_life(self):
        """
        Try to undo the player and corresponded arguments.
        """
        try:
            self._minutes, self._seconds = self._time_right_now
            if self._lives != 0:

                ##check whether previous action hit wall
                if self._hit_wall:

                    ##  Update the lives left
                    self._recent_move_direction = self._recent_move_direction[0:-1]
                    self._lives -= 1
                    self._statusbar_with_lives._lives.config(text = "Lives remaining: {}".format(self._lives))                

                    ##  Update the moves left.
                    self.get_game().get_player().change_move_count(1)
                    moves_left = self.get_game().get_player().moves_remaining()
                    self._statusbar._number.config(text = "{} moves remaining".format(moves_left))
                    self._statusbar_with_lives._number.config(text = "{} moves remaining".format(moves_left))
                    self._hit_wall = False

                else:

                    if self._recent_move_direction[-1] == 'W':
                        undo_direction = 'S'
                    elif self._recent_move_direction[-1] == 'S':
                        undo_direction = 'W'
                    elif self._recent_move_direction[-1] == 'A':
                        undo_direction = 'D'
                    elif self._recent_move_direction[-1] == 'D':
                        undo_direction = 'A'

                    ##  Update the lives left
                    self._recent_move_direction = self._recent_move_direction[0:-1]
                    self._lives -= 1
                    self._statusbar_with_lives._lives.config(text = "Lives remaining: {}".format(self._lives))                

                    ##  Check wheather need to recover key and move_increase.
                    if self._game._player._position == self._game.get_positions(KEY)[0]:
                        self._game._game_information[self._game.get_positions(KEY)[0]] = Key()
                        self._game._player._inventory = []
                    elif self._game._player._position == self._game.get_positions(MOVE_INCREASE)[0]:
                        self._game._game_information[self._game.get_positions(MOVE_INCREASE)[0]] = MoveIncrease()
                        self.get_game().get_player().change_move_count(-5)

                    ##  Update the moves left.
                    self.get_game().get_player().change_move_count(2)
                    moves_left = self.get_game().get_player().moves_remaining()
                    self._statusbar._number.config(text = "{} moves remaining".format(moves_left))
                    self._statusbar_with_lives._number.config(text = "{} moves remaining".format(moves_left))
                    self.move_action(undo_direction)
        except:
            pass
        
    def store_move_dir(self,direction):
        """
        Store move direction with maximum of 3 to undo direction in MASTER mode.
        """
        ##  If the number of lives is equal to the number of direction stored, pop the first one.
        if len(self._recent_move_direction) == self._lives and len(self._recent_move_direction)!= 0:
            self._recent_move_direction.pop(0)
            
        self._recent_move_direction.append(direction)
        self.move_action(direction)
            
    def calculate_time(self):
        """
        A timing function achieved by recursion.
        """
        self._seconds += 1
        if self._seconds == 60:
            self._seconds = 0
            self._minutes += 1
        self._statusbar._label_time.config(text = "{}m {}s".format(self._minutes, self._seconds))
        self._statusbar_with_lives._label_time.config(text = "{}m {}s".format(self._minutes, self._seconds))

        ##  if win or lose the game, stop timing.
        if self._calculate_time or self.get_game().get_player()._move_count == 0:
            return None

        ##  timing by recursion.
        self._root.after(1000, self.calculate_time)

    def new_game(self):
        """Start a new game"""
        self._root.destroy()
        app=GameApp(tk.Tk(), self._task, self._dungeon_name)
        app.play()

    def save_game(self):
        """
        Save the significant information of the game into a file.
        """
        if self._filename == None:
            filename = filedialog.asksaveasfilename()
            if filename:
                self._filename = filename
        if self._filename:
            self._root.title(self._filename)
            fd = open(self._filename,'w')

            if self.get_game().get_positions(KEY)[0] not in self.get_game().get_game_information().keys():
                key_state = '404'
            else:
                key_state = '1'

            if self.get_game().get_positions(MOVE_INCREASE)[0] not in \
                           self.get_game().get_game_information().keys():
                move_inc_state = '404'
            else:
                move_inc_state = '1'

            try:
                direction_1 = self._recent_move_direction[0] + ' '
                direction_2 = self._recent_move_direction[1] + ' '
                direction_3 = self._recent_move_direction[2] + ' '
            except:
                direction_1 = "404" + ' '
                direction_2 = "404" + ' '
                direction_3 = "404" + ' '

            if self._hit_wall:
                hit_wall_undo = "1"
            else:
                hit_wall_undo = "404"

            time = "{} {}".format(self._time_right_now[0],self._time_right_now[1])

            game_info = self._task + " " +\
                        self._dungeon_name + " " +\
                        key_state + ' ' +  move_inc_state + " " +\
                        str(self.get_game().get_player().get_position()[1]) + " " +\
                        str(self.get_game().get_player().get_position()[0]) + " " +\
                        str(self.get_game().get_player().moves_remaining()) + " " +\
                        str(self._lives) + ' ' + time + " " +\
                        direction_1 + direction_2 + direction_3 + " " + hit_wall_undo
            fd.write(game_info)
            fd.close

    def load_game(self):
        """
        Open the file and read the content,
        then create a new GameApp and change its attributes.
        """
        filename = filedialog.askopenfilename()
        if filename:
            self._root.destroy()
            self._filename = filename
            fd = open(filename, 'r')
            game_info = fd.read().split()
            fd.close

            load_game = GameApp(tk.Tk(), game_info[0], game_info[1])
            load_game.get_game().get_player().set_position((int(game_info[5]), int(game_info[4])))
            load_game.get_game().get_player()._move_count = int(game_info[6])
            load_game._lives = int(game_info[7])
            load_game._time_right_now = (int(game_info[8]), int(game_info[9]))
            load_game._minutes, load_game._seconds = load_game._time_right_now
            load_game._filename = filename

            ##  check whether already hit key or move-increase:
            if game_info[2] == "404":
                key_pos = load_game.get_game().get_positions(KEY)[0]
                load_game._game.get_entity(key_pos).on_hit(load_game.get_game())
            if game_info[3] == "404":
                move_inc_pos = load_game.get_game().get_positions(MOVE_INCREASE)[0]
                load_game._game.get_entity(move_inc_pos).on_hit(load_game.get_game())
                load_game._game._player.change_move_count(-5)

            ##  check previous action whether hit wall.
            if game_info[-1] == "1":
                load_game._hit_wall = True

            ##  store the latest move action and prepare for using lives.
            for i in range(3):
                if game_info[10 + i] != "404":
                    load_game._recent_move_direction.append(game_info[10 + i])

            ##  update the status bar
            try:
                load_game._statusbar._number.config(text = "{} moves remaining".format(\
                                                    load_game._game._player._move_count))
                load_game._statusbar_with_lives._lives.config(text = "Lives remaining: {}".format(\
                                                    load_game._lives))
                load_game._statusbar_with_lives._number.config(text = "{} moves remaining".format(\
                                                    load_game._game._player._move_count))
            except:
                pass
            load_game.play()

    def quit_game(self):
        """Destroy the root window"""
        self._root.destroy()
        
    def get_game(self):
        """Return GameLogic instance"""
        return self._game

if __name__ == "__main__" :

    root = tk.Tk()
    app = GameApp(root, MASTER, "game2.txt")
    app.play()
    root.mainloop()
    #TASK_ONE TASK_TWO MASTER
