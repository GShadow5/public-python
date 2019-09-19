"""
mental_math.py
Mental math training program utilizing the command line interface
by Nayan Sawyer
started Sep 17 2019
version 1.0.0 Sep 19 2019

                            IMPORTANT INFORMATION
            This program uses two sections of GS_timing.py v0.2.1 by Gabriel Staples to calculate user
        response times. This is not my code and all credit goes to Gabriel Staples. Keep in mind that
        these selections do not represent the full quality of his work as only the sections of code used
        in mental_math.py are retained in the selection below the main program. Please do not use or reference
        his work as seen in my program. If you wish to use or reference a much better time implementation than
        standard python time, please use the original file and article by Gabriel Staples. The full GS_timing.py
        file can be found at https://github.com/ElectricRCAircraftGuy/eRCaGuy_PyTime and the original article
        can be found at https://www.electricrcaircraftguy.com/ go to table of contents, it is listed under
        PYTHON. Needless to say, a huge thank you Gabriel Staples! The timing code would be much less accurate
        without him!

                            MODES
                    All modes utilize integer values only. This includes generated numbers and compatible inputs.
                For this reason and a few others division is not included. This program's sole purpose is intended
                to be practicing and training of high speed thinking and memory.
                    Typing "stop" during normal operation of any mode is the correct way to stop the program. It will
                output final average user response time and jump to the end of the program. Unless "stop" is used
                the program will continue to produce problems indefinitely.

Type                Simply for practicing typing numbers on the numpad (or any keyboard/configuration)
Add                 This mode is for practicing mental addition. Two numbers are presented between
                input Minimum(boundMin) and Maximum(boundMax), and the correct answer is the sum of
                these two numbers.
Subtract            This mode is for practicing mental subtraction. Virtually the same as mode[Add] except for
                practicing subtraction, includes additional optional argument to restrict possible answers to
                positive only.
Multiply            This mode is for practicing multiplication tables. Arguments include number of multiplication
                tables, actual integer value[s] of table base[s], and maximum multiplier. The last being the highest
                number you can be asked to multiply the table base[s] by.


                            TERMS / ACRONYMS
URT                 User response time
AURT                Average user response time


                            VARIABLES
        global
flag                An input variable used to determine which mode to run
        function*
boundMin/boundMax   Boundary values for generating random numbers
n                   Number. Holds random number, for mode[Type] only
a                   Math variable a. Used for display and calculation
b                   Math variable b. Used for display and calculation
t                   Total. This is the user input answer
numBases            Number of multiplication bases. User defined, defaults to 1, for mode[Multiplication] only
bases               Multiplication base(table) list. User defined, for mode[Multiplication] only
fails               ***DEPRECATED*** Used for accuracy calculation in alpha version, potential future feature
        time
cTime               Current time in millis. Used for calculating URT
fTime               Formatted float time. This is the time difference between question and user response
count               Counts loop iterations for calculating average user response time
total               Holds the sum of all response times, used for calculating AURT^

*many variable names are used in all functions, variables unique to only one function are specified( mode[...] only )

                            REFERENCE
*1*     fTime = round(((millis() - cTime) / 1000), 3)
                    set fTime to the value of

                        ...(millis() - cTime)...
                    the time difference in milliseconds between start(cTime) and current(millis()) time

                        ... / 1000)...
                    converted to seconds

                        ...round( ... , 3)...
                    rounded to 3 decimal places

*2*       str("    " + str(c) + " Problems in " + str(int(int(t) / 60)) + ":" + str(int(t) % 60) +
                "\n    Final average response time: " + str(average) + " seconds per problem")

                Final string should appear as: (example)
                    3 Problems in 0:4
                    Final average response time: 1.61 seconds per problem

                    ...str(int(int(t) / 60))...
                to get minutes string remove* any fractions of a second ...int(t)...
                divide by 60 secs/minute, and remove* any remaining seconds ...int(... / 60)...

                    ...str(int(t) % 60)...
                to get string of remaining seconds, remove* any fractions of a second and modulo by 60

                *typecasting a float as an int truncates all information beyond the decimal point


                            ERROR CODES
1                   Error printing. Most likely due to bug in time calculation code. Most likely deprecated
2                   Error with user input in mode[Subtract]. Debugging only, most likely deprecated
3                   Invalid user input for bases. Common error thrown for any non-integer input during multiplication
                    setup. Has no effect on program function and can be ignored. Primarily for debugging
4                   This indicates an error while rounding the AURT to 3 decimal places. Typically result of all
                    time variables being zero



"""

import random
# For borrowed time code. See important info
import ctypes, os


# Generate time string. For compressing code. f = fTime, c = count, t = total
def resTime(f, c, t, stop = 0):
    """
    "\n    " + str(int(((c - int(stop - 1)) / c) * 100)) + "% Input accuracy" ***DEPRECATED***
    """
    try:
        if stop >= 1:
            # Generate float value of average time to nearest hundredth of a second
            average = round(t / c, 2)
            # Generate final string. See ref 2
            return str("    " + str(c) + " Problems in " + str(int(int(t) / 60)) + ":" + secString(t) +
                "\n    Final average response time: " + str(average) + " seconds per problem")
        else:
            average = round(t / c, 2)
            return str("Time passed: " + str(f) + "  Average response time = " + str(average))
    except:
        return str("Stopped before first submission. Error code 4")


def secString(time):
    if (int(time) % 60) < 10:
        return "0" + str(int(time) % 60)
    else:
        return str(int(time) % 60)


def getMin():
    while True:
        try:
            val = int(input("Minimum: "))
            break
        except:
            print("Invalid input")
    return val


def getMax(mIn):
    while True:
        try:
            val = int(input("Maximum: "))
            while val < mIn:
                print("Maximum cannot be less than minimum")
                val = int(input("Maximum: "))
            break
        except:
            print("Invalid input")
    return val


def isnumber(string):
    try:
        if string.isnumeric():
            return True
        elif string[1].isnumeric():
            return True
        else:
            return False
    except:
        if string[1].isnumeric():
            return True
        else:
            return False


def modeType():
    '''MODE[Type]'''
    # Initialize mode variables
    boundMin = getMin()
    boundMax = getMax(boundMin)
    count = 0
    total = 0
    fTime = 0
    fails = 0
    while True:
        # Generate random numbers
        n = random.randint(int(boundMin), int(boundMax))

        # Get current time in millis
        cTime = millis()
        while True:
            # Try. Prints error instead of crashing if printing error occurs. Most likely deprecated
            try:
                # Get user input. For checking math
                t = input("Number (" + str(n) + "): ")
                # If input is "stop" end the program
                if t.lower() == "stop":
                    return resTime(fTime, count, total, fails + 1)
                # Check if input is numeric
                elif isnumber(t):
                    # Check that input is same as number, if so break (while True)
                    if int(t) == int(n):
                        break
                    else:
                        print("Incorrect!")
                        fails += 1
                else:
                    print("Incorrect!")
                    fails += 1
            except:
                print("Invalid input. Error code 1")
                fails += 1

        # Calculate formatted float time (time difference). ref 1
        fTime = round(((millis() - cTime) / 1000), 3)

        # Update total response times. Count number of times loop has run. For calculating AURT
        total += fTime
        count += 1

        # Print answer "Correct" and response time. The function will only get here given a correct answer, otherwise
        print("Correct! " + resTime(fTime, count, total))  # it will loop forever (while True) or stop




'''MODE[Add]'''
def modeAdd():
    # Initialize mode variables
    boundMin = getMin()
    boundMax = getMax(boundMin)
    count = 0
    total = 0
    fTime = 0
    fails = 0
    while True:
        # Generate random numbers
        a = random.randint(int(boundMin), int(boundMax))
        b = random.randint(int(boundMin), int(boundMax))

        # Get current time in millis
        cTime = millis()

        # Keep asking for same number if incorrect
        while True:
            # Try so you don't crash you mother fucking piece of shit!
            try:
                # Get user input for checking math
                t = input("Sum (" + str(a) + " + " + str(b) + "): ")
                # Check for program stop
                if t == "stop":
                    return resTime(fTime, count, total, fails + 1)
                elif isnumber(t):
                    # Check that input is same as sum, if so break (while True)
                    if int(t) == int(a) + int(b):
                        break
                    else:
                        print("Incorrect!")
                        fails += 1
                else:
                    print("Incorrect!")
                    fails += 1
            except:
                print("Invalid input. Error code 1")
                fails += 1

        # Calculate formatted float time (time difference). ref 1
        fTime = round(((millis() - cTime) / 1000), 3)
        total += fTime
        count += 1
        # Print answer "Correct" and response time. The function will only get here given a correct answer, otherwise
        print("Correct! " + resTime(fTime, count, total))  # it will loop forever (while True) or stop




'''MODE[Subtraction]'''
def modeSubtract():
    # Initialize mode variables
    boundMin = getMin()
    boundMax = getMax(boundMin)
    count = 0
    total = 0
    fTime = 0
    fails = 0

    # Additional argument. Given all problems are subtraction does user want to allow negative answers?
    negativeA = input("Allow possibility of negative answers? (y/n): ")

    # Check that input is valid
    while negativeA.lower() != "y" and negativeA.lower() != "n":
        negativeA = input("Allow possibility of negative answers? (y/n): ")

    # If negative answers are undesired make sure the value being subtracted FROM is no lower than 1
    if negativeA.lower() == "n":
        if boundMin <= 1:
            boundMin = 1

    while True:
        # Generate random numbers
        if negativeA.lower() == "y":
            a = random.randint(int(boundMin), int(boundMax))
            b = random.randint(int(boundMin), int(boundMax))
        elif negativeA.lower() == "n":
            # When no negatives make sure the subtracted value is lower than the initial value
            a = random.randint(int(boundMin), int(boundMax))
            b = random.randint(int(boundMin), int(a))
        else:  # for debugging
            print("Negative answer input invalid, or bug.  Returned error code: 2")

        # Get current time in millis
        cTime = millis()

        while True:
            # Try. Prints error instead of crashing if printing error occurs. Most likely deprecated
            try:
                # Get user input. For checking math
                t = input("Sum (" + str(a) + " - " + str(b) + "): ")
                # End if stop
                if t == "stop":
                    return resTime(fTime, count, total, fails + 1)
                elif isnumber(t):
                    # Check that input is same as sum, if so break while True
                    if int(t) == int(a) - int(b):
                        break
                    else:
                        print("Incorrect!")
                        fails += 1
                else:
                    print("Incorrect!")
                    fails += 1
            except:
                print("Invalid input. Error code 1")
                fails += 1

        # Calculate formatted float time (time difference). ref 1
        fTime = round(((millis() - cTime) / 1000), 3)

        # Update total response times. Count number of times loop has run. For calculating AURT
        total += fTime
        count += 1

        # Print answer "Correct" and response time. The function will only get here given a correct answer, otherwise
        print("Correct! " + resTime(fTime, count, total))  # it will loop forever (while True) or stop


'''MODE[Multiply]'''
def modeMultiply():
    # Initialize mode variables
    numBases = 0
    while numBases <= 0:
        try:
            # Get number of bases(times tables) desired
            numBases = int(input("Number of tables "
                                 "(ex: Doing the 6 and 8 tables together would require 2. default 1):"))
            break
        except:
            # If invalid input (non-int) default to one base
            numBases = 1

    # Initialize list of bases
    bases = []
    # Fill list with [numBases] of actual base values via user input
    for i in range(numBases):
        while True:
            try:
                bases.append(int(input("Base[" + str(i + 1) + "]: ")))
                break
            except:
                print("Invalid input. Must be integer. Returned error code: 3")

    boundMax = 0
    while True:
        try:
            # Get number of bases desired
            boundMax = int(input("Maximum multiplier: "))
            break
        except:
            print("Invalid input")

    count = 0
    total = 0
    fTime = 0
    fails = 0

    # Main function
    while True:
        # Generate Random numbers
        a = random.choice(bases)
        b = random.randint(0, int(boundMax))

        # Get current time in millis
        cTime = millis()

        while True:
            # Try. Prints error instead of crashing if printing error occurs. Most likely deprecated
            try:
                # Get user input. For checking math
                t = input("Product (" + str(a) + " x " + str(b) + "): ")
                # End if stop
                if t == "stop":
                    return resTime(fTime, count, total, fails + 1)
                elif isnumber(t):
                    # Check that input is same as sum, if so break while True
                    if int(t) == int(a) * int(b):
                        break
                    else:
                        print("Incorrect!")
                        fails += 1
                else:
                    print("Incorrect!")
                    fails += 1
            except:
                print("Invalid input. Error code 1")
                fails += 1

        # Calculate formatted float time (time difference). ref 1
        fTime = round(((millis() - cTime) / 1000), 3)

        # Update total response times. Count number of times loop has run. For calculating AURT
        total += fTime
        count += 1

        # Print answer "Correct" and response time. The function will only get here given a correct answer, otherwise
        print("Correct! " + resTime(fTime, count, total))  # it will loop forever (while True) or stop


"""
THE FOLLOWING CODE IS TWO TIME CALCULATION FUNCTIONS BORROWED FROM Gabriel Staples 
PLEASE SEE IMPORTANT INFO IN DOCSTRING
"""

"""
START OF BORROWED CODE
"""

#-------------------------------------------------------------------
#MODULE FUNCTIONS:
#-------------------------------------------------------------------
#OS-specific low-level timing functions:
if (os.name=='nt'): #for Windows:

    def millis():
        "return a timestamp in milliseconds (ms)"
        tics = ctypes.c_int64() #use *signed* 64-bit variables; see the "QuadPart" variable here: https://msdn.microsoft.com/en-us/library/windows/desktop/aa383713(v=vs.85).aspx
        freq = ctypes.c_int64()

        #get ticks on the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
        #get the actual freq. of the internal ~2MHz QPC clock
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))

        t_ms = tics.value*1e3/freq.value
        return t_ms

elif (os.name=='posix'): #for Linux:

    #Constants:
    CLOCK_MONOTONIC_RAW = 4 # see <linux/time.h> here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h

    #prepare ctype timespec structure of {long, long}
    #-NB: use c_long (generally signed 32-bit) variables within the timespec C struct, per the definition here: https://github.com/torvalds/linux/blob/master/include/uapi/linux/time.h
    class timespec(ctypes.Structure):
        _fields_ = \
            [
                ('tv_sec', ctypes.c_long),
                ('tv_nsec', ctypes.c_long)
            ]

    #Configure Python access to the clock_gettime C library, via ctypes:
    #Documentation:
    #-ctypes.CDLL: https://docs.python.org/3.2/library/ctypes.html
    #-librt.so.1 with clock_gettime: https://docs.oracle.com/cd/E36784_01/html/E36873/librt-3lib.html #-
    #-Linux clock_gettime(): http://linux.die.net/man/3/clock_gettime
    librt = ctypes.CDLL('librt.so.1', use_errno=True)
    clock_gettime = librt.clock_gettime
    #specify input arguments and types to the C clock_gettime() function
    # (int clock_ID, timespec* t)
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]

    def monotonic_time():
        "return a timestamp in seconds (sec)"
        t = timespec()
        #(Note that clock_gettime() returns 0 for success, or -1 for failure, in
        # which case errno is set appropriately)
        #-see here: http://linux.die.net/man/3/clock_gettime
        if clock_gettime(CLOCK_MONOTONIC_RAW , ctypes.pointer(t)) != 0:
            #if clock_gettime() returns an error
            errno_ = ctypes.get_errno()
            raise OSError(errno_, os.strerror(errno_))
        return t.tv_sec + t.tv_nsec*1e-9 #sec

    def millis():
        "return a timestamp in milliseconds (ms)"
        return monotonic_time()*1e3 #ms

"""
END OF BORROWED CODE
"""

#
#
#
'''
        PROGRAM START
'''
#
#
#

# User input to determine mode
flag = input('Select mode: Type[1], Add[2], Subtract[3] or Multiply[4], or "help" for help ')

if flag == "1":
    print(modeType())
elif flag == "2":
    print(modeAdd())
elif flag == "3":
    print(modeSubtract())
elif flag == "4":
    print(modeMultiply())
elif flag.lower() == "help":
    print(__doc__)
else:
    print("Invalid mode input")

