"""
@author: Mujibul Islam Dipto
This program provides a GUI to analyze a given password to determine its strength.
"""


import sys
from termcolor import colored
import re
import tkinter as tk

# Check usage
if len(sys.argv) > 2:
    sys.exit("Usage (GUI): python3 password_analyzer.py\nUsage(cmd line): python3 password_analyzer.py YOUR_PASSWORD")



#  sentences to print
STRENGTHS = {0: 'weak', 1: 'weak', 2: 'medium', 3: 'medium', 4: 'strong'}
# colors for corresponding the strength
COLORS = {'weak': 'red', 'medium': 'yellow', 'strong': 'green'}
# reasons
REASONS = {'len': "Password should be greater than 8 characters.", 'capital': "Password should contain a mixture of upper and lower case characters.",
           'num': "Password should contain at least one number.", 'special': "Password should contain at least one special character.", }

"""
Checks if a password is:
1) Above a certain length
2) Contains at least one upper and lower case
3) Contains at least one special character
4) Contains at least one number
@param pw: password to analyze
@param env: Selects environment: Command line or GUI (tkinter)
"""

def analyze_password(pw, env):
    count = 0 # keep track of strength
    problems = [] # store issues with password
    # check length
    if (len(pw)) < 8:
        problems.append(REASONS['len'])
    else:
        count += 1

    # check for upper and lower case
    if not (any(c.isupper() for c in pw) and any(c.islower() for c in pw)):
        problems.append(REASONS['capital'])
    else:
        count += 1

    # check for special character
    special_c = re.findall("[^a-zA-Z, 0-9]", pw)
    if len(special_c) == 0:
        problems.append(REASONS['special'])
    else:
        count += 1

    # check for numbers
    digits = re.findall("[0-9]", pw)
    if len(digits) == 0:
        problems.append(REASONS['num'])
    else:
        count += 1

    # print analysis (for command line)
    if env == "cmd":
        strength = STRENGTHS[count]
        print(colored("Your password strength is: %s",
                COLORS[strength]) % strength)

        if(len(problems) > 0):
            print("\nHere are some suggestions:")
            for problem in problems:
                print(problem)
            return

    # create output for GUI
    outputs = []
    # password strength
    out = ""
    strength = STRENGTHS[count]
    out += "Your password strength is: "
    outputs.append(strength)

    # suggestions
    if strength != "strong":
        out = ""
        out += "\n\n"
        if len(problems) > 0:
            for problem in problems:
                out +=  problem + "\n"
        outputs.append(out)
    
    # remove given password
    pw = None
    return outputs

# if script was ran for GUI mode
if len(sys.argv) == 1:
    # setup root
    root = tk.Tk()
    root.title("Password Analyzer")
    root.geometry("500x500")

    # text input to get password
    entry = tk.Entry(root)
    # hide characters on screen
    entry.config(show= "*" )
    entry.place(relx=.5, rely=.3, anchor="c")

    # displays the result on the GUI
    def show_result(event=None):
        # create canvas to display suggestions
        canvas = tk.Canvas(root, width=460, height=300)
        canvas.place(relx=.5, rely=.7, anchor="c")

        pw = entry.get()
        # check for empty string
        if len(pw) == 0:
            return

        results = analyze_password(pw, "GUI")
        
        # display strength
        txt = "Your password strength is: "
        strength = results[0]
        txt += strength
        txt += ".\n"
        color = COLORS[strength]
        label_strength = tk.Label(root, text = txt)
        label_strength.config(fg = color)
        label_strength.place(relx=.5, rely=.5, anchor="c")
        # display suggestions
        if len(results) > 1:
            suggestions = results[1:]
            out = ""
            for suggestion in suggestions:
                out += suggestion + "\n"
            label_suggest = tk.Label(canvas, text = out)
            label_suggest.config(fg = color)
            label_suggest.config(fg="snow")
            label_suggest.place(relx=.5, rely=.5, anchor="c")
        canvas.delete("all")

    # ensure app works with keyboard (return key)
    root.bind('<Return>', show_result)
    
    button = tk.Button(text='Enter your password', command = show_result)
    button.place(relx=.5, rely=.37, anchor="c")

    root.mainloop()

else:
    analyze_password(sys.argv[1], "cmd")
