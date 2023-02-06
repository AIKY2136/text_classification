import random
import turtle

def random_drawing():
    t = turtle.Turtle()
    t.speed(0)
    t.pensize(2)
    for i in range(100):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        t.pencolor((r, g, b))
        size = random.randint(10, 100)
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        t.penup()
        t.goto(x, y)
        t.pendown()
        for j in range(4):
            t.forward(size)
            t.right(90)

random_drawing()
turtle.done()
