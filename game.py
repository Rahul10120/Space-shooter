#display resolution 1920 x 1080.
#game controls- 
# 1) press enter to play the game.
# 2) press spacebar to shoot bullets.
# 3) press arrow keys(<,>) or (A,D) to move left and right.

# -------------------------------------------------------------------------------------------------------------------------

# imports
from tkinter import *
from tkinter.font import Font
import time
import random

# default windows size.
w = 800 
h = 600

# initialisation to check the game has started.
gameState = 0
# no of game rounds.
gameRound = 1
# game score check .
gameScore = 0

# game progression speed(gradually increases)
gameSpeed = 30

# accuracy measurement.
shootBulletCounter = 0
enemyKillCounter = 0

# combo kill measurements.
comboCounter = 0
maxComboCounter = 0

#---------------------------------------------------------------------------------------------------------------------------

# game class that has methods and variables for the game.
class Sprite :
    # constructor		
    def __init__(self, image, x, y):
        self.img = image	
        self.x = x		
        self.y = y		
        self.dx = 0		
        self.dy = 0      
                
    # returns the width		
    def getWidth(self) :
        return self.img.width()

    # returns the height			
    def  getHeight(self) :
        return self.img.height()

    # draws a sprite to the screen	
    def draw(self, g) :
        g.create_image(self.x, self.y, anchor=NW, image=self.img)

    # movement of the sprite.
    def move(self) :
        self.x += self.dx
        self.y += self.dy
    
    # method to set dx
    def  setDx(self, dx) :
        self.dx = dx

    # method to set dy
    def  setDy(self, dy) :
        self.dy = dy

    # returns dx
    def  getDx(self) :
        return self.dx

    # returns dy. 
    def  getDy(self) :
        return self.dy

    # returns x coordinate
    def  getX(self) :
        return self.x

    # returns y coordinate. 
    def  getY(self) :
        return self.y

#----------------------------------------------------------------------------------------------------------------------------

    # counts whether it collides with another sprite. 
    def  checkCollision(self, other) :
        p1x = self.x
        p1y = self.y
        p2x = self.x+self.getWidth()
        p2y = self.y+self.getHeight()
        p3x = other.x
        p3y = other.y
        p4x = other.x+other.getWidth()
        p4y = other.y+other.getHeight()

        overlapped = not( p4x < p2x or
            p3x > p2x or
            p2y < p3y or
            p1y > p4y)
        return overlapped

    # handle conflicts.
    def  handleCollision(self, other) :
        pass

#--------------------------------------------------------------------------------------------------------------------------------------------
 
# class for out starship.
class StarShipSprite(Sprite):
    def __init__(self, game, image, x, y):
        super().__init__(image, x, y)
        self.game = game
        self.dx = 0
        self.dy = 0

    # spaceship movement and prevents it to run out of screen.  
    def move(self):
        if ((self.dx < 0)  and (self.x < 10)) :
            return
        if ((self.dx > 0) and (self.x > 760)) :
            return
        super().move()
        self.dx = 0

    # collision detector(if our spaceship collides with an alien object, game over) 
    def handleCollision(self, other) :
        if  type(other) is AlienSprite :
            self.game.endGame()

#---------------------------------------------------------------------------------------------------------------------------------------------

# class representing our alien spaceship.
class AlienSprite(Sprite):
    def __init__(self, game, image, x, y):
        super().__init__(image, x, y)
        self.game = game
        self.dx = -10		

    # How to move an alien spaceship
    # Move down one space when the window border is reached. 
    def move(self):
        if (((self.dx < 0) and (self.x < 10)) or ((self.dx > 0) and (self.x > 760))) :
            self.dx = -self.dx
            self.y += 108
            if (self.y >= 600) :	
                self.game.endGame()
        super().move()

# class representing the shell.
class ShotSprite(Sprite):
    def __init__(self, game, image, x, y):
        super().__init__(image, x, y)
        self.game = game
        self.dy = -20

    # When it leaves the screen, the object is deleted from the list. 
    def move(self):
        super().move()
        global comboCounter
        if (self.y < -100) :
            self.game.removeSprite(self)
            comboCounter = 0

    # handle conflicts. Removes all shells and alien spaceship objects from the list. 
    def handleCollision(self, other) :
        if  type(other) is AlienSprite:
            global gameScore
            global enemyKillCounter
            global comboCounter
            enemyKillCounter += 1
            comboCounter += 1
            gameScore += 10
            self.game.removeSprite(self)
            self.game.removeSprite(other)

#------------------------------------------------------------------------------------------------------------------------------------------------
            
# class representing the game
class GalagaGame():

    # Function to handle left arrow key event
    def keyLeft(self, event) :
        self.starship.setDx(-30)
        return

    # Function to handle right arrow key event
    def keyRight(self, event) :
        self.starship.setDx(+30)
        return

    # Function to handle space key event
    def keySpace(self, event) :
        self.fire()
        return

    # A method to create the sprites needed for the game
    def initSprites(self) :
        # Clear the sprite at the start of a new round 
        self.sprites.clear() 
        global gameRound
        self.starship = StarShipSprite(self, self.shipImage, 370, 520)
        self.sprites.append(self.starship)

        # The number of enemies varies according to the number of game rounds
        for x in range(0, 1+(gameRound)):
            purpleAlien = AlienSprite(self, self.purpleAlienImage, 600+(x*50), 3*36)
            blueAlien = AlienSprite(self, self.blueAlienImage, 600+(x * 50), 2*36)
            greenAlien = AlienSprite(self, self.greenAlienImage, 600+(x*50), 1*36)
            self.sprites.append(blueAlien)
            self.sprites.append(purpleAlien)
            self.sprites.append(greenAlien)

    # constructor method
    def __init__(self, master):
        global gameState
        master.bind("<Return>", self.menuStartGame)
        self.master = master
        self.sprites = []

        # Create a canvas with 4:3 aspect ratio
        self.canvas = Canvas(master, width=800, height=600)
        self.canvas.pack()
        self.canvas.focus_set()

        # usage of the image files inside the res folder.
        self.shotImage = PhotoImage(file="res\\laser.png")
        self.shipImage = PhotoImage(file="res\\ship.png")
        self.blueAlienImage = PhotoImage(file="res\\enemy2_1.png")
        self.purpleAlienImage = PhotoImage(file="res\\enemy1_1.png")
        self.greenAlienImage = PhotoImage(file="res\\enemy3_1.png")
        self.mysteryImage = PhotoImage(file="res\\mystery.png")
        self.alienDeadImage = PhotoImage(file="res\\explosionblue.png")  
        self.running = True
        master.bind("<Left>",  self.keyLeft)
        master.bind("<Right>", self.keyRight)
        master.bind("<space>", self.keySpace)
        self.initSprites()

    # Calling this method changes gameState
    def menuStartGame(self, sprite):
        global gameState
        gameState = 1
        self.running = True
        

    # method to start the game 
    def startGame(self) :
        self.sprites.clear()
        

    # method to end the game. 
    def endGame(self) :
        self.running = False
        
    
    # Delete the sprite from the recit. 
    def removeSprite(self, sprite) :
        if( sprite in self.sprites):
            self.sprites.remove(sprite)
            del sprite

    # method of firing a cannonball
    def fire(self) :
        global shootBulletCounter 
        shootBulletCounter += 1
        shot = ShotSprite(self, self.shotImage, self.starship.getX() + 22,	self.starship.getY() - 0)
        self.sprites.append(shot)

    # method to draw the screen 
    def paintMainMenu(self) :
        self.canvas.delete(ALL)

        # Color the background of the game screen black.
        self.canvas.create_rectangle(0, 0, 800, 600, fill="black")

       # Set the font to be used on the main screen.
        
        mainBigMenuFont = Font(family="Roman", size=85, weight="bold")
        mainSmallMenuFont = Font(family="Roman", size=35)
        

        # Draw the game title on the main screen.
        self.canvas.create_text(400,200,text="Space Shooter", fill="gold", font=mainBigMenuFont)
        self.canvas.create_text(400,370,text="- Press ENTER To Play -", fill="red", font=mainSmallMenuFont)

    # Draw the screen when the game is over.
    def paintGameOver(self) :
        #  global variables.
        global gameScore
        global gameRound
        global maxComboCounter
        global shootBulletCounter
        global enemyKillCounter

        # Use the try statement to handle an exception if the game is over without the user doing anything.
        try:
            accuracy = enemyKillCounter/shootBulletCounter
            if accuracy > 1:
                accuracy = 1 
            accuracy = str(round(round(accuracy,3)*100))+'%'
        except ZeroDivisionError:
            accuracy = "No Bullets Fired, Try Again"
        
        #Clear everything on the screen for the Game Over screen.
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0, 0, 800, 600, fill="black")
        
        mainBigMenuFont = Font(family="Roman", size=100, weight="bold")
        mainSmallMenuFont = Font(family="Roman", size=25)

        # Added function - Shows the game history with Game Over. It shows the number of rounds, score, max combo, and accuracy.
        self.canvas.create_text(400,200,text="Game Over", fill="red", font=mainBigMenuFont)
        self.canvas.create_text(400,300,text="Round: "+str(gameRound), fill="white", font=mainSmallMenuFont)
        self.canvas.create_text(400,343,text="Score: "+str(gameScore), fill="white", font=mainSmallMenuFont)
        self.canvas.create_text(400,386,text="Max Combo: "+str(maxComboCounter), fill="white", font=mainSmallMenuFont)
        self.canvas.create_text(400,429,text="Accuracy: "+str(accuracy), fill="white", font=mainSmallMenuFont)

    # Draws the screen when the game starts.
    def paintGame(self,g):
        self.canvas.delete(ALL)
        
        self.canvas.create_rectangle(0, 0, 800, 600, fill="black")
        self.canvas.create_rectangle(610,10,790,190, fill="purple")
        self.canvas.create_rectangle(615,15,785,185, fill="black")

        # The red dots were randomly taken to give the impression of a spaceship flying through space.
        for i in range(20):
            x = random.randint(0,w)
            y = random.randint(0,h)
            self.canvas.create_oval(x,y,x,y,width=0,fill="red")

        # Added function - Real-time update of necessary information.
        self.updateAccuracy()
        self.updateCombo()
        self.updateScore()
        self.updateRound()
        self.canvas.update
        for sprite in self.sprites:
            sprite.draw(self.canvas)

    #  Added function - display accuracy by drawing on canvas 
    def updateAccuracy(self):
        global shootBulletCounter
        global enemyKillCounter
        try:
            accuracy = enemyKillCounter/shootBulletCounter
            if accuracy > 1:
                accuracy = 1
            accuracy = str(round(round(accuracy,3)*100))+'%'
        except ZeroDivisionError:
            accuracy = "Ready"
        self.canvas.create_text(700,165,fill="white",font="Chiller 22 bold",text='Accuracy: '+accuracy)

    # Added function - Draw and display combos on the canvas
    def updateCombo(self):
        global comboCounter
        global maxComboCounter
        if comboCounter>maxComboCounter:
            maxComboCounter = comboCounter
        self.canvas.create_text(700,121,fill="white",font="Chiller 22 bold",text ='Combo: '+str(comboCounter))

    #Added Feature - Score is drawn and displayed on canvas
    def updateScore(self):
        global gameScore
        self.canvas.create_text(700,78,fill="white",font="Chiller 22 bold",text="Score: "+str(gameScore))
    
    # Added Feature - Draw and display game rounds on canvas
    def updateRound(self):
        global gameRound
        self.canvas.create_text(700,35,fill="white",font="Chiller 22 bold",text="Round: "+str(gameRound))

    def gameMenuLoop(self):
        self.paintMainMenu()

    def gameOverLoop(self):
        self.paintGameOver()

    # game loop
    def  gameLoop(self) :
        global gameSpeed
        global gameState
        global gameRound
        global gameScore
        if gameState == 0:
            self.master.after(20, self.gameMenuLoop)

        elif gameState == 1:
            for sprite in self.sprites:
                sprite.move()

            # Check for collisions between objects in the sprite list.
            for  me in self.sprites: 
                for  other in self.sprites :
                    if me != other:
                        if (me.checkCollision(other)) :
                            me.handleCollision(other)
                            other.handleCollision(me)
            self.paintGame(self.canvas)

        # Make sure all enemies are dead.
        # The reason self.sprites should be of length 1 is that the player's ship is inside self.sprites.
        if (self.running == True) and (len(self.sprites)==1):
            gameRound += 1 
            gameSpeed += 10 
            self.initSprites() 
            self.master.after(gameSpeed+(gameRound-1)*5, self.gameLoop)
        if self.running:
            self.master.after(gameSpeed+(gameRound-1)*5, self.gameLoop)
        elif self.running == False:
            self.master.after(gameSpeed+(gameRound-1)*5, self.gameOverLoop)

root = Tk()
# Added function - Set the game program title and game icon
root.title("Space Shooter")
root.iconbitmap("res\\ss.ico")



# Added function - End game menu bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit", command=quit)
menubar.add_cascade(label="Menu", underline=0, menu=filemenu)
root.config(menu=menubar)

# Added function - window size window size resizable (top, bottom, left and right)
root.resizable(False, False)
ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

#Added function - fixed position where Tkinter windows are created - center of screen
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
g = GalagaGame(root)
root.after(10, g.gameLoop())
root.mainloop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------