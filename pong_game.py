import turtle as t





win = t.Screen()  # creating a window
win.title("Ping-Pong Game")  # Giving name to the game.
win.bgcolor('black')  # providing color to the HomeScreen
win.setup(width=800, height=500)  # Size of the game panel
win.tracer(0)  # which speeds up the game.



# Creating a left paddle for the game

paddle_left = t.Turtle()
paddle_left.speed(0)
paddle_left.shape('square')
paddle_left.color('white')
paddle_left.shapesize(stretch_wid=5, stretch_len=1)
paddle_left.penup()
paddle_left.goto(-350, 0)

# Creating a right paddle for the game

paddle_right = t.Turtle()
paddle_right.speed(0)
paddle_right.shape('square')
paddle_right.shapesize(stretch_wid=5, stretch_len=1)
paddle_right.color('white')
paddle_right.penup()
paddle_right.goto(350, 0)

# Creating a pong ball for the game
# Setting up the pixels for the ball movement.
ball_dx = 0
ball_dy = 0
ball = t.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('white')
ball.penup()
ball.goto(0, 0)

# Setting up the pixels for the ball movement.
ball_dx = 0.1
ball_dy = 0.1

pen = t.Turtle()
pen.speed(0)
pen.color('White')
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("PONG", align="center", font=('Monaco', 24, "bold"))


##### MAIN GAME LOOP ####

def gameMain(q, lock):
    global ball_dx, ball_dy
    side = "R"
    coords = (250,250)
    cy = 250
    oldleftcrood = 250
    oldrightcrood = 250
    # default values to assign variables to side and wrist coordinates

    while True:
        win.update()

        with lock:
            if not q.empty():
                lst = q.get()
                if lst[0] != None:
                    print(f"coords: {lst[0]} side:{lst[1]}")
                    coords = lst[0]
                    side = lst[1]
                    if coords == 0:
                        cy = 0
                    else:
                        cy = coords[1]


        if side == "L":


            # Moving the left paddle and making it stop at the border
            if paddle_left.ycor() <= -290:
                # when paddle hits bottom
                if abs(cy - oldleftcrood) >= 5:
                    y = paddle_left.ycor()
                    y += 30
                    oldleftcrood = cy
                    paddle_left.sety(y)


            elif paddle_left.ycor() >= 290: # hit top
                if abs(cy - oldleftcrood) <= 5:
                    y = paddle_left.ycor()
                    y -= 30
                    paddle_left.sety(y)
                    oldleftcrood = cy

            else:
                if cy - oldleftcrood >= 10:    # +- 270 is where it hits the top and bottom
                    y = paddle_left.ycor()
                    y -= 30
                    oldleftcrood = cy
                    paddle_left.sety(y)

                elif cy - oldleftcrood <= -10:
                    y = paddle_left.ycor()
                    y += 30
                    paddle_left.sety(y)
                    oldleftcrood = cy

        elif side == "R":

            # Moving the right paddle and making it stop at the border
            if paddle_right.ycor() <= -290: # hit bottom
                if abs(cy - oldrightcrood) >= 5:
                    y = paddle_right.ycor()
                    y += 30
                    oldrightcrood = cy
                    paddle_right.sety(y)


            elif paddle_right.ycor() >= 290: # hit top
                if abs(cy - oldrightcrood) <= 5:
                    y = paddle_right.ycor()
                    y -= 30
                    paddle_right.sety(y)
                    oldrightcrood = cy

            else:
                if cy - oldrightcrood >= 10:    # +- 270 is where it hits the top and bottom
                    y = paddle_right.ycor()
                    y -= 30
                    oldrightcrood = cy
                    paddle_right.sety(y)

                elif cy - oldrightcrood <= -10:
                    y = paddle_right.ycor()
                    y += 30
                    paddle_right.sety(y)
                    oldrightcrood = cy

        elif side in ["L", "R", 0] and (cy == 0 or cy == None):
            # make paddle stay in place if person is out of frame
            ry = paddle_right.ycor()
            paddle_right.sety(ry)

            ly = paddle_left.ycor()
            paddle_left.sety(ly)



        # Moving the ball
        ball.setx(ball.xcor() + ball_dx)
        ball.sety(ball.ycor() + ball_dy)

        # setting up the border

        if ball.ycor() > 290:  # Right top paddle Border
            ball.sety(290)
            ball_dy = ball_dy * -1

        if ball.ycor() < -290:  # Left top paddle Border
            ball.sety(-290)
            ball_dy = ball_dy * -1

        if ball.xcor() > 390:  # right width paddle Border
            ball.goto(0, 0)
            ball_dx = ball_dx * -1


        if (ball.xcor()) < -390:  # Left width paddle Border
            ball.goto(0, 0)
            ball_dx = ball_dx * -1


        # Handling the collisions with paddles.

        if (ball.xcor() > 340) and (ball.xcor() < 350) and (
                ball.ycor() < paddle_right.ycor() + 40 and ball.ycor() > paddle_right.ycor() - 40):
            ball.setx(340)
            ball_dx = ball_dx * -1


        if (ball.xcor() < -340) and (ball.xcor() > -350) and (
                ball.ycor() < paddle_left.ycor() + 40 and ball.ycor() > paddle_left.ycor() - 40):
            ball.setx(-340)
            ball_dx = ball_dx * -1



# if __name__ == "__main__":
#     gameMain()