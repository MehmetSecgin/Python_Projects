# Python Program to find Area and Circumference of circle using Radius
def circle():
    R = input("Enter a number: ")
    try:
        R = int(R)
        if R < 0:
            print("You cant use negative values")
            exit(1)
    except ValueError:
        try:
            R = float(R)
            if R < 0:
                print("You cant use negative values")
                exit(1)
        except ValueError:
            print("The input is not a number.")
            exit(1)
    PI = 3.14
    S = PI * R * R
    C = 2 * PI * R
    print("Area Of a Circle = {:.2f}".format(S))
    print("Circumference Of a Circle = {:.2f}".format(C))


circle()
