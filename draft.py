from tkinter import *
from tkinter import ttk
import copy
from random import randint
from lib import *
import random

# Main class runs the whole game and manges transformations between stages.
class Main(object):
    def __init__(self,width,height):
        # self.sceneNum = 0
        self.sceneNum = 2
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
        self.mode=DormScene(self.root)
       # self.mode.keyPressed(event)
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
            self.mode = MapScene(self.root)
        elif (self.sceneNum == 2):
            self.mode = EntropyScene(self.root)

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

class DormScene(Scene):
    def __init__(self,root):
        super().__init__(root)
        self.init(root)

    def mousePressed(self,canvas):
        pass

    def keyPressed(self,canvas):
        pass

    def init(self,root):
        self.refreshText(self.root.dialog, "")
        self.refreshText(self.root.explanation, "")
        self.stageNum=0
        self.totalStage=3
        self.time=0
        self.myImage = PhotoImage(file='dormdoor.gif')
        self.stageStatus = [False] * self.totalStage
        print("WLC SCR Canvas width = {0}, Canvas height {1}".format(self.width, self.height))
        self.time = 0 # timer
        self.textWidth = self.width / 2
        self.textHeight = self.height / 2
        self.textIndexTup = [0,0] # typeWriter effect counter
        self.dormText = "> Welcome to your dorm. \n" \
                        "> Why not meet more people! \n" # typeWriter text

    def timerFired(self):
        self.time += 1
        if self.stageNum == 0:
            if not self.stageStatus[self.stageNum] and self.textIndexTup[0] >= (len(self.dormText) - 1):
                self.stageStatus[self.stageNum] = True
                self.stageNum = min(self.stageNum + 1, self.totalStage - 1)
                self.resetText()
                self.root.editor.config(state="normal")
        elif self.stageNum == 1:
            dialogContent = '''Keep knocking on the next person's door until someone opens
Try the script below and press Command + b to execute:\nwhile(the door is not opened):
    self.knockOnTheNextDoor()'''
            explanationContent = '''Hello!!!!!!'''
            self.refreshText(self.root.dialog, dialogContent)
            self.refreshText(self.root.explanation, explanationContent)
            self.root.explanation.tag_add("blue", "1.0", "1.5")
            self.root.explanation.tag_add("yellow", "1.6", "1.12")
            #   print(self.stageStatus)
            if self.root.content and self.stageStatus[self.stageNum] == False:
                self.getScene1Content()

    def getScene1Content(self):
        try:
            eval(self.root.content)
            if (self.root.content.strip().startswith('print("') and
                self.root.content.strip().endswith('")')):
                self.scene1Content = self.root.content.strip()[7:-2]
                self.stageStatus[self.stageNum] = True
                self.root.editor.config(state="disabled")
               # print(self.root.editor.cget("state"))
        except:
            self.refreshText(self.root.explanation,self.root.explanation.get('1.0',"end")+"\nError!! Please check your"
                                                                                          " code.")
            self.root.explanation.tag_add("blue","1.0","1.5")
            self.root.explanation.tag_add("yellow","1.6","1.12")
            self.root.explanation.tag_add("error","end -{0}c".format(len("Error!! Please check your code.")+1),"end")


    def resetText(self,width = -1,height = -1):
        self.textIndexTup = [0,self.time]
        if(width == -1):
            width = self.textWidth
        if height == -1:
            height = self.textHeight
        self.textWidth = width
        self.textHeight = height

    def redrawAll(self,canvas):
        self.root.canvas.create_image(0,0,image=self.myImage,anchor=NW)
        if self.stageNum == 0:
            if (self.dormText[self.textIndexTup[0]].isalpha()):
                if (self.time - self.textIndexTup[1] > randint(3,4)):
                    self.textIndexTup[0] = min(self.textIndexTup[0]+1, len(self.dormText) - 1)
                    self.textIndexTup[1] = self.time
                else:
                    pass
            else:
                if (self.time - self.textIndexTup[1] > randint(4,6)):
                    self.textIndexTup[0] = min(self.textIndexTup[0]+1, len(self.dormText) - 1)
                    self.textIndexTup[1] = self.time
                else:
                    pass
            textIndex = self.textIndexTup[0]
            printedText = self.dormText[0:textIndex]
            canvas.create_text(self.textWidth,self.textHeight,text=printedText,font = "Calibri 25", fill = "white")
        elif self.stageNum == 1:
            canvas.create_text(self.textWidth, self.textHeight, text=self.dormText, font="Calibri 25", fill="white")

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
            self.refreshText(self.root.explanation,self.root.explanation.get('1.0',"end")+"\nError!! Please check your"
                                                                                          " code.")
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
    def __init__(self,root):
        super().__init__(root)
        self.init(root)
        self.root.editor.configure(state="normal")
        self.root.editor.delete('1.0', 'end')
        self.root.content = ""
        self.commands = []
        self.counter = 0
        self.stageNum = 0
        dialogContent = '''It's time to go back to your dorm Donner. 
Please use the command that we provided to move to donner.'''
        explanationContent = '''Available Commands:
me.moveRight()
me.moveLeft()
me.moveUp()
me.moveDown()'''
        self.refreshText(self.root.dialog,dialogContent)
        self.refreshText(self.root.explanation,explanationContent)

    def init(self,root):
        self.mapbg = PhotoImage(file = "map.gif")
        self.location = [0,0]
        self.headImg = PhotoImage(file = "head.gif")
        self.locations = [[[None,None]] * 3 for i in range(3)]
        self.locations[0][0] = (328,88)
        self.locations[1][0] = (335,321)
        self.locations[2][0] = (334,499)
        self.locations[1][1] = (430,322)
        self.locations[1][2] = (602,322)
        self.locations[2][1] = (522,492)
        self.locations[2][2] = (644,503)

    def mousePressed(self,event):
        pass

    def timerFired(self):
        if self.stageNum != 1:
            if self.root.content:
                self.commands = list(self.root.content.splitlines())
                self.root.content = ""
                explanationContent = '''Available Commands:
me.moveRight()
me.moveLeft()
me.moveUp()
me.moveDown()'''
                self.refreshText(self.root.explanation,explanationContent)
            if self.commands:
                self.counter += 1
                if self.counter % 20 == 0:
                    move = self.commands.pop(0)
                    if self.isLegalMove(move):
                        if move == "me.moveRight()":
                            self.location[0],self.location[1] = self.location[0],self.location[1]+1
                        elif move == "me.moveLeft()":
                            self.location[0],self.location[1] = self.location[0],self.location[1]-1
                        elif move == "me.moveUp()":
                            self.location[0],self.location[1] = self.location[0]-1,self.location[1]
                        elif move == "me.moveDown()":
                            self.location[0],self.location[1] = self.location[0]+1,self.location[1]
                    else:
                        self.refreshText(self.root.explanation,self.root.explanation.get('1.0',"end")+"\nError!! Please check your code.")
                        self.root.explanation.tag_add("error","end -{0}c".format(len("Error!! Please check your code.")+1),"end")
                    if self.location == [2,2]:
                        self.stageNum = 1

    def redrawAll(self,canvas):
        canvas.create_image(0,0,anchor = NW,image=self.mapbg)
        for row in range(len(self.locations)):
            for col in range(len(self.locations[row])):
                for i in (-1,0,1):
                    if self.locations[row][col] != [None,None]:
                        if (row+i) in (0,1,2) and self.locations[row+i][col] != [None,None]:
                            canvas.create_line(self.locations[row][col][0],self.locations[row][col][1],
                                self.locations[row+i][col][0],self.locations[row+i][col][1],fill = "turquoise2",width=5)
                        if (col+i) in (0,1,2) and self.locations[row][col+i] != [None,None]:
                            canvas.create_line(self.locations[row][col][0],self.locations[row][col][1],
                                self.locations[row][col+i][0],self.locations[row][col+i][1],fill = "turquoise2",width=5)
        for row in range(len(self.locations)):
            for col in range(len(self.locations[row])):
                if self.locations[row][col] != [None,None]:
                    canvas.create_oval(self.locations[row][col][0]-10,self.locations[row][col][1]-10,
                        self.locations[row][col][0]+10,self.locations[row][col][1]+10,fill = "DodgerBlue2")
        canvas.create_image(self.locations[self.location[0]][self.location[1]][0],self.locations[self.location[0]][self.location[1]][1],anchor = CENTER,image=self.headImg)
        if self.stageNum == 1:
            canvas.create_text(self.width//2,self.height//2,anchor=CENTER,text="You are back to Donner!",font = "Times 50",fill = "blue")

    def isLegalMove(self,command):
        if command == "me.moveRight()":
            if (self.location[1] + 1) in (0,1,2) and self.locations[self.location[0]][self.location[1]+1] != [None,None]:
                return True
            else:
                return False
        elif command == "me.moveLeft()":
            if (self.location[1] - 1) in (0,1,2) and self.locations[self.location[0]][self.location[1]-1] != [None,None]:
                return True
            else:
                return False
        elif command == "me.moveUp()":
            if (self.location[0] - 1) in (0,1,2) and self.locations[self.location[0]-1][self.location[1]] != [None,None]:
                return True
            else:
                return False
        elif command == "me.moveDown()":
            if (self.location[0] + 1) in (0,1,2) and self.locations[self.location[0]+1][self.location[1]] != [None,None]:
                return True
            else:
                return False
        else:
            return False

class EntropyScene(Scene):
    def __init__(self,root):
        super().__init__(root)
        self.init(root)

    def init(self,root):
        self.entropybg = PhotoImage(file = "entropy.gif")
        self.root.editor.configure(state="normal")
        self.root.editor.delete('1.0', 'end')
        self.root.content = ""
        self.stageNum = 0
        self.dialogContent = '''Your friend asked you to buy him a gluten free bread, you need to see the back of the package to see if it
is halal. You can either see the bags one by one by using:
bread1.see()
bread2.see()
bread3.see()
or you can use a loop like:

for bread in shelf:
    bread.see()'''
        self.explanationContent = '''Available Commands:
bread.see()
for loop'''
        self.refreshText(self.root.dialog,self.dialogContent)
        self.refreshText(self.root.explanation,self.explanationContent)
        self.shelf = [random.choice([0,1,2]) for i in range(14)]
        print(self.shelf)
        self.result = ""

    def redrawAll(self,canvas):
        canvas.create_image(0,0,anchor = NW,image=self.entropybg)
        if self.result:
            canvas.create_text(self.width//2,self.height//2,anchor=CENTER,text="{}".format(self.result),font = "Times 50",fill = "blue")

    def timerFired(self):
        if self.stageNum == 0:
            if self.root.content:
                for line in self.root.content.splitlines():
                    if line.endswith(".see()") and line.startswith("bread"):
                        try:
                            if self.shelf[int(line[5])] == 1:
                                self.root.editor.configure(state = "disabled")
                                self.result = "Yes you found it!"
                                self.stageNum = 1
                            else:
                                self.result = "No it is not gluten free."
                        except:
                            pass
                if self.root.content.startswith("for bread in shelf"):
                    for i in range(len(self.shelf)):
                        if self.shelf[i] == 1:
                            self.result = "You find that bread {0} is gluten free".format(i)
                            self.stageNum = 1
                            return None
                    self.result = "No bread is gluten free :("

main = Main(600,700)
main.run()