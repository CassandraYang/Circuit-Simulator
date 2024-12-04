"""
15-110 Hw6 - Circuit Simulator Project
Name:
AndrewID:
"""

import hw6_circuit_tests as test

project = "Circuit"

#### CHECK-IN 1 ####

'''
findMatchingParen(expr, index)
#1 [Check6-1]
Parameters: str ; int
Returns: int
'''
def findMatchingParen(expr, index):
    openParen = 1
    while openParen != 0:
        index += 1
        if expr[index] == '(':
            openParen += 1
        elif expr[index] == ')':
            openParen -= 1
    return index


'''
getTokenBounds(expr, start)
#2 [Check6-1]
Parameters: str ; int
Returns: list of ints
'''
def getTokenBounds(expr, start):
    begin = None
    end = None
    while end == None:
        if begin == None and expr[start] != ' ':
            begin = start
        elif begin != None and (start == len(expr) or expr[start] == ' '):
            end = start - 1
        start += 1
    return [begin, end]


'''
parseExpr(expr)
#3 [Check6-1]
Parameters: str
Returns: tree of strs
'''
def parseExpr(expr):
    expr = expr.strip()
    if expr[0] == '(' and findMatchingParen(expr, 0) == len(expr) -1:
        return parseExpr(expr[1: -1])
    elif ' ' not in expr:
        return {"contents": expr, "children": []}
    elif expr[0:3] == 'NOT':
        value = parseExpr(expr[3:])
        return {"contents": expr[0:3], "children": [value]}
    else:
        if expr[0] == '(':
            closeParen = findMatchingParen(expr, 1)
            leftValue = expr[: closeParen + 1]
            rightStart, rightEnd = getTokenBounds(expr, closeParen + 1)
        else:
            tokenStart, tokenEnd = getTokenBounds(expr, 0)
            leftValue = expr[tokenStart: tokenEnd + 1]
            rightStart, rightEnd = getTokenBounds(expr, tokenEnd + 1)
        token = expr[rightStart: rightEnd + 1]
        leftTree = parseExpr(leftValue)
        rightTree = parseExpr(expr[rightEnd + 1:])
        return {"contents": token, "children": [leftTree, rightTree]}


'''
validateTree(t)
#4 [Check6-1]
Parameters: tree of strs
Returns: bool
'''
def validateTree(t):
    if t == {}:
        return False
    if t["contents"] == 'NOT':
        if len(t["children"]) != 1:
            return False
    elif t["contents"] == 'AND':
        if len(t["children"]) != 2:
            return False
    elif t["contents"] == 'OR':
        if len(t["children"]) != 2:
            return False
    elif t["contents"] == 'XOR':
        if len(t["children"]) != 2:
            return False
    else:
        if len(t["children"]) != 0:
            return False
    return True


'''
runWeek1()
#5 [Check6-1]
Parameters: no parameters
Returns: None
'''
def runWeek1():
    print('Enter a Boolean Expression: ')
    x = input()
    tree = parseExpr(x)
    if validateTree(tree):
        print(tree)
    else:
        print('Tree is invalid. Try again')
    return None

#### CHECK-IN 2 ####

'''
getLeaves(t)
#1 [Check6-2]
Parameters: tree of strs
Returns: list of strs
'''
def getLeaves(t):
    if t['children'] == []:
        return [t['contents']]
    else:
        result = []
        leaves = []
        for child in t['children']:
            result += getLeaves(child)
        for leaf in result:
            if leaf not in leaves:
                leaves.append(leaf)
    return sorted(leaves)


'''
generateAllInputs(n)
#2 [Check6-2]
Parameters: int
Returns: 2D list of bools
'''
def generateAllInputs(n):
    if n == 0:
        return [[]]
    else:
        results = generateAllInputs(n - 1)
        list = []
        for result in results:
            list.append(result + [True])
            list.append(result + [False])
    return list


'''
evalTree(t, inputs)
#3 [Check6-2] & #4 [Hw6]
Parameters: tree of strs ; dict mapping strs to bools
Returns: bool
'''
def evalTree(t, inputs):
    if t['children'] == []:
        t['powered'] = inputs[t['contents']]
        return inputs[t['contents']]
    else:
        if t['contents'] == 'NOT':
            t['powered'] = not evalTree(t['children'][0], inputs)
            return not evalTree(t['children'][0], inputs)
        elif t['contents'] == 'AND':
            left = evalTree(t['children'][0], inputs)
            right = evalTree(t['children'][1], inputs)
            t['powered'] = left and right
            return left and right
        elif t['contents'] == 'OR':
            left = evalTree(t['children'][0], inputs)
            right = evalTree(t['children'][1], inputs)
            t['powered'] = left or right
            return left or right
        elif t['contents'] == 'XOR':
            left = evalTree(t['children'][0], inputs)
            right = evalTree(t['children'][1], inputs)
            t['powered'] = left ^ right
            return left ^ right


'''
makeTruthTable(tree)
#4 [Check6-2]
Parameters: tree of strs
Returns: None
'''
def makeTruthTable(tree):
    leaves = getLeaves(tree)
    rows = generateAllInputs(len(leaves))
    table = leaves + ['Out']
    print(table)
    for row in rows:
        inputs = {}
        for i in range(len(leaves)):
            inputs[leaves[i]] = row[i]
        ouput = evalTree(tree, inputs)
        print(row + [ouput])
    return None


'''
runWeek2()
#5 [Check6-2]
Parameters: no parameters
Returns: None
'''
def runWeek2():
    print('Enter a Boolean Expression: ')
    x = input()
    tree = parseExpr(x)
    if validateTree(tree):
        makeTruthTable(tree)
    else:
        print('Tree is invalid. Try again')
    return None


### WEEK 3 ###

'''
makeModel(data)
#2 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data['expression'] = ''
    data['tree'] = None
    data['inputs'] = []
    return


'''
makeView(data, canvas)
#2 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def makeView(data, canvas):
    canvas.create_text(325, 625, text = f"Expression: {data['expression']}")
    if data['tree'] != None:
        drawCircuit(data, canvas)
    return


'''
keyPressed(data, event)
#2 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == 'BackSpace' and data['expression'] != '':
        data['expression'] = data['expression'][:-1]
    elif event.keysym == 'Return':
        data['tree'] = parseExpr(data['expression'])
        data['expression'] = ''
        runInitialCircuit(data)
    elif event.keysym == 'space':
        data['expression'] += ' '
    elif event.keysym in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        data['expression'] += event.keysym
    elif event.keysym == 'Tab':
        makeTruthTable(data['tree'])
    elif event.keysym == 'parenleft':
        data['expression'] += '('
    elif event.keysym == 'parenright':
        data['expression'] += ')'
    return


'''
mousePressed(data, event)
#4 [Hw6]
Parameters: dict mapping strs to values ; mouse event object
Returns: None
'''
def mousePressed(data, event):
    for input in data['inputLocations']:
        if (data['inputLocations'][input]['left'] <= event.x <=
           data['inputLocations'][input]['right'] and
           data['inputLocations'][input]['top'] <= event.y <=
           data['inputLocations'][input]['bottom']):
            data['inputs'][input] = not data['inputs'][input]
    data['output'] = evalTree(data['tree'], data['inputs'])
    return



'''
runInitialCircuit(data)
#2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def runInitialCircuit(data):
    inputList = getLeaves(data['tree'])
    input = {}
    for leaf in inputList:
        input[leaf] = False
    data['inputs'] = input
    data['output'] = evalTree(data['tree'], data['inputs'])
    return


'''
drawNode(canvas, value, x, y, size, lit)
#3 [Hw6]
Parameters: Tkinter canvas ; str ; int ; int ; int ; bool
Returns: None
'''
def drawNode(canvas, value, x, y, size, lit):
    if lit == True:
        color = 'yellow'
    else:
        color = None
    canvas.create_rectangle(x - size//2, y - size//2, x + size//2, y + size//2, fill = color)
    canvas.create_text(x, y, text = value)
    return


'''
drawWire(canvas, x1, y1, x2, y2, lit)
#3 [Hw6]
Parameters: Tkinter canvas ; int ; int ; int ; int ; bool
Returns: None
'''
def drawWire(canvas, x1, y1, x2, y2, lit):
    if lit:
        color = 'yellow'
    else:
        color = 'black'
    canvas.create_line(x1, y1, x2, y2, fill = color)
    return

#### WEEK 3 PROVIDED CODE ####

''' getTreeDepth() finds the depth of the tree, the max length from root to leaf '''
def getTreeDepth(t):
    if len(t["children"]) == 0:
        return 0
    max = 0
    for child in t["children"]:
        tmp = getTreeDepth(child)
        if tmp > max:
            max = tmp
    return max + 1

''' getTreeWidth() finds the width of the tree, the max number of nodes on the same level '''
def getTreeWidth(t):
    if len(t["children"]) == 0:
        return 0
    elif len(t["children"]) == 1:
        return max(1, getTreeWidth(t["children"][0]))
    else:
        biggestChildSize = max(getTreeWidth(t["children"][0]),
                               getTreeWidth(t["children"][1]))
        return max(1, 2 * biggestChildSize)

''' This function draws all the inputs of the circuit. They should all go on
    the left side of the screen. '''
def drawInputs(data, canvas, size):
    ''' We'll track the locations of inputs for button-pressing later on '''
    if "inputLocations" not in data:
        data["inputLocations"] = { }
    keys = list(data["inputs"].keys())
    keys.sort()

    # make the inputs centered on the Y axis
    margin = (600 - (len(keys) * size)) / 2
    centerX = size/2
    for i in range(len(keys)):
        var = keys[i]
        if var not in data["inputLocations"]:
            data["inputLocations"][var] = { }
        inp = data["inputLocations"][var]
        centerY = size * i + size/2 + margin
        # Store the location so we can use it to click buttons later on
        inp["left"] = centerX - size/2
        inp["top"] = centerY - size/2
        inp["right"] = centerX + size/2
        inp["bottom"] = centerY + size/2
        drawNode(canvas, var, centerX, centerY, size/2, data["inputs"][var])

''' This function draws a circuit tree within the specified bounding box.
    It returns the location where the node was drawn, to make drawing wires easier. '''
def drawTree(data, canvas, t, size, left, top, right, bottom):
    if "powered" not in t:
        t["powered"] = False
    centerX = (left + right) / 2
    centerY = (top + bottom) / 2
    # Don't draw the leaves- they're all on the left side of the screen!
    if len(t["children"]) == 0:
        var = t["contents"]
        d = data["inputLocations"][var]
        # Instead, return the location of the leaf, to make drawing wires easier.
        return [ (d["left"] + d["right"]) / 2 + size/4,
                 (d["top"] + d["bottom"]) / 2, data["inputs"][var] ]
    elif len(t["children"]) == 1:
        drawNode(canvas, t["contents"], centerX, centerY, size/2, t["powered"])
        # Position the child at the same Y position, but to the left
        [childX, childY, childOn] = drawTree(data, canvas, t["children"][0], size,
                left - size, top, right - size, bottom)
        drawWire(canvas, childX, childY, centerX - size/4, centerY, childOn)
        return [ centerX + size/4, centerY, t["powered"] ]
    else:
        drawNode(canvas, t["contents"], centerX, centerY, size/2, t["powered"])
        # Split the Y dimension in half, and give each to one child.
        # Left child
        [childX, childY, childOn] = drawTree(data, canvas, t["children"][0], size,
                left - size, top, right - size, centerY)
        drawWire(canvas, childX, childY, centerX - size/4, centerY, childOn)
        # Right child
        [childX, childY, childOn] = drawTree(data, canvas, t["children"][1], size,
                left - size, centerY, right - size, bottom)
        drawWire(canvas, childX, childY, centerX - size/4, centerY, childOn)
        return [ centerX + size/4, centerY, t["powered"] ]

''' This function draws the entire circuit. It first determines the size of each
    circuit node by measuring the width/height of the tree. Then it draws the
    inputs and outputs. Then it recursively draws the circuit tree. '''
def drawCircuit(data, canvas):
    t = data["tree"]
    if "output" not in data:
        data["output"] = False
    depth = 2 + getTreeDepth(t)
    width = max(1, len(data["inputs"]), getTreeWidth(t))
    size = 600 / max(depth, width)

    drawInputs(data, canvas, size)

    outLeft, outRight = 600 - size, 600
    outTop, outBottom = 0, 600
    outX, outY = (outLeft + outRight)/2, (outTop + outBottom)/2
    drawNode(canvas, "Out", outX, outY, size/2, data["output"])

    [childX, childY, childOn] = drawTree(data, canvas, t, size,
        outLeft - size, outTop, outRight - size, outBottom)
    drawWire(canvas, childX, childY, outLeft + size/4, outY, childOn)

#### SIMULATION STARTER CODE ###

from tkinter import *

def keyEventHandler(data, canvas, event):
    if event.keysym == "Return":
        # Clear previous data, if it exists
        if "inputLocations" in data:
            del data["inputLocations"]
    keyPressed(data, event)

    canvas.delete(ALL)
    makeView(data, canvas)
    canvas.update()

def mouseEventHandler(data, canvas, event):
    mousePressed(data, event)

    canvas.delete(ALL)
    makeView(data, canvas)
    canvas.update()

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    canvas = Canvas(root, width=w, height=h)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    makeView(data, canvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, canvas, event))
    root.bind("<Button-1>", lambda event : mouseEventHandler(data, canvas, event))

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # try:
    #     runWeek1()
    # except:
    #     print("Text could not be parsed to a tree; try again.")

    ## Uncomment these for Week 2 ##
    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # try:
    #     runWeek2()
    # except:
    #     print("Text could not be parsed to a tree; try again.")

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*5 + " NO WEEK 3 OUTPUT - SEE SIMULATION " + "#" * 5 + "\n")
    ## Finally, run the simulation to test it manually ##
    runSimulation(600, 650)
