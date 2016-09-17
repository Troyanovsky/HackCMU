from tkinter import *
from tkinter import ttk
import copy
from random import randint
from lib import *

# Main class runs the whole game and manges transformations between stages.
class Main(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.timerDelay = 10
        # create the root and the canvas
        self.root = Tk()
        self.initFrames(self.root)
        #global func
        initTags(self.root.editor)
        self.root.time = 0
        self.init()
        #global func
        recolorizeAll(self.root.editor,self.root)
        # updateLineNumber(root)
        # root.words = reservedWords()
        # root.listbox = Listbox(root.text)
        # redirect closing window to a confirmation message

    # run(self) adapted from http://www.cs.cmu.edu/~112/notes/events-example0.py
    def run(self):
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
        # set up events
        self.root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, self.root.canvas))
        self.root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, self.root.canvas))
        timerFiredWrapper(self.root.canvas)

        # and launch the app
        self.root.update_idletasks()
        # get actual width
        print("Canvas width = {0}, Canvas height {1}".format(self.width, self.height))
        self.root.mainloop()  # blocks until window is closed
        print("bye!")

    def initFrames(self,root):
        root.canvas = Canvas(root, background="black", height=self.width, width=self.height)
        root.dialog = Text(root, background="gray13", foreground='white', wrap="none",
                           borderwidth=0, highlightthickness=0, undo=True,
                           insertbackground="white")
        root.canvas.grid(row=0, column=0)
        root.dialog.grid(row=1, column=0, sticky="WE")
        root.editor = Text(root, background="gray13", foreground='white', wrap="none",
                           borderwidth=0, highlightthickness=0, undo=True,
                           insertbackground="white")
        root.editor.grid(row=0, column=1, sticky="NS")
        root.explanation = Text(root, background="bisque2", foreground='black', wrap="none",
                                borderwidth=0, highlightthickness=0, undo=True,
                                insertbackground="black")
        root.explanation.grid(row=1, column=1, sticky="S")

    def redrawAll(self,canvas):
        self.mode.redrawAll(canvas)
    def mousePressed(self,canvas):
        self.mode.mousePressed(canvas)
    def keyPressed(self,canvas):
        self.mode.keyPressed(canvas)
    def timerFired(self):
        self.mode.timerFired()
    def init(self):
        self.mode = WelcomeScreen(self.root)

# Scene class parent that dispatch the actual drawing and interaction with text widgets
class Scene(object):
    def __init__(self,root):
        self.root = root
        self.end = False

        # text editor stage number
        # will be update when a stage is finished
        # need to be checked by text interactive widget to decide phase
        self.stageNum = 0
        self.stageNext = False
        self.root.update_idletasks()
        self.width, self.height = (self.root.canvas.winfo_width(), self.root.canvas.winfo_height())
    def isEnd(self):
            return self.end
    def redrawAll(self,canvas):
        pass
    def mousePressed(self,canvas):
        pass
    def keyPressed(self,canvas):
        pass
    def timerFired(self):
        pass
    def init(self,root):
        pass
class WelcomeScreen(Scene):
    def __init__(self,root):
        super().__init__(root)
        self.init(root)
    def init(self,root):
        print("WLC SCR Canvas width = {0}, Canvas height {1}".format(self.width, self.height))
        self.time = 0 # timer
        self.textWidth = self.width / 2
        self.textHeight = self.height / 2
        self.textIndexTup = [0,0] # typeWriter effect counter
        self.welcomeText = "> Hi There, Welcome to CMU\n" # typeWriter text
    def resetText(self,width = -1,height = -1):
        self.textIndexTup = [0,self.time]
        self.textWidth = width
        self.textHeight = height
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
        if not self.stageNext and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
            self.stageNum += 1
            self.stageNext = True
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
        canvas.create_text(self.textWidth,self.textHeight,text=printedText,font = "Calibri 25", fill = "white")

main = Main(600,700)
main.run()


