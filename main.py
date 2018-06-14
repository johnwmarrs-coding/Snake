# AUTHOR: John Marrs
# Snake: Implementation of Snake using python and Tkinter
# Created in Python 3.6
# 6/14/2018

# Basic Game Architecture
# 1 - Start Game (Initialize Values)
# 2 - Render Game Visuals
# 3 - Receive/Process Input
# 4 - Update Game Logic
# 5 - JUMP TO STEP 2

import tkinter as tk
import random

class Main_GUI(tk.Frame):
    def __init__(self, master):
        #COLOR SCHEME VARIABLES
        self.primary = "#1995AD"
        self.secondary = "#A1D6E2"
        self.tertiary = "#BCBABE"
        self.quaternary = "#F1F1F2"

        self.snake = "#000000"
        self.food = "#BA9531"

        self.game_over_color = "#FF3232"

        # Provide number of rows and columns
        self.rows = 21
        self.columns = 21

        # Housekeeping for Frame and Tk() objects
        self.master = master
        self.master.title("Snake - John Marrs")
        self.master.geometry("500x500")
        self.master.focus_set()
        self.master.update()
        self.width = self.master.winfo_width()
        self.height = self.master.winfo_height()

        # Specify padding for edges
        self.padding = 50

        self.create_components()


    def create_components(self):
        #Initialize the canvas, bind keys to function handler, bind configure to on_resize method

        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.master.bind("<Key>", self.handle_keystroke)
        self.master.bind("<Configure>", self.on_resize)
        self.setup()
        


    def start_game(self):
        #Clear screan
        self.canvas.delete("all")

        #Launch the game
        self.setup()
        self.game_running = True

        self.update()

    def game_over(self):
        # End the game
        self.game_running = False
        self.game_ended = True


    def setup(self):
        # Prepare a new game/ Display menu
        self.game_running = False
        self.game_ended = False

        # Initialize Game Data --------------------------
        self.score = 0

        self.player_direction = 'w' #d - right, w = up, a = left, s = down
        self.player_row = int(self.rows/2)
        self.player_col = int(self.columns/2)
        self.tail_positions = []

        self.place_food()



        # End Game Data Initialization ------------------

        self.canvas.delete("all")
        # Draw Menu Screen
        self.canvas.create_rectangle(0,0,self.width, self.height, fill=self.secondary)
        self.canvas.create_text(self.width/2 , 2 * self.height/5,fill=self.primary,font="system 48", text="Snake")
        self.canvas.create_text(self.width/2 , 2.75 * self.height/5,fill=self.primary,font="system 20", text="Controls")
        self.canvas.create_text(self.width/2 , 3.25 * self.height/5,fill=self.primary,font="system 14", text="<w,a,s,d> to move, <space> to reset.")
        

    def update(self):
        if (self.game_running):
            # Game logic 

            # Draw move tail positions
            for i in range(0, len(self.tail_positions)):
                if (i == (len(self.tail_positions) - 1)):
                    self.tail_positions[i] = (self.player_row, self.player_col)
                else:
                    self.tail_positions[i] = self.tail_positions[i+1]

            # Move player
            if (self.player_direction == 'a'):
                self.player_col -= 1
            elif (self.player_direction == 'w'):
                self.player_row -= 1
            elif (self.player_direction == 'd'):
                self.player_col += 1
            elif (self.player_direction == 's'):
                self.player_row += 1

            #Check if biting tail
            for pos in self.tail_positions:
                if (pos[0] == self.player_row and pos[1] == self.player_col):
                    self.game_over()

            #Check if player is moving out of bounds
            if (self.player_row < 0) or (self.player_row > (self.rows - 1)):
                self.game_over()

            if (self.player_col < 0) or (self.player_col > (self.columns - 1)):
                self.game_over()




            # Eat food and add more
            if ((self.player_row == self.food_row) and (self.player_col == self.food_col)):
                self.score += 1
                self.place_food()
                self.tail_positions.append((self.player_row, self.player_col))
                self.tail_positions[len(self.tail_positions) - 1] = (self.player_row, self.player_col)
                    


            #Draw game values
            self.canvas.delete("all")
            box_width = (self.width - self.padding * 2) / self.columns
            box_height = (self.height - self.padding * 2) / self.rows 
            for i in range(0, self.rows):
                for j in range(0, self.columns):
                    if (((i + j) % 2) == 0):
                        self.canvas.create_rectangle(j * box_width + self.padding, i * box_height + self.padding,
                            j * box_width + self.padding + box_width, i * box_height + self.padding + box_height, fill=self.primary)
                    else:
                        self.canvas.create_rectangle(j * box_width + self.padding, i * box_height + self.padding,
                            j * box_width + self.padding + box_width, i * box_height + self.padding + box_height, fill=self.secondary)

            self.canvas.create_rectangle(self.player_col * box_width + self.padding, self.player_row * box_height + self.padding,
                self.player_col * box_width + self.padding + box_width, self.player_row * box_height + self.padding + box_height, fill=self.snake)

            self.canvas.create_rectangle(self.food_col * box_width + self.padding, self.food_row * box_height + self.padding,
                self.food_col * box_width + self.padding + box_width, self.food_row * box_height + self.padding + box_height, fill=self.food)

            for t in self.tail_positions:
                self.canvas.create_rectangle(t[1] * box_width + self.padding, t[0] * box_height + self.padding,
                    t[1] * box_width + self.padding + box_width, t[0] * box_height + self.padding + box_height, fill=self.snake)

            # Display score and reset instructions
            self.canvas.create_text(self.width/2 ,25,fill=self.primary,font="system 20", text=("Score: " + str(self.score)))
            self.canvas.create_text(self.width/2 , self.height - 25,fill=self.primary,font="system 14", text="Press <space> to reset.")
            #self.canvas.create_text(0 ,25,fill=self.primary,font="Times 20", text=("Score: " + str(self.score)))

            

            #updat every 10th of a second
            self.master.after(100, self.update)
        elif self.game_ended:
            #Display game over if the game has ended
            self.canvas.create_text(self.width/2 , self.height/2,fill=self.game_over_color,font="system 36", text="GAME OVER")



    #handle user inputs
    def handle_keystroke(self, event):
        i = event.char
        if (not self.game_running):
            if (i == ' '):
                if (self.game_ended):
                    self.setup()
                else :
                    self.start_game()
        else:
            if (i == ' '):
                self.setup()
            elif (i == 'a'):
                if (self.player_direction != 'd') or len(self.tail_positions) == 0:
                    self.player_direction = 'a'
            elif (i == 'w'):
                if (self.player_direction != 's') or len(self.tail_positions) == 0:
                    self.player_direction = 'w'
            elif (i == 'd'):
                if (self.player_direction != 'a') or len(self.tail_positions) == 0:
                    self.player_direction = 'd'
            elif (i == 's'):
                if (self.player_direction != 'w') or len(self.tail_positions) == 0:
                    self.player_direction = 's'

    #Function for placing food in a position where the snake isn't
    def place_food(self):
        unique = False
        while (not unique):
            self.food_row = random.randint(0, self.rows-1)
            self.food_col = random.randint(0, self.columns-1)
            if ((self.food_row != self.player_row) and (self.food_col != self.player_col)):
                unique = True
                for pos in self.tail_positions:
                    if (pos[0] == self.food_row) and (pos[1] == self.food_col):
                        unique = False
                        break
                
    #handle resize
    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.master.update()
        self.setup()

                
# Actually launch the application
application = tk.Tk()
application.update()
m_gui = Main_GUI(application)
application.mainloop()


