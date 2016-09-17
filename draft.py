from tkinter import *
from tkinter import ttk
import copy
from random import randint
from lib import *
import re

# Main class runs the whole game and manges transformations between stages.
class Main(object):
    def __init__(self,width,height):
        self.sceneNum = 0
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
        self.root.content = ""
        #global func
        self.root.bind("<Command-b>", lambda event:
                                self.getUserInput())
        self.root.bind("<Control-b>",lambda event:
                                self.getUserInput())
        recolorizeAll(self.root.editor,self.root)
        # updateLineNumber(root)
        # root.words = reservedWords()
        # root.listbox = Listbox(root.text)
        # redirect closing window to a confirmation message

    def getUserInput(self):
        self.root.content = self.root.editor.get("1.0", "end")

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
                           insertbackground="white",state="disabled")
        root.canvas.grid(row=0, column=0)
        root.dialog.grid(row=1, column=0, sticky="WE")
        root.editor = Text(root, background="gray13", foreground='white', wrap="none",
                           borderwidth=0, highlightthickness=0, undo=True,
                           insertbackground="white",state="disabled")
        root.editor.grid(row=0, column=1, sticky="NS")
        root.explanation = Text(root, background="bisque2", foreground='black', wrap="none",
                                borderwidth=0, highlightthickness=0, undo=True,
                                insertbackground="black",state="disabled")
        root.explanation.grid(row=1, column=1, sticky="S")
        root.explanation.tag_configure("yellow",foreground = "#ff4500")
        root.explanation.tag_configure("blue",foreground = "#64d6eb")
        root.explanation.tag_configure("green",foreground = "green2")
        root.explanation.tag_configure("red",foreground = "red")
        root.explanation.tag_configure("error",foreground = "red",underline=1,background="yellow")

    def redrawAll(self,canvas):
        self.mode.redrawAll(canvas)
    def mousePressed(self,event):
        self.mode.mousePressed(event)
    def keyPressed(self,event):
        self.mode.keyPressed(event)
    def timerFired(self):
        self.mode.timerFired()
        if self.mode.isEnd():
            self.sceneNum +=1
            if type(self.mode) == MapScene :
                self.cacheScene()
                self.buildScene()
            else:
                self.loadScene()
    def init(self):
        self.buildScene()
    def buildScene(self):
        if (self.sceneNum == 0):
            self.mode = WelcomeScreen(self.root)
        elif (self.sceneNum == 1):
            self.mode = MapScene()
    def cacheScene(self):
        self.sceneCache = self.mode
    def loadScene(self):
        self.mode = self.sceneCache
# Scene class parent that dispatch the actual drawing and interaction with text widgets
class Scene(object):
    def __init__(self,root):
        self.root = root
        self.end = False
        self.root.update_idletasks()
        self.width, self.height = (self.root.canvas.winfo_width(), self.root.canvas.winfo_height())
    def isEnd(self):
            return self.end
    def redrawAll(self,canvas):
        pass
    def mousePressed(self,event):
        pass
    def keyPressed(self,event):
        pass
    def timerFired(self):
        pass
    def init(self,root):
        pass

    def refreshText(self,text, content):
        text.configure(state="normal")
        text.delete('1.0', 'end')
        text.insert('1.0', content)
        text.config(state="disabled")


class WelcomeScreen(Scene):
    def __init__(self,root):
        super().__init__(root)
        self.init(root)
    def init(self,root):
        # text editor stage number
        # will be update when a stage is finished
        # need to be checked by text interactive widget to decide phase
        self.stageNum = 0
        self.totalStage = 9
        self.stageStatus = [False] * self.totalStage
        print("WLC SCR Canvas width = {0}, Canvas height {1}".format(self.width, self.height))
        self.time = 0 # timer
        self.textWidth = self.width / 2
        self.textHeight = self.height / 2
        self.textIndexTup = [0,0] # typeWriter effect counter
        self.welcomeText = "> Hi There, \n> Welcome to CMU" # typeWriter text
    def resetText(self,width = -1,height = -1):
        self.textIndexTup = [0,self.time]
        if(width == -1):
            width = self.textWidth
        if height == -1:
            height = self.textHeight
        self.textWidth = width
        self.textHeight = height
    def mousePressed(self,event):
        # use event.x and event.y
        pass
    def keyPressed(self,event):
        pass
    def timerFired(self):
        self.time+=1
        if self.stageNum == 0:
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage-1)
                self.root.editor.config(state="normal")
        elif self.stageNum == 1:
            dialogContent = '''Hi, let's make a call! Use print() function to yell something!
Try the script below and press Command + b to execute:\nprint("Hello")'''
            explanationContent = '''print(String) is a function which take in a String type .
You can try to replace the "Hello" with other things'''
            self.refreshText(self.root.dialog,dialogContent)
            self.refreshText(self.root.explanation,explanationContent)
            self.root.explanation.tag_add("blue","1.0","1.5")
            self.root.explanation.tag_add("yellow","1.6","1.12")
            if self.root.content and self.stageStatus[self.stageNum] == False:
                if (self.getScene1Content()): # move forward
                    self.stageStatus[self.stageNum] = True
                    self.stageNum += 1
                    self.welcomeText =  self.welcomeText +"\n" + "> Me: " + self.scene1Content
        elif self.stageNum == 2: # restart typewriter prints
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage-1)
                self.welcomeText = (self.welcomeText + "\n" +
                                    "> How many pieces of luggage do you have?")
        elif self.stageNum == 3: # restart typewriter prints
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage-1)
                self.root.editor.config(state="normal")
                self.root.editor.delete("1.0", "end")

        elif self.stageNum == 4:
            dialogContent = '''Type in number of luggage you have using statement\n\t\tluggage = int\n\tPress Command + b to execute:\n'''
            explanationContent = '''var = int\n will give value of int to variable var'''
            self.refreshText(self.root.dialog, dialogContent)
            self.refreshText(self.root.explanation, explanationContent)
            self.root.explanation.tag_add("red", "1.4", "1.5")
            self.root.explanation.tag_add("orange", "1.6", "1.9")
            if self.root.content and self.stageStatus[self.stageNum] == False:
                if (self.getScene1Content()): # move forward
                    self.stageStatus[self.stageNum] = True
                    self.stageNum += 1
                    # print("+1")
                    self.welcomeText =  self.welcomeText +"\n" + "> Me: I have " + str(self.scene1Content.split(" ")[-1]) + "."

        elif self.stageNum == 5:
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage-1)
                self.welcomeText = (self.welcomeText + "\n" +
                                    "> Let's go to dorm?")
        elif self.stageNum == 6:
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage - 1)
                self.root.editor.config(state="normal")
                self.root.editor.delete("1.0", "end")

        elif self.stageNum == 7:
            dialogContent = '''Type in boolean value True or False\n\tPress Command + b to execute:\n'''
            explanationContent = '''True or False are the boolean values in python'''
            self.refreshText(self.root.dialog, dialogContent)
            self.refreshText(self.root.explanation, explanationContent)
            self.root.explanation.tag_add("red", "1.4", "1.5")
            self.root.explanation.tag_add("orange", "1.6", "1.9")
            if self.root.content and self.stageStatus[self.stageNum] == False:
                if (self.getScene1Content()): # move forward
                    self.stageStatus[self.stageNum] = True
                    self.stageNum += 1
                    self.welcomeText =  self.welcomeText +"\n" + "> Me: Okay"
        elif self.stageNum == 8:
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.welcomeText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage - 1)
                self.end = True
    def getScene1Content(self):
        try:
            if self.stageNum == 1:
                eval(self.root.content)
                if (self.root.content.strip().startswith('print("') and
                    self.root.content.strip().endswith('")')):
                    self.scene1Content = self.root.content.strip()[7:-2]
                    self.root.editor.config(state="disabled")
                    return True
            elif self.stageNum == 4:
                # print("in 4: " + self.root.content.strip().split(" ")[-1])
                self.scene1Content = self.root.content.strip()
                if (self.root.content.strip().startswith("luggage") and
                        self.root.content.strip().split(" ")[-1].isdecimal()):
                    return True
                else:
                    return False
            elif self.stageNum == 7:
                self.scene1Content = self.root.content.strip()
                if (self.root.content.strip() == "True" or self.root.content.strip() == "False"):
                    return True
                else:
                    return False
            print("undefined num case")
        except:
            self.refreshText(self.root.explanation,self.root.explanation.get('1.0',"end")+"\nError!! Please check your code.")
            self.root.explanation.tag_add("blue","1.0","1.5")
            self.root.explanation.tag_add("yellow","1.6","1.12")
            self.root.explanation.tag_add("error","end -{0}c".format(len("Error!! Please check your code.")+1),"end")
            return False

    def redrawAll(self,canvas):
        #draw in canvas
        #draw back ground
        canvas.create_rectangle(0,0,self.width,self.height,fill='black', width = 0)
        #draw <<
        if self.stageNum == 0 or self.stageNum == 2 or self.stageNum == 3 or self.stageNum == 5 or self.stageNum == 6 or self.stageNum == 8:
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
            textIndex = self.textIndexTup[0]+1
            printedText = self.welcomeText[0:textIndex]
            canvas.create_text(self.textWidth,self.textHeight,text=printedText,font = "Calibri 25", fill = "white")
        elif self.stageNum == 1 or self.stageNum == 4 or self.stageNum == 7:
            canvas.create_text(self.textWidth, self.textHeight, text=self.welcomeText, font="Calibri 25", fill="white")
class MapScene(Scene):
    pass
main = Main(600,700)
main.run()