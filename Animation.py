from tkinter import *
import copy
from tkinter import *

class Animation(object):
    # run(self) adapted from http://www.cs.cmu.edu/~112/notes/events-example0.py
    # parent class of event based animation objects.
    def run(self, width=1026, height=768):
        def redrawAllWrapper(canvas):
            canvas.delete(ALL)
            self.redrawAll(canvas)
            canvas.update()    

        def mousePressedWrapper(event, canvas):
            self.mousePressed(event)
            redrawAllWrapper(canvas)

        def keyPressedWrapper(event, canvas):
            self.keyPressed(event)
            redrawAllWrapper(canvas)

        def timerFiredWrapper(canvas):
            self.timerFired()
            redrawAllWrapper(canvas)
            # pause, then call timerFired again
            canvas.after(self.timerDelay, timerFiredWrapper, canvas)
        # Set up data and call init
        self.width = width
        self.height = height
        self.timerDelay = 10 # milliseconds
        self.init()
        # create the root and the canvas
        root = Tk()
        canvas = Canvas(root, width=self.width, height=self.height)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas))
        timerFiredWrapper(canvas)
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")

    def redrawAll(self,canvas):
        pass
    def mousePressed(self,canvas):
        pass
    def keyPressed(self,canvas):
        pass
    def timerFired(self):
        pass
    def init(self):
        pass

class WelcomeScreen(Animation):
    def __inti__(self):
        self.init()
    def isEnd(self):
        return self.end
    def init(self):
        self.end = False
        self.time = 0
        self.textIndexTup = [0,0]
        self.welcomeText = "> Hi There, \n> Welcome to CMU\n"
    def mousePressed(self,event):
        # use event.x and event.y
        pass
    def keyPressed(self,event):
        # # use event.char and event.keysym
        # if not self.end:
        #     if event.keysym == "Left" and data.player.x > 5:
        #         data.player.movex(True)
        #     elif event.keysym == 'Right'and data.player.x < data.width -5:
        #         data.player.movex(False)
        #     elif event.keysym == "space" and data.fireTime >= 20:
        #         if data.score < 1000:
        #             data.missile.append(Missile(data.player.getPos(),-10))
        #         elif data.score < 2500:
        #             Missile.sizex = 2
        #             data.missile.append(Missile(
        #                 (data.player.getPos()[0]-3,data.player.getPos()[1])
        #                  ,-10,"yellow"))
        #             data.missile.append(Missile(
        #                 (data.player.getPos()[0]+3,data.player.getPos()[1])
        #                 ,-10,"yellow"))
        #         elif data.score< 3000:
        #             Missile.sizex = 2
        #             data.missile.append(Missile(
        #                 (data.player.getPos()[0]-5,data.player.getPos()[1])
        #                  ,-10,'blue'))
        #             data.missile.append(Missile(
        #                 (data.player.getPos()[0],data.player.getPos()[1])
        #                  ,-10,'blue'))
        #             data.missile.append(Missile(
        #                 (data.player.getPos()[0]+5,data.player.getPos()[1])
        #                 ,-10,'blue'))
        #         else:
        #             for i in range (5):
        #                 data.missile.append(Missile(
        #                     (data.player.getPos()[0] - 7.5 + 5*i,
        #                         350 - 20*sin(3.1415926/5*i))
        #                      ,-10,'blue'))
        #         data.fireTime = 0
        pass
    def timerFired(self):
        self.time+=1
        pass
    def redrawAll(self,canvas):
        #draw in canvas
        #draw back ground
        canvas.create_rectangle(0,0,self.width,self.height,fill='black', width = 0)
        #draw <<

        if (self.welcomeText[self.textIndexTup[0]].isalpha()):
            if (self.time - self.textIndexTup[1] > randint(3,4)):
                self.textIndexTup[0] = min(self.textIndexTup[0]+1, len(self.welcomeText) - 1)
                self.textIndexTup[1] = self.time
            else:
                pass
        else:
            if (self.time - self.textIndexTup[1] > randint(4,6)):
                self.textIndexTup[0] = min(self.textIndexTup[0]+1, len(self.welcomeText) - 1)
                self.textIndexTup[1] = self.time
            else:
                pass
        textIndex = self.textIndexTup[0]
        printedText = self.welcomeText[0:textIndex]
        canvas.create_text(self.width/2,self.height/2,text=printedText,font = "Calibri 25", fill = "white")

from math import cos,sin
from random import randint

def rgbString(red, green, blue):
    #http://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return "#%02x%02x%02x" % (red, green, blue)

scene1 = WelcomeScreen()
scene1.run(1024,768)