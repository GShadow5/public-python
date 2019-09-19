"""
conversions.py
A command line temperature conversion calculator
by Nayan Sawyer
started Feb 2019
version 0.1.0 Sep 19 2019

            This was a small personal project to make chem class more interesting.
            I never got around to updating or documenting it, but it's pretty straight forward.

"""

def runTemp():
    inType = input("Input unit(F,C,K): ")
    while inType == "":
        inType = input("Input unit(F,C,K): ")
    outType = input("Output unit(F,C,K): ")
    while outType == "":
        outType = input("Output unit(F,C,K): ")
    inTemp = float(input("Temperature: "))


    if inType == "F" or inType == "f":
        if outType == "K" or outType == "k":
            print("F: " + str(inTemp) + ", K: " + str(((5/9) * (inTemp-32)) + 273.15))
        elif outType == "C" or outType == "c":
            print("F: " + str(inTemp) + ", C: " + str((5/9) * (inTemp-32)))
        else:
            print("invalid output unit")

    elif inType == "C"or inType == "c":
        if outType == "F" or outType == "f":
            print("C: " + str(inTemp) + ", F: " + str(((9/5) * inTemp) + 32))
        elif outType == "K" or outType == "k":
            print("C: " + str(inTemp) + ", K: " + str(inTemp + 273.15))
        else:
            print("invalid output unit")

    elif inType == "K" or inType == "k":
        if outType == "F" or outType == "f":
            print("K: " + str(inTemp) + ", F: " + str(((9/5) * (inTemp - 273.15)) + 32))
        elif outType == "C" or outType == "c":
            print("K: " + str(inTemp) +", C: " + str(inTemp - 273.15))
        else:
            print("invalid output unit")

    else:
        print("invalid input unit")


'''
        PROGRAM START
'''
while True:
    runTemp()
    print("")
