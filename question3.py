import turtle

def draw_pattern(t, length, depth):
    # Base Case: Stop the recursion when depth is 0.
    if depth == 0:
        t.forward(length)
    # Recursive Step: Apply the pattern rules.
    else:
        # 1. Divide the edge into three equal segments
        #    Draw the first segment.
        draw_pattern(t, length / 3, depth - 1)
        
        # 2. Turn to start the inward-pointing triangle.
        #    This is the correction: We turn left.
        t.left(60)
        draw_pattern(t, length / 3, depth - 1)

        # 3. Turn to complete the triangle.
        #    This is the correction: We turn right.
        t.right(120)
        draw_pattern(t, length / 3, depth - 1)
        
        # 4. Turn to align for the last segment.
        #    This is the correction: We turn left.
        t.left(60)
        draw_pattern(t, length / 3, depth - 1)

def main():
    # Set up the drawing screen and turtle.
    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0) # Sets the fastest drawing speed.

    # Prompt the user for input parameters.
    try:
        num_sides = int(input("Enter the number of sides: "))
        side_length = int(input("Enter the side length: "))
        recursion_depth = int(input("Enter the recursion depth: "))
    except ValueError:
        print("Invalid input. Please enter integers for sides, length, and depth.")
        return
    
    t.hideturtle()
    
    # Position the turtle for a centered drawing.
    t.up()
    t.goto(-side_length / 2, side_length / 3)
    t.down()
    
    # Draw the initial polygon by calling the recursive function for each side.
    angle = 360 / num_sides
    for _ in range(num_sides):
        draw_pattern(t, side_length, recursion_depth)
        t.left(angle)

    screen.exitonclick()

if __name__ == "__main__":
    main()