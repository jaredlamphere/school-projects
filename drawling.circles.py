#import turtle
#declare variables
#horizontal = int()
#radius = int()
#colors = ["red", "blue", "yellow", "green"]
#pen_size = int()
#initializing the location size and colors
#horizontal = -200
#radius = 25
#pen_size = 2

#turtle.penup()
#turtle.goto(horizontal, 0)

#turtle.pensize(5)
#turtle.pendown()
#loop for the circles
#for count in range (0, 4):
    #set colors size and color
   # turtle.fillcolor(colors[count])
  #  turtle.pensize(pen_size)
 #   turtle.begin_fill()
    #drawwwwww
    #turtle.circle(radius)
    #reset location
    #horizontal = horizontal +75
    #radius = radius + 20
    #pen_size = pen_size + 2
    #move turtle
    #turtle.penup()
   # turtle.goto(horizontal, 0)
  #  turtle.pendown()
#    turtle.end_fill()
import random
import turtle
import time

turtle.setup(600, 600)
turtle.write('Ready for more circles?',align='center',font=("Aerial",16,"bold"))
time.sleep(3)
turtle.undo()
#Variables
radius = int()
colors = ["red","blue","yellow","green"]
pen_size = int()
random_index = int()
x=int()
y=int()
#write the loop
for i in range(20):
    x = random.randint(-150,150)
    y = random.randint(-150,150)
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()
    random_index = random.randint(0,3)
    radius = random.randint(25,125)
    pen_size = random.randint(0,10)
    #set random colors size radius
    turtle.fillcolor(colors[random_index])
    turtle.pensize(pen_size)
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()
turtle.mainloop()
#end program