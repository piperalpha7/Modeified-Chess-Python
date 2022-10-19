import pytest
import random
from chess_puzzle import *


def test_location2index1():
    assert location2index("e2") == (5,2)

def test_location2index2():     # The column number should range in between 1 and 26#
    assert location2index("z29") == 'Not a valid Location'

def test_location2index3():     # The string passed is of incorrect format.No column nos. mentioned#
    assert location2index("abc") == 'Not a valid Location'

def test_location2index4():     # Correct test#
    assert location2index("k26") == (11,26)

def test_location2index5():     # No row name mentioned #
    assert location2index("225") == 'Not a valid Location'



def test_index2location1(): 
    assert index2location(5,2) == "e2"

def test_index2location2():
    assert index2location(26,7) == "z7"

def test_index2location3 (): # Row number a to z translates between 1 and 26...30 exceeds that#
    assert index2location(30,5) == "Not a valid Location"

def test_index2location4():
    assert index2location(15,15) == "o15"

def test_index2location5():   # Random Number at column no...Hence not a valid entry#
    assert index2location(-1,26) == "Not a valid Location"



wb1 = Bishop(1,1,True)
wr1 = Rook(1,2,True)
wb2 = Bishop(5,2, True)
bk = King(2,3, False)
br1 = Rook(4,3,False)
br2 = Rook(2,4,False)
br3 = Rook(5,4, False)
wr2 = Rook(1,5, True)
wk = King(3,5, True)
wr3 = Rook(2,5,True)
br2a = Rook(1,5,False)
wr2a = Rook(2,5,True)
wb3 = Bishop(2,5,True)
wb4 = Bishop(4,1,True)
wb2a=Bishop(4,3,True)
wb1c=Bishop(3,3,True)
wb3c= Bishop(3,4,True)
br2b = Rook(4,5,False)
B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
'''
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖   ♗
♗    
'''

B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
'''
♜♖♔　　
　　　　♜
　♚　♜　
♖　　　♗
♗
'''


B3 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk, wr3])

'''
♖♖♔　　
　♜　　♜
　♚　♜　
♖　　　♗
♗
'''
B4 = (5, [wb1, wb4, wr1, wb2, bk, br1, br3, br2a, wb3, wk])

'''
♜♗♔　　
　　　　♜
　♚　♜　
♖　　　♗
♗　　♗　
'''

B5 = (5, [wb1, wr1, wb2, bk, br1, br3, wr2, wk])

'''
♖　♔　　
　　　　♜
　♚　♜　
♖　　　♗
♗　
'''

B6 = (5, [wb1, wr1, wb2a, bk, br2, br3, wr2, wk])

'''
♖　♔　　
　♜　　♜
　♚　♗　
♖　　　　
♗　
'''

B8 = (5, [wb1c, wr1, wb2, bk, br1, br2, br3, wr2, wk])   

'''
♖　♔　　
　♜　　♜
　♚♗♜　
♖　　　♗
'''
B10 = (5, [wb1, wb4, wr1, wb2, bk, br1, br2a, br3, wb3c, wk])

B11 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])

# Tests whether there is a piece at any of the specified location, returns True if present and False if absent #

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False
    
def test_is_piece_at2():
    assert is_piece_at(1,2, B1) == True

def test_is_piece_at3():
    assert is_piece_at(5,2, B1) == True

def test_is_piece_at4():
    assert is_piece_at(4,5, B1) == False

def test_is_piece_at5():
    assert is_piece_at(3,5, B1) == True

def test_is_piece_at6():          #  Invalid Co-ordinate #  
    assert is_piece_at(6,6, B1) == False


# These tests return the player/pawn present at a particular location. Wont return anything if location is empty #

def test_piece_at1():
    assert piece_at(4,3, B1) == br1

def test_piece_at2():
    assert piece_at(1,2, B1) == wr1

def test_piece_at3():
    assert piece_at(2,3, B1) == bk

def test_piece_at4():
    assert piece_at(5,2, B1) == wb2

def test_piece_at5():
    assert piece_at(3,5, B1) == wk

def test_piece_at6():              # No piece at this location ,hence returns None #
    assert piece_at(5,5, B1) == None


# These tests return whether a Rook can reach a particular location w.r.t Rule 2 and Rule 4 #

def test_can_reach1():   # Cannot Leap over a piece present at(3,5) to reach Location#
    assert wr2.can_reach(4,5, B1) == False

def test_can_reach2():   # Cannot Replace a piece of the same side or coexist at the same location# 
    assert wr2.can_reach(1,2,B1) == False

def test_can_reach3(): # Cannot move diagonally#
    assert wr1.can_reach(2,3,B1) == False

def test_can_reach4():   # Can move vertically(file)#
    assert wr1.can_reach(1,4,B1) == True 

def test_can_reach5():   # Can move horizontally(rank)#
    assert wr1.can_reach(4,2,B1) == True

def test_can_reach6():    # Random Location not pertaining to the rule ##
    assert wr2.can_reach(4,4,B1) == False

def test_can_reach7():    # Can move along a line to dislodge a piece from the opposite side#
    assert wr3.can_reach(2,4,B1) == True


# These tests return whether a Bishop can reach a particular location w.r.t Rule 1 and Rule 4 #

def test_can_reach8():    # Cannot move vertically#
    assert wb1.can_reach(1,4,B1) == False

def test_can_reach9():    # Cannot move horizontally#
    assert wb1.can_reach(5,1,B1) == False

def test_can_reach10():    # Can move diagonally#
    assert wb1.can_reach(3,3,B1) == True

def test_can_reach11():    # Cannot Leap over a piece present at(4,3) to reach Location#
    assert wb2.can_reach(3,4,B1) == False

def test_can_reach12():    # Can reach a location to dislodge a player from the opposite side diagonally#
    assert wb2.can_reach(4,3,B1) == True

def test_can_reach13():    
    assert wb3.can_reach(3,4,B4) == True
    

# These tests return whether a King can reach a particular location w.r.t Rule 3 and Rule 4 #

def test_can_reach14():    # Can move vertically for 1 square only #
    assert wk.can_reach(3,4,B1) == True

def test_can_reach15():    # Cannot move vertically for more than 1 square #
    assert wk.can_reach(3,3,B1) == False

def test_can_reach16():    # Cannot move horizontally for more than 1 square #
    assert wk.can_reach(5,5,B1) == False

def test_can_reach17():    # Can move horizontally for 1 square only #
    assert wk.can_reach(4,5,B1) == True

def test_can_reach18():    # Cannot move diagonally for more than 1 square #
    assert bk.can_reach(4,1,B1) == False

def test_can_reach19():    # Can move horizontally for 1 square only and can dislodge oponent if present  #
    assert wk.can_reach(2,4,B1) == True


# These tests return whether a Rook can move to a certain location in adherance to Rules 2,4 and 5.#
    
br2a = Rook(1,5,False)
wr2a = Rook(2,5,True)

def test_can_move_to1():   # Straight movement adhering to all rules especially King is not under check #
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
    assert wr1.can_move_to(1,4, B1) == True

def test_can_move_to2():
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
    assert wr2a.can_move_to(2,4, B2) == False

def test_can_move_to3():         #Although br2 can reach the desired location, it cannot move there because then the King is under check#
    B3 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk, wr3])
    assert br2.can_move_to(4,4, B3) == False

def test_can_move_to4():         #Cannot Leap over other pieces#
    B3 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk, wr3])
    assert wr3.can_move_to(2,2, B3) == False

def test_can_move_to5():         #Cannot move to location occupied by teammates#
    B3 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk, wr3])
    assert wr3.can_move_to(1,5, B3) == False


# These tests return whether a Bishop can move to a certain location in adherance to Rules 1,4 and 5.#
wb3 = Bishop(2,5,True)
wb4 = Bishop(4,1,True)


def test_can_move_to6():         #Can move to a location adhering to movement rules and the King not in check as well as dislodging oponent#
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
    assert wb2.can_move_to(4,3, B1) == True

def test_can_move_to7():         #Cannot move to a location adhering to movement rules causing the King to be in check#
    B4 = (5, [wb1, wb4, wr1, wb2, bk, br1, br2a, br3, wb3, wk])
    assert wb3.can_move_to(3,4, B4) == False

def test_can_move_to8():         #Cannot move to a location occupied by teammates#
    B4 = (5, [wb1, wb4, wr1, wb2, bk, br1, br2a, br3, wb3, wk])
    assert wb2.can_move_to(4,1, B4) == False

def test_can_move_to9():         #Cannot move to any arbitrary locations apart from diagonal movement, not leaping over and without ensuring King is not in check#
    B4 = (5, [wb1, wb4, wr1, wb2, bk, br1, br2a, br3, wb3, wk])
    assert wb2.can_move_to(2,3, B4) == False

def test_can_move_to10():    # Can reach to this location but cannot move as the King from the same side would be in check#
    B4 = (5, [wb1, wb4, wr1, wb2, bk, br1, br3, br2a, wb3, wk])
    assert wb3.can_move_to(3,4,B4) == False


# These tests return whether a King can move to a certain location in adherance to rules 3,4,5

def test_can_move_to11():         #Cannot move to a location since the king is safe at the current location and will be in check to all other locations he can move#
    assert wk.can_move_to(3,4, B3) == False

def test_can_move_to12():         #King can reach this location as seen above but cannot move since it results in a check at new location#
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
    assert wk.can_move_to(2,4, B1) == False 

def test_can_move_to13():         #King can reach this location as well as can move as there is no danger of check#
    assert wk.can_move_to(2,5, B5) == True

    

# The Following tests returns the board after any movement or non movement of the pieces#

def test_move_to1():     # Since bk cannot move to the desired location beacuse of check situation, the same board will be returned#
    assert bk.move_to(1,3,B1) == B1


def test_move_to2():     # Since wb2 eliminates br1 in B1, a new board B6 is formed and Returned.New board is not equal to B1#
    B7= wb2.move_to(4,3,B1)
    assert B6[0] == B7[0] == 5
    for piece in B7[1]:  #we check if every piece in B7 is also present in B6
        found = False
        for piece1 in B6[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B6[1]: #we check if every piece in B6 is also present in B7
        found = False
        for piece in B7[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found




def test_move_to3():     # Here wb1 moves to a new position without eliminating anything,still resulting into a new board B( which is eual to B8 and not B1 anymore#
    B9= wb1.move_to(3,3,B1)
    assert B8[0] == B9[0] == 5
    for piece in B9[1]:  #we check if every piece in B9 is also present in B8
        found = False
        for piece1 in B8[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B8[1]: #we check if every piece in B8 is also present in B9
        found = False
        for piece in B9[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_move_to4():     # Since the location desired is a diagonal one, rook cannot move there.Hence the original board will be returned#
    assert wr2.move_to(2,4,B1) == B1

def test_move_to5():     #The location desired is a legal one, However It would have to leap over the piece at (3,5). Thus an unchanged board is returned#
    assert wr2.move_to(5,5,B1) == B1



#  Checks if the King of the side desired is in check or not,which is can the King be Captured in one move #
def test_is_check1():
    wr2b = Rook(2,4,True)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(True, B2) == True
    
def test_is_check2():     #Checking if the Black King is in check on Board B1#
    assert is_check(False,B1)== False

def test_is_check3():    # Checking if the White King is under check on Board B1#
    assert is_check(True,B1)== False

def test_is_check4():    # Checking if the White King is under check on Board B10#
    assert is_check(True,B10)== True

def test_is_check5():    # Checking if the Black King is under check on Board B10#
    assert is_check(False,B10)== True

def test_is_check6():    # Checking if the Black King is under check on Board B3#
    assert is_check(False,B3)==False




# Checks if the King of a side is checkmated which means after being checked,he has no means of escape now#

def test_is_checkmate1():
    br2b = Rook(4,5,False)
    B11 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert is_checkmate(True, B11) == True

def test_is_checkmate2():       # Checks the checkmate condition for the white king on board B1#
    assert is_checkmate(True,B1)== False

def test_is_checkmate3():               # Checks the checkmate condition for the white king on board B3 #
    assert is_checkmate(False,B3)== False

def test_is_checkmate4():                  # Checks the checkmate condition for the white king on board B10#
    assert is_checkmate(True,B10)== True

def test_is_checkmate5():                  # Checks the checkmate condition for the black king on board B10#
    assert is_checkmate(False, B10)==True





# The read_board tests go on to show that a text file with coordinate and piece information gets converted to a board only if it follows the rules mentioned in readme.md#


def test_read_board1():                            #Reading a syntactically correct file,just goes to show what was read matched from the .txt file created a board and matched with B1# 
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_read_board2():        #Reading a syntactically correct file,just goes to show what was read matched from the .txt file created a board and matched with B10#
    B12 = read_board("B10.txt")
    assert B12[0]==B10[0] == 5

    for piece in B12[1]:  #we check if every piece in B12 is also present in B10; if not, the test will fail
        found = False
        for piece1 in B10[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B10[1]: #we check if every piece in B10 is also present in B12; if not, the test will fail
        found = False
        for piece in B12[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_read_board3():        # This file violated the syntax of having an extra comma after the last element in the row of a text file#
    assert read_board('ExtraComma.txt')== "File is invalid"


def test_read_board4():       # This file violated the rule of having more than 1 king for the same side#
    assert read_board('ExtraKing.txt')== "File is invalid"


def test_read_board5():        # This file violated the limitations of the board.The board was 5X5 yet some elements had column outside the range#
    assert read_board('OutofBounds.txt')== "File is invalid"


def test_read_board6():         # Multiple pieces were in the same place,Hence an invalid file #
    assert read_board('Sameplace.txt')== "File is invalid"

def test_read_board7():        # Does not accept any out of bound row characters(Z in this case) as well as any text disguised as coordinates#
    assert read_board('Fakecoord.txt')=='File is invalid'





# These test show us if the pieces of a board gets converted to the advised pictographic characters correctly #


def test_conf2unicode1():
    assert conf2unicode(B1) == "♖ ♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "

def test_conf2unicode2():
    assert conf2unicode(B2)== "♜♖♔  \n    ♜\n ♚ ♜ \n♖   ♗\n♗    "

def test_conf2unicode3():
    assert conf2unicode(B3)== "♖♖♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "

def test_conf2unicode4():
    assert conf2unicode(B4)== "♜♗♔  \n    ♜\n ♚ ♜ \n♖   ♗\n♗  ♗ "

def test_conf2unicode5():
    assert conf2unicode(B5)== "♖ ♔  \n    ♜\n ♚ ♜ \n♖   ♗\n♗    "

def test_conf2unicode6():
    assert conf2unicode(B6)== "♖ ♔  \n ♜  ♜\n ♚ ♗ \n♖    \n♗    "


# A simple function to split the pieces on the boards into teams of black and white in the form of dictionary#

def test_splitb4w1():
    assert splitb4w(B1)== ({wb1: (1, 1), wr1: (1, 2), wb2: (5, 2), wr2: (1, 5), wk: (3, 5)}, {bk: (2, 3), br1: (4, 3), br2: (2, 4), br3: (5, 4)})

def test_splitb4w2():
    assert splitb4w(B3)== ({wb1: (1, 1), wr1: (1, 2), wb2: (5, 2), wr2: (1, 5), wk: (3, 5), wr3: (2, 5)}, {bk: (2, 3), br1: (4, 3), br2: (2, 4), br3: (5, 4)})

def test_splitb4w3():
    assert splitb4w(B5)==({wb1: (1, 1), wr1: (1, 2), wb2: (5, 2), wr2: (1, 5), wk: (3, 5)}, {bk: (2, 3), br1: (4, 3), br3: (5, 4)})

def test_splitb4w4():
    assert splitb4w(B11)== ({wb1: (1, 1), wr1: (1, 2), wb2: (5, 2), wr2: (1, 5), wk: (3, 5)}, {bk: (2, 3), br1: (4, 3), br2b: (4, 5), br3: (5, 4)})

def test_splitb4w5():
    assert splitb4w(B6)== ({wb1: (1, 1), wr1: (1, 2), wb2a: (4, 3), wr2: (1, 5), wk: (3, 5)}, {bk: (2, 3), br2: (2, 4), br3: (5, 4)})
# This function returns all the possible moves a Bishop can have without any constraints based on its current location and the board dimensions #

def test_bish_poss_moves1():
    assert bish_poss_moves(1,1,B1)== [(2, 2), (3, 3), (4, 4), (5, 5)]

def test_bish_poss_moves2():
    assert bish_poss_moves(4,1,B10)== [(5, 2), (3, 2), (2, 3), (1, 4)]

def test_bish_poss_moves3():
    assert bish_poss_moves(5,2,B1)== [(4, 1), (4, 3), (3, 4), (2, 5)]

def test_bish_poss_moves4():
    assert bish_poss_moves(2,5,B4)== [(1, 4), (3, 4), (4, 3), (5, 2)]

def test_bish_poss_moves5():
    assert bish_poss_moves(3,4,B10)== [(4, 5), (2, 3), (1, 2), (4, 3), (5, 2), (2, 5)]


 #This function returns all the possible moves a Rook can have without any constraints based on its current location and the board dimensions #

def test_rook_poss_moves1():
   assert rook_poss_moves(1,2,B2)== [(2, 2), (3, 2), (4, 2), (5, 2), (1, 3), (1, 4), (1, 5), (1, 1)]

def test_rook_poss_moves2():
   assert rook_poss_moves(1,5,B1)== [(2, 5), (3, 5), (4, 5), (5, 5), (1, 4), (1, 3), (1, 2), (1, 1)]

def test_rook_poss_moves3():
   assert rook_poss_moves(4,3,B3)== [(5, 3), (3, 3), (2, 3), (1, 3), (4, 4), (4, 5), (4, 2), (4, 1)]

def test_rook_poss_moves4():
   assert rook_poss_moves(2,4,B3)== [(3, 4), (4, 4), (5, 4), (1, 4), (2, 5), (2, 3), (2, 2), (2, 1)]

def test_rook_poss_moves5():
   assert rook_poss_moves(5,4,B10)== [(4, 4), (3, 4), (2, 4), (1, 4), (5, 5), (5, 3), (5, 2), (5, 1)]


# This function retruns all the possible moves for a King without any constarints and based on its current location and board#

def test_king_poss_moves1():
   assert king_poss_moves(2,3,B1)== [(1, 3), (3, 3), (2, 2), (2, 4), (1, 2), (3, 4), (1, 4), (3, 2)]

def test_king_poss_moves2():
   assert king_poss_moves(3,5,B1)== [(2, 5), (4, 5), (3, 4), (2, 4), (4, 4)]

def test_king_poss_moves3():
   assert king_poss_moves(4,4,B1)== [(3, 4), (5, 4), (4, 3), (4, 5), (3, 3), (5, 5), (3, 5), (5, 3)]

def test_king_poss_moves4():
   assert king_poss_moves(3,1,B1)== [(2, 1), (4, 1), (3, 2), (4, 2), (2, 2)]

def test_king_poss_moves5():
   assert king_poss_moves(4,3,B1)== [(3, 3), (5, 3), (4, 2), (4, 4), (3, 2), (5, 4), (3, 4), (5, 2)]


# A small utility function which returns True incase the read_board function encounters an exception while reading a file and converting to a board. This happens when the file is not in the expected format#


def test_is_exception1():
    assert is_exception(read_board,'ExtraKing.txt')== True

def test_is_exception2():
    assert is_exception(read_board,'ExtraComma.txt')== True

def test_is_exception3():
    assert is_exception(read_board,'OutofBounds.txt')== True

def test_is_exception4():
    assert is_exception(read_board,'B10.txt')== False

def test_is_exception5():
    assert is_exception(read_board,'Sameplace.txt')== True


# A small utility function that splits the user entered from and to co-ordinates and returns a tuple (to_location,from_location) in the alphanumeric format

def test_traverse1():
    assert traverse('b1a2')== ('a2', 'b1')

def test_traverse2():
    assert traverse('c10a5')== ('a5', 'c10')

def test_traverse3():
    assert traverse('g7a10')== ('a10', 'g7')

def test_traverse4():
    assert traverse('c3f6')== ('f6', 'c3')

def test_traverse5():
    assert traverse('d1d6')== ('d6', 'd1')

