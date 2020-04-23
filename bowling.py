import pyglet
import math
# imports pyglets library
import random
from pyglet.window import Window, mouse, gl, key
#from pyglet.media import avbin
 
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
 
mygame = pyglet.window.Window(800, 710,                     # setting window
              resizable=False,  
              caption="BOWLING",  
              config=pyglet.gl.Config(double_buffer=True),  # Avoids flickers
              vsync=False                                   # For flicker-free animation
              )                                             # Calling base class constructor
mygame.set_location(screen.width // 2 - 200,screen.height//2 - 350)
 
bimage = pyglet.resource.image('ball2.png')                 # Image for brick
bimage.anchor_x= bimage.width/2
bimage.anchor_y=bimage.height/2
ballsprite= pyglet.sprite.Sprite(bimage, 400, 60)

bgimage= pyglet.resource.image('bac.png')
pinimage = pyglet.resource.image('pin5.png')
#pinimage.anchor_x=pinimage.width/2
pin1sprite =  pyglet.sprite.Sprite(pinimage, 300, 530)
pin2sprite =  pyglet.sprite.Sprite(pinimage, 334, 530)
pin3sprite =  pyglet.sprite.Sprite(pinimage, 368, 530)
pin4sprite =  pyglet.sprite.Sprite(pinimage, 402, 530)
pin5sprite =  pyglet.sprite.Sprite(pinimage, 318, 520)
pin6sprite =  pyglet.sprite.Sprite(pinimage, 352, 520)
pin7sprite =  pyglet.sprite.Sprite(pinimage, 386, 520)
pin8sprite =  pyglet.sprite.Sprite(pinimage, 336, 510)
pin9sprite =  pyglet.sprite.Sprite(pinimage, 370, 510)
pin10sprite =  pyglet.sprite.Sprite(pinimage, 354, 500)
arrowimage= pyglet.resource.image('arrow4.png')
arrowimage.anchor_x= arrowimage.width/2
arrowsprite = pyglet.sprite.Sprite(arrowimage, 400, 60)

inst=pyglet.resource.image('help.png')
instsprite=pyglet.sprite.Sprite(inst, 0, 0)                 # sprite for help an instructions
instsprite.visible=False

menuimage = pyglet.resource.image('menu.png')
menusprite = pyglet.sprite.Sprite(menuimage, 0, 0)          # sprite for menu
menusprite.visible= True


abcimage=pyglet.resource.image('abc.png')                   #shutter sprite            
abcsprite= pyglet.sprite.Sprite(abcimage, 220, 620)
abcsprite.visible=False

scoreboard=pyglet.resource.image('scoreboard.png')           #scoreboard sprite
scoreboard= pyglet.sprite.Sprite(scoreboard, 18, 619)
scoreboard.visible=True

bowlsound = pyglet.resource.media("Ball_Return.wav", streaming = False) #sounds to play
sparesound=pyglet.resource.media("SPARE.wav", streaming = False)
guttersound=pyglet.resource.media("gutter.wav", streaming = False)
strikesound=pyglet.resource.media("strike.wav", streaming = False)
fallsound=pyglet.resource.media("close.wav", streaming = False)



move=False
lis = [pin1sprite, pin2sprite, pin3sprite,pin4sprite, pin5sprite, pin6sprite, pin7sprite,pin8sprite,pin9sprite,pin10sprite] #list of pin sprites
s=1
c=0
angle=0
lis2=[]
cond = False
frame=0
b=False
t=0
m1=0
m2=0
g1=0
g2=0
total=0
summed=0
lock= True
lock2=False
lock3=False
v=0
p=0

sparelabel = pyglet.text.Label("",
                             font_name='Comic Sans MS',
                             font_size=48,
                             x=400, y=400,
                             anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))
strikelabel = pyglet.text.Label("",
                             font_name='Comic Sans MS',
                             font_size=48,
                             x=400, y=400,
                             anchor_x='center', anchor_y='center', color=(255, 0, 0, 255))
scores=[]
for i in range(20):
    scores.append(pyglet.text.Label("",
                                 font_name='Comic Sans MS',
                                 font_size=20,
                                 x=33*(i+1), y=(653+684)/2,
                                 anchor_x='center', anchor_y='center', color=(0, 0, 0, 255)))
sums=[]

for i in range(10):
    sums.append(pyglet.text.Label("",
                                 font_name='Comic Sans MS',
                                 font_size=20,
                                 x=40*(i+1)+ 25*i, y=640,
                                 anchor_x='center', anchor_y='center', color=(0, 0, 0, 255)))
totallabel=pyglet.text.Label("",
                                 font_name='Comic Sans MS',
                                 font_size=30,
                                 x=735, y=660,
                                 anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))


def hit(i,j):                                                              #checks collision
    global ballsprite
    
    topa=j.y+j.height/2
    bottoma=j.y-j.height/2
    righta=j.x+j.width/2
    lefta=j.x-j.width/2

    topb=i.y+i.height
    bottomb=i.y
    rightb=i.x+i.width
    leftb=i.x

    if bottoma >= topb :
        return False
    if topa <= bottomb:
        return False
    if righta <= leftb :
        return False
    if lefta >= rightb:
        return False
    return True;                                                         #returns true if ball collides with pins

def fall(a):                                                             #pushes pins down if coliision is true
    
    global lis,lis2, frame, length1, m2, m1, g1, g2
    
    
    f=True
   
    for i in lis:
        if i not in lis2 and i.visible== True:
            if hit(i,a)==True:
                lis2.append(i)
                r=random.randint(1,2)
                if r==1:
                    i.rotation =83
                elif r==2:
                    i.rotation =-85
                if frame%2==0:
                    m2+=1
                    g2+=1
                    
                elif frame%1==0:
                    m1+=1
                    g1+=1
                sparesound.play()                                      #soud of falling pins played
                

def arrange():                                                          #arranges pins in original order
    global frame, lis, lis2
    a=0
    if frame%2==0 or len(lis2)==10:
        for i in range(4):
            lis[i].x=300+a
            lis[i].y=530
            a+=34
        a=0
        for j in range(4,7):
            lis[j].x=318+a
            lis[j].y=520
            a+=34
        a=0
        for k in range(7,9):
            lis[k].x=336+a
            lis[k].y=510
            a+=34
        lis[9].x=354
        lis[9].y=500
        lis[9].visible=True
            
        for i in lis:
            i.rotation = 0
            i.visible=True        
        
@mygame.event

def on_draw():                                                                   # draws all the sprites
     
    mygame.clear()
    bgimage.blit(0,0)
    pin1sprite.draw()
    pin2sprite.draw()
    pin3sprite.draw()
    pin4sprite.draw()
    pin5sprite.draw()
    pin6sprite.draw()
    pin7sprite.draw()
    pin8sprite.draw()
    pin9sprite.draw()
    pin10sprite.draw()
    arrowsprite.draw()
    ballsprite.draw()
    abcsprite.draw()
    sparelabel.draw()
    strikelabel.draw()
    scoreboard.draw()
    
    totallabel.draw()
    for i in range(20):
        scores[i].draw()
    for i in range(10):
        sums[i].draw()
    menusprite.draw()
    instsprite.draw()


@mygame.event
def on_mouse_release(x, y, button, modifiers):                                    # takes users mouse input
    global frame, lis, lis2, c, b, s, t, angle, cond, b, t, m1, m2, lock, lock2, lock3, ballsprite, g1, g2
    
    
    if menusprite.visible== True :                                              # menu selection
        if button==mouse.LEFT: 
            if (277 <= x <= 478) and (388 <= y <= 460):                         # if play selected
                menusprite.visible= False
##                backsprite.visible=True
            elif (277 <= x <= 478) and (292 <= y <= 368):                       # if help selected
                instsprite.visible=True
                menusprite.visible= False
            elif (277 <= x <= 478) and (202 <= y <= 276):                        # if quit selected
                mygame.close()
            
    elif menusprite.visible== False and instsprite.visible== True:              # help instructions
        if button==mouse.LEFT:
            if( 661 <= x <= 778) and ( 20 <= y <= 61):                          # if back is pressed
                instsprite.visible=False
                menusprite.visible=True
    elif menusprite.visible== False  and instsprite.visible==False:             # if back is pressed during game
        if button==mouse.LEFT:
            if frame< 21:
                menusprite.visible= True
            else:                                                                #restarts and initializes all variables
                x=0
                y=0
                s=1
                c=0
                angle=0
                lis2=[]
                cond = False
                frame=0
                b=False
                t=0
                m1=0
                m2=0
                g1=0
                g2=0
                lock= True
                lock2=False
                lock3=False
                ballsrpite.x=400
                ballsprite.y=60
                a=0
                menusprite.visible=True
                for i in range(4):
                    lis[i].x=300+a
                    lis[i].y=530
                    a+=34
                a=0
                for j in range(4,7):
                    lis[j].x=318+a
                    lis[j].y=520
                    a+=34
                a=0
                for k in range(7,9):
                    lis[k].x=336+a
                    lis[k].y=510
                    a+=34
                lis[9].x=354
                lis[9].y=500
                lis[9].visible=True
                    
                for i in lis:
                    i.rotation = 0
                    i.visible=True

                for j in range(20):
                    scores[j].text=""
                for k in range(10):
                    sums[k].text=""                                    
                            
    

@mygame.event

def on_key_press(symbol, modifiers):                                         #takes key input if gamescreen is on only

    global move, angle, frame, b, lis2,m1, m2, g1, g2, t, summed, total

    if menusprite.visible== False  and instsprite.visible==False :
        if arrowsprite.visible==True:
            if symbol == key.RIGHT:                                          #rotates arrow towards right if right key pressed
                if angle<40:
                    arrowsprite.rotation+=5
                    angle+=5
            elif symbol==key.LEFT:                                           #rotates arrow towards left if left key pressed
                if angle>-40:
                    arrowsprite.rotation-=5
                    angle-=5
            if symbol == key.SPACE:                                          #moves ball if space bar pressed
                bowlsound.play()
                move = True
                print(angle)
                arrowsprite.visible=False
                b=False
                lis2=[]
                t=0
                if frame%2==0:
                    total+=g1+g2
                    g1=0
                    g2=0
                    
            
    
def update(dt):
    global c, angle,s,move, lis2, cond, b, frame, lis, sparelabel,t, m1, m2, g1, g2,lock, lock2, lock3, summed, v, total, p
    if menusprite.visible== False and instsprite.visible==False:
    
        angler= (angle*3.1416)/180
        if move==True:
            fall(ballsprite)                                                           #fall function called
            c+=1

            if angle == 20 and ballsprite.x>=560.4 and ballsprite.y>=500.7:           #gutter balls
                guttersound.play()
                s=0.6
                lock=False
                lock2=True
            if angle == 25 and ballsprite.x>=584.292 and ballsprite.y>=484.36:
                guttersound.play()
                s=0.6
                ballsprite.x-=10
                lock=False
                lock2=True
            if angle == 30 and ballsprite.x>=620.5 and ballsprite.y>=441.9:
                guttersound.play()
                s=0.6
                ballsprite.x-=10
                lock=False
                lock2=True
            if angle==35 and ballsprite.x >=652.9 and ballsprite.y>=421.24:
                guttersound.play()
                s=0.7
                ballsprite.x-=20
                ballsprite.y-=10
                lock=False
                lock2=True
            if angle== 40 and ballsprite.x>= 660.97 and ballsprite.y>= 371:
                guttersound.play()
                s=0.7
                lock=False
                lock2=True
            if angle== -20 and ballsprite.x<= 220.4 and ballsprite.y>= 553.34:
                guttersound.play()
                s=0.6
                lock=False
                lock3=True
            if angle== -25 and ballsprite.x<= 201.79 and ballsprite.y>= 485:
                guttersound.play()
                s=0.6
                lock=False
                lock3=True
            if angle== -30 and ballsprite.x<= 165.5 and ballsprite.y>= 466.16:
                guttersound.play()
                s=0.6
                lock=False
                lock3=True
            if angle== -35 and ballsprite.x<=151 and ballsprite.y>= 415.51:
                guttersound.play()
                s=0.7
                lock=False
                lock3=True
            if angle== -40 and ballsprite.x <= 112 and ballsprite.y>= 403.19:
                guttersound.play()
                s=0.7
                ballsprite.x+=10
                lock=False
                lock3=True
            if lock == True:
                ballsprite.y+=10*math.cos(angler)
                ballsprite.x+=10*math.sin(angler)
                ballsprite.rotation+= 45
                ballsprite.scale=s
                if c%2==0:
                    s-=0.01
        if lock2==True:                                                      #right gutter balls
            
            ballsprite.x-=2
            ballsprite.y+=3
            ballsprite.rotation+= 45
            ballsprite.scale=s
            if c%3==0:
                s-=0.02
        if lock3==True:                                                     #left gutter balls
            
            ballsprite.x+=2
            ballsprite.y+=3
            ballsprite.rotation+= 45
            ballsprite.scale=s
            if c%3==0:
                s-=0.02   
            
        if ballsprite.y >= 555:                                            #after hittig pins 
            abcsprite.visible=True                                          #shutter appears
            if p<1:
                fallsound.play()
                p+=1
            q2=str(m2)
            q1=str(m1)
            q3=str(summed)
            if frame%2==0:
                summed=g1+g2
                if summed> 10:
                    summed=10
                scores[frame].text=q2                                    #displays score in even moves
                m1=0
                m2=0
                if frame>0:
                    sums[(frame-2)//2].text=q3                            #displays sum in each frame
            if frame%2!=0:
                scores[frame].text=q1                                      #displays score in odd moves
                totallabel.text=str(total)                                 #displays total score

            ballsprite.visible = False
            move=False
            angle=0
            if b==False:
                frame+=1
                b=True
        
            if cond==False and abcsprite.y>450:                          #moves shutter down until y=450
                abcsprite.y-=8
               
        if abcsprite.y<= 450:                                            #when shutter falls, fallen ins become invisible
            for j in lis2:
                j.visible= False 
            cond = True
            
        if cond== True and abcsprite.y!=620:                            #moves shutter up again
            abcsprite.y+=8
            
        if abcsprite.y>=620 and ballsprite.visible==False:              #sets ball in place again
            
            
            cond=False
            
            ballsprite.scale=1
            ballsprite.x=400
            ballsprite.y=60
            s=1
            c=0
            p=0
            lock2= False
            lock3=False
            lock=True
            ballsprite.visible=True
            arrowsprite.visible=True
            arrowsprite.rotation=0
            arrange()


                                                      
        
        if len(lis2)==10 and g1!=10:                                  #strike condition
            if t<5:
                strikesound.play()
            if t<20:
                strikelabel.text="STRIKE"
                t+=1
            else:
                strikelabel.text=""
            
        if g1+g2 ==10 and g2!=10:                                  #spare condition
            if t<20:
                sparelabel.text="SPARE"
                t+=1
            else:
                sparelabel.text=""
        
    
pyglet.clock.schedule_interval(update, 1/20.)
    
pyglet.app.run()
