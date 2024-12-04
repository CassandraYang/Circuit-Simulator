from hw6_circuit import *

### WEEK 1 TESTS ###

def testFindMatchingParen():
    print("Testing findMatchingParen()...", end="")
    expr = "(((X) AND (NOT ((Y) OR (X)))) OR (Y))"
    assert(findMatchingParen(expr, 0) == len(expr) - 1)
    assert(findMatchingParen(expr, 1) == 28)
    assert(findMatchingParen(expr, 2) == 4)
    assert(findMatchingParen(expr, 10) == 27)
    assert(findMatchingParen(expr, 15) == 26)
    assert(findMatchingParen(expr, 16) == 18)
    assert(findMatchingParen(expr, 23) == 25)
    assert(findMatchingParen(expr, 33) == 35)
    print("... done!")

def testGetTokenBounds():
    print("Testing getTokenBounds()...", end="")
    expr = "(X AND (NOT (Y OR X))) OR Y"
    assert(getTokenBounds(expr, 1) == [1, 1])
    assert(getTokenBounds(expr, 2) == [3, 5])
    assert(getTokenBounds(expr, 8) == [8, 10])
    assert(getTokenBounds(expr, 13) == [13, 13])
    assert(getTokenBounds(expr, 14) == [15, 16])
    assert(getTokenBounds(expr, 22) == [23, 24])
    assert(getTokenBounds(expr, 26) == [26, 26])
    print("... done!")

def testParseExpr():
    print("Testing parseExpr()...", end="")
    assert(parseExpr("X") == {"contents": "X", "children":[]})
    assert(parseExpr("(Y)") == {"contents": "Y", "children":[]})
    assert(parseExpr("(NOT X)") == {"contents": "NOT", "children":[{"contents": "X", "children":[]}]})
    assert(parseExpr("(FOO AND BAR)") == {"contents": "AND", "children":[{"contents": "FOO", "children":[]}, {"contents": "BAR", "children":[]}]})
    assert(parseExpr("(X) XOR (Y)") == {"contents": "XOR", "children":[{"contents": "X", "children":[]}, {"contents": "Y", "children":[]}]})
    assert(parseExpr("((FOO) OR (BAR))") == {"contents": "OR", "children":[{"contents": "FOO", "children":[]}, {"contents": "BAR", "children":[]}]})
    assert(parseExpr("(X AND (NOT (Y OR X))) OR Y") == { "contents" : "OR", "children" : [
        { "contents" : "AND", "children" : [
            { "contents" : "X", "children" : []},
            { "contents" : "NOT", "children" : [
                { "contents" : "OR", "children" : [
                    { "contents" : "Y", "children" : []},
                    { "contents" : "X", "children" : []} ]
                } ]
            } ]
        },
        { "contents" : "Y", "children" : []} ]
    })
    assert(parseExpr("X AND ((NOT (Y OR X)) OR Y)") == { "contents" : "AND", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "OR", "children" : [
            { "contents" : "NOT", "children" : [
                { "contents" : "OR", "children" : [
                    { "contents" : "Y", "children" : [] },
                    { "contents" : "X", "children" : [] } ]
                } ],
            },
            { "contents" : "Y", "children" : [] } ]
        } ]
    })
    print("... done!")

def testValidateTree():
    print("Testing validateTree()...", end="")
    assert(validateTree({ }) == False)
    assert(validateTree({ "contents" : "X", "children" : [] }) == True)
    assert(validateTree({ "contents" : "Y", "children" : [] }) == True)
    assert(validateTree({ "contents" : "AND", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }) == True)
    assert(validateTree({ "contents" : "OR", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }) == True)
    assert(validateTree({ "contents" : "XOR", "children" : [
        { "contents" : "FOO", "children" : [] },
        { "contents" : "BAR", "children" : [] } ]
    }) == True)
    assert(validateTree({ "contents" : "NOT", "children" : [
        { "contents" : "X", "children" : [] } ]
    }) == True)
    assert(validateTree({ "contents" : "OR", "children" : [
        { "contents" : "AND", "children" : [
            { "contents" : "X", "children" : [] },
            { "contents" : "OR", "children" : [
                { "contents" : "NOT", "children" : [
                    { "contents" : "Y", "children" : [] } ]
                },
                { "contents" : "Y", "children" : [] } ]
            } ]
        },
        { "contents" : "Y", "children" : [] } ]
    }) == True)

    assert(validateTree({ "contents" : "NOT", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }) == False)
    assert(validateTree({ "contents" : "AND", "children": [
        { "contents" : "X", "children" : [] } ]
    }) == False)
    print("... done!")

def week1Tests():
    testFindMatchingParen()
    testGetTokenBounds()
    testParseExpr()
    testValidateTree()


#### WEEK 2 TESTS ####

def testGetLeaves():
    print("Testing getLeaves()...", end="")
    assert(getLeaves({ "contents" : "X", "children" : [] }) == [ "X" ])
    assert(getLeaves({ "contents" : "Y", "children" : [] }) == [ "Y" ])
    assert(getLeaves({ "contents" : "AND", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }) == [ "X", "Y" ])
    assert(getLeaves({ "contents" : "OR", "children" : [
        { "contents" : "Y", "children" : [] },
        { "contents" : "X", "children" : [] } ]
    }) == [ "X", "Y" ])
    assert(getLeaves({ "contents" : "XOR", "children" : [
        { "contents" : "FOO", "children" : [] },
        { "contents" : "BAR", "children" : [] } ]
    }) == [ "BAR", "FOO" ])
    assert(getLeaves({ "contents" : "NOT", "children" : [
        { "contents" : "Z", "children" : [] } ]
    }) == [ "Z" ])
    assert(getLeaves({ "contents" : "OR", "children" : [
        { "contents" : "AND", "children" : [
            { "contents" : "X", "children" : [] },
            { "contents" : "OR", "children" : [
                { "contents" : "NOT", "children" : [
                    { "contents" : "Y", "children" : [] } ]
                },
                { "contents" : "Y", "children" : [] } ]
            } ]
        },
        { "contents" : "Y", "children" : [] } ]
    }) == [ "X", "Y" ])
    assert(getLeaves({ "contents" : "OR", "children" : [
        { "contents" : "AND", "children" : [
            { "contents" : "X", "children" : [] },
            { "contents" : "Y", "children" : [] } ]
        },
        { "contents" : "XOR", "children" : [
            { "contents" : "Y", "children" : [] },
            { "contents" : "Z", "children" : [] } ]
        } ]
    }) == [ "X", "Y", "Z" ])
    print("... done!")

def testGenerateAllInputs():
    print("Testing generateAllInputs()...", end="")
    assert(generateAllInputs(0) == [ [] ])
    assert(sorted(generateAllInputs(1)) == [ [False], [True] ])
    assert(sorted(generateAllInputs(2)) == [ [False, False], [False, True], [True, False], [True, True] ])
    assert(sorted(generateAllInputs(3)) == [ [False, False, False], [False, False, True],
        [False, True, False], [False, True, True], [True, False, False], [True, False, True],
        [True, True, False], [True, True, True] ])
    print("... done!")

def testEvalTree():
    print("Testing evalTree()...", end="")
    # basic inputs
    assert(evalTree({ "contents" : "X", "children" : []}, { "X" : False }) == False)
    assert(evalTree({ "contents" : "X", "children" : []}, { "X" : True }) == True)
    not_y = { "contents" : "NOT", "children" : [ { "contents" : "Y", "children" : [] } ] }
    assert(evalTree(not_y, { "Y" : False }) == True)
    assert(evalTree(not_y, { "Y" : True }) == False)
    x_and_y = { "contents" : "AND", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }
    assert(evalTree(x_and_y, { "X" : False, "Y" : False }) == False)
    assert(evalTree(x_and_y, { "X" : False, "Y" : True }) == False)
    assert(evalTree(x_and_y, { "X" : True, "Y" : False }) == False)
    assert(evalTree(x_and_y, { "X" : True, "Y" : True }) == True)
    x_or_y = { "contents" : "OR", "children" : [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }
    assert(evalTree(x_or_y, { "X" : False, "Y" : False }) == False)
    assert(evalTree(x_or_y, { "X" : False, "Y" : True }) == True)
    assert(evalTree(x_or_y, { "X" : True, "Y" : False }) == True)
    assert(evalTree(x_or_y, { "X" : True, "Y" : True }) == True)
    x_xor_y = { "contents" : "XOR", "children": [
        { "contents" : "X", "children" : [] },
        { "contents" : "Y", "children" : [] } ]
    }
    assert(evalTree(x_xor_y, { "X" : False, "Y" : False }) == False)
    assert(evalTree(x_xor_y, { "X" : False, "Y" : True }) == True)
    assert(evalTree(x_xor_y, { "X" : True, "Y" : False }) == True)
    assert(evalTree(x_xor_y, { "X" : True, "Y" : True }) == False)

    # more complicated expressions
    # (X AND ((NOT Y) OR Z)) OR Y
    expr_1 = { "contents" : "OR", "children" : [
        { "contents" : "AND", "children" : [
            { "contents" : "X", "children" : [] },
            { "contents" : "OR", "children" : [
                { "contents" : "NOT", "children" : [
                    { "contents" : "Y", "children" : [] } ]
                },
                { "contents" : "Z", "children" : [] } ]
            } ]
        },
        { "contents" : "Y", "children" : [] } ]
    }
    assert(evalTree(expr_1, { "X" : False, "Y" : False, "Z" : False }) == False)
    assert(evalTree(expr_1, { "X" : False, "Y" : False, "Z" : True }) == False)
    assert(evalTree(expr_1, { "X" : False, "Y" : True, "Z" : False }) == True)
    assert(evalTree(expr_1, { "X" : False, "Y" : True, "Z" : True }) == True)
    assert(evalTree(expr_1, { "X" : True, "Y" : False, "Z" : False }) == True)
    assert(evalTree(expr_1, { "X" : True, "Y" : False, "Z" : True }) == True)
    assert(evalTree(expr_1, { "X" : True, "Y" : True, "Z" : False }) == True)
    assert(evalTree(expr_1, { "X" : True, "Y" : True, "Z" : True }) == True)
    print("... done!")

def testMakeTruthTable():
    print("Testing makeTruthTable()...")
    expr = { "contents" : "OR", "children" : [
        { "contents" : "AND", "children" : [
            { "contents" : "X", "children" : [] },
            { "contents" : "OR", "children" : [
                { "contents" : "NOT", "children" : [
                    { "contents" : "Y", "children" : [] } ]
                },
                { "contents" : "Z", "children" : [] } ]
            } ]
        },
        { "contents" : "Y", "children" : [] } ]
    }
    makeTruthTable(expr)
    print("... check the table to see if it looks right!")

def week2Tests():
    testGetLeaves()
    testGenerateAllInputs()
    testEvalTree()
    testMakeTruthTable()


### WEEK 3 TESTS ###