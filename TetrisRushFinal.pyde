import random 
gameend = False
NUM_ROWS = 20
NUM_COLS = 10

class Block:
    def __init__(self, x, l, w, colour):
        self.x = x
        self.y = 0
        self.l = l
        self.w = w
        self.colour = colour
        self.r = 0
        self.keyHandlers = {LEFT: False, RIGHT: False}
        self.move_speed = 20  

    def horizontalmove(self): #method for moving the blocks left or right upon relevant key presses
        if self.keyHandlers[RIGHT] and self.x < ((NUM_COLS)*20-20) and game.ground_y[(self.x//20)+1]>=self.y: 
            #the second condition ensures that the movement is within the bounds of the board 
            #the third condition ensures that there is no horizontal movement of a block if there is a block next to it      
            self.x += self.move_speed
            self.keyHandlers[RIGHT] = False
        elif self.keyHandlers[LEFT] and self.x >= 20 and game.ground_y[(self.x//20)-1]>=self.y: 
            self.x -= self.move_speed
            self.keyHandlers[LEFT] = False

    def blockdisplay(self): #method for creating block
        if self.colour == "red":
            fill(255, 51, 52)
        elif self.colour == "blue":
            fill(12, 150, 228)
        elif self.colour == "green":
            fill(30, 183, 66)
        elif self.colour == "yellow":
            fill(246, 187, 0)
        elif self.colour == "purple":
            fill(76, 0, 153)
        elif self.colour == "white":
            fill(255, 255, 255)
        elif self.colour == "black":
            fill(0, 0, 0)
        rect(self.x, self.y, self.l, self.w)
    def blockupdate(self): #method for moving the block down by a row every time the method is called
        
        if self.y < game.ground_y[self.x // 20]: #checks the y value of the block against ground value for that column, ensures that block lands on the ground
            self.y += 4
            self.y += 4
            self.y += 4
            self.y += 4
            self.y += 4
class Game:
    def __init__(self):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.blocksize = 20
        self.blocks = [] #list to contain all blocks generated
        self.speed = 0 # controls the speed of the game, check draw() function
        self.a = True
        self.colours = ["red", "blue", "green", "yellow", "purple", "white", "black"] 
        self.blocks.append(Block(random.randint(0,10)*20, 20, 20, random.choice(self.colours))) #appends a block of a random colour to the list so that it is not empty
        self.score = 0
        self.ending = False
        self.availablex = [] #creates a list of all "available x" i.e x values where new blocks can be generated (if a column is fully stacked, it becomes unavailable)
        for r in range(self.cols):
            self.availablex.append(r)
        self.xchosen = 0
        self.ground_y = [] #creates a list of ground level values for each column
        for r in range(NUM_COLS+1):
            self.ground_y.append((NUM_ROWS*20)-20)
    def newblock(self): # method for generating a new block which simultaneously increments the game speed
        if (len(self.blocks) == 0 or self.blocks[-1].y >= self.ground_y[self.blocks[-1].x/20]):
            self.xchosen = random.choice(self.availablex)
            while self.ground_y[self.xchosen]<= -20:
                self.xchosen = random.choice(self.availablex) #the availablex attribute ensures that the random block is generated at a column that is not already filled
            self.blocks.append(Block(self.xchosen*20, 20, 20, random.choice(self.colours)))
            self.speed += 0.25
    def checkend(self): #method to check if the game has ended, if the length of the blocks list is equal to the total number of slots available on the board, it indicates the end of the game
        if len(self.blocks) == NUM_ROWS*NUM_COLS and self.ground_y:
            self.ending = True
        else:
            self.ending = False
    def clearlist(self):
        self.blocks.__init__()
    def placedblocksdisplay(self): #method to ensure that blocks already generated stay displayed on the screen
        for block in self.blocks:
            if self.blocks.index(block) != -1:
                block.blockdisplay()
    def display(self): #method to update the block position and check for 4 vertical blocks of the same colour
        for block in self.blocks:
            block.blockdisplay()
            if self.blocks.index(block) == len(self.blocks)-1:
                block.blockupdate()
                if block.y == self.ground_y[block.x // 20]:
                    self.ground_y[block.x // 20] -= 20
                    #the following sequence of code checks for 4 consecutive vertical blocks of the same colour
                    a = block.x 
                    b = block.y
                    c = block.colour
                    block1 = block
                    for block in self.blocks:
                        if block.x== a and b+20 == block.y and block.colour == c and block.y//20 <19:
                            d = block.x 
                            e = block.y
                            f = block.colour
                            block2 = block
                            for block in self.blocks:
                                if block.x== d and e+20 ==block.y and block.colour == f:
                                    g = block.x 
                                    h = block.y
                                    i = block.colour
                                    block3 = block
                                    for block in self.blocks:
                                        if block.x== g and h+20== block.y and block.colour == i:
                                            block4 = block
                                            #if 4 vertically consecutive blocks of the same colour are found, the ground level is changed, the blocks are removed, the score is incremented and the speed is reset to 0
                                            self.ground_y[block.x // 20] += 80
                                            self.score += 1
                                            self.blocks.remove(block1)
                                            self.blocks.remove(block2)
                                            self.blocks.remove(block3)
                                            self.blocks.remove(block4)
                                            self.speed = 0
        self.newblock()
        self.checkend()

game = Game()
def setup():
    size(NUM_COLS*20,NUM_ROWS*20)
    background(210)

def draw():
    if game.ending == False: #if game.ending is False i.e. the game is still running, grid is displayed, blocks are displayed and the last block is allowed to move down and be moved horizontally. Additionally, we check if the game has ended
        size(NUM_COLS*20,NUM_ROWS*20)
        background(210)
        x = 0
        y = 0
        for r in range(game.rows):
            for c in range(game.cols):
                noFill()
                stroke(180)
                rect(x, y, 20, 20)
                x += 20
            x=0
            y+=20
        game.checkend()
        game.blocks[-1].horizontalmove()
        game.placedblocksdisplay()
        if frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1: #to control the speed of the game i.e. how often a block moves down by 1 row
            game.display()
        fill(0)
        textSize(15)
        text("Score: "+str(game.score),(NUM_COLS*20)-70 , 20)
    elif game.ending == True:
        size(NUM_COLS*20,NUM_ROWS*20)
        background(210)
        fill(0)
        textSize(13)
        text("                  Score: "+str(game.score)+"\n   Click anywhere to replay :)",3 , 100)
        gameend = True

        
def mouseClicked():
    if game.ending == True: #clears list of blocks so that a new game can start, resets speed and score to zero, and resets the ground for the game to its original value too
        game.clearlist() 
        game.display()
        game.score = 0
        game.speed = 0
        game.ground_y = []
        for r in range(NUM_COLS):
            game.ground_y.append((NUM_ROWS*20)-20)
        game.ending = False
        
    
def keyPressed():
    if keyCode == LEFT:
        game.blocks[-1].keyHandlers[LEFT] = True
    elif keyCode == RIGHT:
        game.blocks[-1].keyHandlers[RIGHT] = True

def keyReleased():
    if keyCode == LEFT:
        game.blocks[-1].keyHandlers[LEFT] = False
    elif keyCode == RIGHT:
        game.blocks[-1].keyHandlers[RIGHT] = False
