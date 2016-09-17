from tkinter import *
import copy
from tkinter import *

class Animation(object):
    # run(self) adapted from http://www.cs.cmu.edu/~112/notes/events-example0.py
    ####################################
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
        self.timerDelay = 100 # milliseconds
        self.init(data)
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

        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()

class WelcomeScreen(Animation):
    def __inti__(self):
        self.init()
    def isEnd(self):
        return self.end
    def init(self,data):
        self.end
        # load data.xyz as appropriate
        data.counter = 0
        data.score = 0 ;         data.items = [Boss(data.width/2,30)]
        data.timerDelay = 5 ;         data.numInrow = 9
        data.rTime = round(
            (data.width - (Minions.sizex * data.numInrow*1.5))/Minions.xspeed)
        data.time =data.rTime/2
        # minions
        ini = (data.width - (Minions.sizex * 
            data.numInrow*1.5))/2 + Minions.sizex/2
        for i in range(data.numInrow):
            data.items.append(Minions1((1.5*i)*Minions.sizex + ini+3,100))
        for j in range(0,2):
            for i in range(data.numInrow):
                data.items.append(Minions2((1.5*i)*Minions.sizex + 
                    ini+3,130+30*j))
        for j in range(0,2):
            for i in range(data.numInrow):
                data.items.append(Minions3((1.5*i)*Minions.sizex + 
                    ini+3,190+30*j))
        #player
        data.player = Player(data.width/2,data.height-15)
        data.missile = [] ;         data.end = False
        data.fireTime = 5 ;         data.explosion = []
        #baracade
        data.baracade = []
        for i in range(4):
            data.baracade.append(Baracade(50+66*i,360))
    def mousePressed(self,event, data):
        # use event.x and event.y
        pass
    def keyPressed(self,event, data):
        # use event.char and event.keysym
        if not data.end:
            if event.keysym == "Left" and data.player.x > 5:     
                data.player.movex(True)
            elif event.keysym == 'Right'and data.player.x < data.width -5:  
                data.player.movex(False)
            elif event.keysym == "space" and data.fireTime >= 20:
                if data.score < 1000:
                    data.missile.append(Missile(data.player.getPos(),-10))
                elif data.score < 2500:
                    Missile.sizex = 2
                    data.missile.append(Missile(
                        (data.player.getPos()[0]-3,data.player.getPos()[1])
                         ,-10,"yellow"))
                    data.missile.append(Missile(
                        (data.player.getPos()[0]+3,data.player.getPos()[1])
                        ,-10,"yellow"))
                elif data.score< 3000:
                    Missile.sizex = 2
                    data.missile.append(Missile(
                        (data.player.getPos()[0]-5,data.player.getPos()[1])
                         ,-10,'blue'))
                    data.missile.append(Missile(
                        (data.player.getPos()[0],data.player.getPos()[1])
                         ,-10,'blue'))
                    data.missile.append(Missile(
                        (data.player.getPos()[0]+5,data.player.getPos()[1])
                        ,-10,'blue'))
                else:
                    for i in range (5):
                        data.missile.append(Missile(
                            (data.player.getPos()[0] - 7.5 + 5*i,
                                350 - 20*sin(3.1415926/5*i))
                             ,-10,'blue'))
                data.fireTime = 0
    def timerFired(self,data):
        if data.end: OopyInvaders.score = data.score
        data.fireTime += 1
        data.time +=1
        data.time %= data.rTime
        #move minnions
        movey = False
        if int(data.time) == 0:
            Minions.xspeed = -Minions.xspeed
            data.counter += 1
            if data.counter == 2 :
                movey = True
        for obj in data.items:
            if movey:
                obj.movey(data)
                if obj.y > data.height:
                    data.end = True
            obj.movex(data)
        if movey:
            data.counter = 0
        #minions attack
        if int (data.time) % int(3+50/40*len(data.items)) == 0 and len(
            data.items)!= 0:
            i = randint (0,len(data.items)-1)
            if data.items[i].score == 500:
                data.missile.append(BossLaser(data.items[i].getPos(),5))
            else:data.missile.append(MonsterMissile(data.items[i].getPos(),5))
        #move missile
        for obj in data.missile:
            obj.trace(data)
            obj.movex()
            obj.movey()
        #check collision
        self.baracadeCollision(data)
        self.alienCollision(data)
        pass
    def alienCollision(self,data):
        itemspop,missilepop = [],[]
        for mis in range(len(data.missile)):
            for minion in range(len(data.items)):
                (misx,misy)=(data.missile[mis].getPos()[0],
                        data.missile[mis].getPos()[1])
                if data.missile[mis].y < 0 or data.missile[mis
                ].x > data.width or data.missile[mis].x < 0: missilepop += [mis]
                if data.player.hit(misx,misy):
                    data.player.hp-=data.missile[mis].hp
                    missilepop += [mis]
                    if data.player.hp <= 0:
                        data.end = True
                        return
                    break
                if data.missile[mis].friendly: break
                if data.items[minion].hit(misx,misy):
                    data.items[minion].hp -= data.missile[mis].hp
                    missilepop += [mis]
                    if data.items[minion].hp <= 0 and minion not in itemspop:
                        itemspop += [minion]
                        data.score += data.items[minion].score
                        data.explosion += [Explosion(data.items[minion].x
                            ,data.items[minion].y)]
                    else:
                        data.explosion += [smallerExplosion(data.items[minion].x
                            ,data.items[minion].y)]
                    break
        if missilepop != []:
            newitems,newmis=[],[]
            for mis in range(len(data.missile)):
                if mis not in missilepop:
                    newmis.append(data.missile[mis])
            for minion in range(len(data.items)):
                if minion not in itemspop:
                    newitems.append(data.items[minion])
            data.missile = newmis
            data.items = newitems
    def baracadeCollision(self,data):
        barpop,missilepop = [],[]
        for mis in range(len(data.missile)):
            for baracade in range(len(data.baracade)):
                (misx,misy)=(data.missile[mis].getPos()[0],
                        data.missile[mis].getPos()[1])
                if data.missile[mis].y > data.height or data.missile[mis
                ].x > data.width or data.missile[mis].x < 0 : missilepop+= [mis]
                if data.baracade[baracade].hit(misx,misy):
                    data.baracade[baracade].hp -= data.missile[mis].hp
                    missilepop += [mis]
                    if data.baracade[baracade].hp <= 0:
                        barpop += [baracade]
                        data.explosion += [Explosion(data.baracade[baracade].x
                            ,data.baracade[baracade].y)]
                    else:
                        data.explosion += [smallerExplosion(
                            data.baracade[baracade].x
                            ,data.baracade[baracade].y)]
                    break
        if missilepop != []:
            newbar,newmis=[],[]
            for mis in range(len(data.missile)):
                if mis not in missilepop:
                    newmis.append(data.missile[mis])
            for baracade in range(len(data.baracade)):
                if baracade not in barpop:
                    newbar.append(data.baracade[baracade])
            data.missile = newmis
            data.baracade = newbar
    def redrawAll(self,canvas, data):
        # draw in canvas
        #draw back ground
        canvas.create_rectangle(0,0,data.width,data.height,fill='black',
            width = 0)
        #dtaw items
        for obj in data.items:
            obj.draw(canvas)
        #draw score
        canvas.create_text(data.width/5,20,text = "SCORE",font = "Helvetica 10",
            fill="cyan")
        canvas.create_text(data.width/5,40,text = data.score, 
            font = "Helvetica 10",fill = "white")
        #draw player
        if data.end == True:
            data.explosion.append(Explosion(data.player.x,data.player.y))
            canvas.create_text(data.width/2,data.height/2+20,text = "YOU LOSE",
                font = "Helvetica 40 bold",  fill="white")
        else:
            data.player.draw(canvas)
        #draw missile
        for obj in data.missile:
            obj.draw(canvas)
        #check win
        if len(data.items) == 0:
            canvas.create_text(data.width/2,data.height/2+20,text = "YOU WIN",
                font = "Helvetica 40 bold",  fill="white")
        #draw explosion
        for obj in data.explosion:
            if obj.time <= 20:
                obj.time += 1
                obj.draw(canvas)
        #draw baracade
        for obj in data.baracade:
            obj.draw(canvas)
        #draw hp
        for i in range(data.player.hp):
            canvas.create_rectangle(5+i*15,390,5+i*15+10,400,width =0, 
                fill = 'pink')

from math import cos,sin
from random import randint
import copy
def rgbString(red, green, blue):
    #http://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return "#%02x%02x%02x" % (red, green, blue)

game1 = OopyInvaders()
game1.run()
print(game1.getFinalScore())

game2 = OopyInvaders()
game2.run()
print(game2.getFinalScore())