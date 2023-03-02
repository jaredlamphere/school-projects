import turtle
#determin variables
pen_color = str()
fill_color = str()
pen_size = int()

# #moving the pen
# turtle.penup()
# turtle.goto(0, 150)
# turtle.pendown()
# pen_color = input("please input blue red yellow  ")
# pen_size = int(input("input size 1-10  "))
# if pen_color == "red":
#     fill_color = "yellow"
# if pen_color == "blue":
#     fill_color = "red"
# if pen_color == "yellow":
#     fill_color = "green"
# turtle.pensize(pen_size)
# turtle.pencolor(pen_color)
# turtle.fillcolor(fill_color)

# #draw circle
# turtle.begin_fill()
# turtle.circle(50)
# turtle.end_fill()
# #moving pen
# turtle.penup()
# turtle.right(90)
# turtle.forward(150)
# turtle.pendown()
# #input for square

# pen_color = input("please input blue red yellow  ")
# pen_size = int(input("input size 1-10  "))
# if pen_color == "red":
#     fill_color = "yellow"
# if pen_color == "blue":
#     fill_color = "red"
# if pen_color == "yellow":
#     fill_color = "green"
# turtle.pensize(pen_size)
# turtle.pencolor(pen_color)
# turtle.fillcolor(fill_color)
# #square draw
# turtle.begin_fill()
# turtle.right(90)
# turtle.forward(50)
# turtle.left(90)
# turtle.forward(100)
# turtle.left(90)
# turtle.forward(100)
# turtle.left(90)
# turtle.forward(100)
# turtle.left(90)
# turtle.forward(50)
# turtle.end_fill()

# #moving pen
# turtle.penup()
# turtle.left(90)
# turtle.forward(150)
# turtle.pendown

# #input for triangle
# pen_color = input("please input blue red yellow  ")
# pen_size = int(input("input size 1-10  "))
# if pen_color == "red":
#     fill_color = "yellow"
# if pen_color == "blue":
#     fill_color = "red"
# if pen_color == "yellow":
#     fill_color = "green"
# turtle.pensize(pen_size)
# turtle.pencolor(pen_color)
# turtle.fillcolor(fill_color)
# turtle.begin_fill()
# turtle.right(35)
# turtle.forward(125)
# turtle.right(235)
# turtle.forward(150)
# turtle.left(127)
# turtle.forward(130)
# turtle.end_fill()

import time
time.sleep(3)
turtle.reset()
turtle.setup(600,600)

#additional variables
turtle_shape=str()
turtle_location=str()
turtle.pencolor("red")
turtle.fillcolor("purple")
#inputs
turtle_location = input("please input top left, top right, bottom right, bottom left  ")
turtle_shape = input("pick square, circle, triangle  ")

if turtle_location == "top left":
    turtle.pensize(3) 
elif turtle_location == "top right":
    turtle.pensize(5)
elif turtle_location == "bottom left":
    turtle.pensize(7)
else:
    turtle.pensize(9)

if turtle_location == "top left":
    turtle.penup()
    turtle.goto(-200,200)
    turtle.pendown()
elif turtle_location == "top right":
    turtle.penup()
    turtle.goto(200, 200)
    turtle.pendown()
elif turtle_location == "bottom left":
    turtle.penup()
    turtle.goto(-200, 200)
    turtle.pendown()
else: 
    turtle.penup()
    turtle.goto(150, -150)
    turtle.pendown()

if turtle_shape == "square":
    turtle.begin_fill()
    turtle.right(90)
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(100)
    turtle.left(90)
    turtle.forward(50)
    turtle.end_fill()
elif turtle_shape == "triangle":
    turtle.begin_fill()
    turtle.right(35)
    turtle.forward(125)
    turtle.right(235)
    turtle.forward(150)
    turtle.left(127)
    turtle.forward(130)
    turtle.end_fill()
else:
    turtle.begin_fill()
    turtle.circle(50)
    turtle.end_fill()