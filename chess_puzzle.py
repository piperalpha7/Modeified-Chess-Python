import random
import copy
import itertools

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    try:    
        if int(loc[1:])<=26 and 1<=(ord(loc[0])-96)<=26:
            num = ord(loc[0])-96
            return (num,int(loc[1:]))
        else:
            raise IOError
    except IOError: 
        return ('Not a valid Location')
    except ValueError:
        return ('Not a valid Location')
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    try:
        if(1<=x<=26) and (1<=y<=26):
            result=""
            result+=chr(x+96)+str(y)
            return result
        else:
            raise IOError
    except IOError: 
        return('Not a valid Location')
    except ValueError:
        return('Not a valid Location')

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_   

Board = tuple[int, list[Piece]]


def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    for i in B[1]:
        if i.pos_x== pos_X and i.pos_y== pos_Y:
            return True
    return False
	
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for i in B[1]:
            if i.pos_x==pos_X and i.pos_y==pos_Y:
                    return i

def splitb4w(B: Board) -> dict[Piece, tuple[int,int]]:
    ''' This function splits the pieces on a board to their respective teams. Teams are represented in the form of 
    dictionaries. This function is of great help in knowing at any stage exactly what are the pieces left in a team. Very useful
    for detecting pieces from own team so that there is no co occupancy at any square'''    

    dict_w={}
    dict_b={}
    for i in B[1]:
        if i.side==True:
            dict_w[i]=((i.pos_x),(i.pos_y))
        else:
            dict_b[i]=((i.pos_x),(i.pos_y))
    return (dict_w,dict_b)


class Rook(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X , pos_Y, side_)
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule4](see section Intro)
        Hint: use is_piece_at
        '''
        list_w = list(splitb4w(B)[0].values())
        list_b = list(splitb4w(B)[1].values())
        k=0
        while (is_piece_at(pos_X,pos_Y,B))==True and k==0:
            k+=1
            a= piece_at(pos_X,pos_Y,B)
            while (a.pos_x,a.pos_y) in list_w and (self.pos_x,self.pos_y) in list_w or (a.pos_x,a.pos_y) in list_b and (self.pos_x,self.pos_y) in list_b and k==1:
                return False 
            break 
        if ((self.pos_x==pos_X) and (1<= pos_Y<=B[0]) and (pos_Y>self.pos_y)):
                for j in range(self.pos_y+1,pos_Y):
                    if (pos_X,j) in list_w or (pos_X,j) in list_b:
                        return False 
                return True
        elif ((self.pos_x==pos_X) and (1<= pos_Y<=B[0]) and (pos_Y<self.pos_y)):
                for j in range(self.pos_y-1,pos_Y,-1):
                    if (pos_X,j) in list_w or (pos_X,j) in list_b:
                        return False 
                return True
        elif ((self.pos_y==pos_Y) and (1<= pos_X<=B[0]) and (pos_X>self.pos_x)):
                for j in range(self.pos_x+1,pos_X):
                    if (j,pos_Y) in list_w or (j,pos_Y) in list_b:
                        return False
                return True
                
        elif ((self.pos_y==pos_Y) and (1<= pos_X<=B[0]) and (pos_X<self.pos_x)):
                for j in range(self.pos_x-1,pos_X,-1):
                    if (j,pos_Y) in list_w or (j,pos_Y) in list_b:
                        return False
                return True
        else:
                return False
            
    
                    
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule2] and [Rule4] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule5], use is_check on new board
        '''
        if self.can_reach(pos_X,pos_Y,B)==True:
            tem_B= copy.deepcopy(B)
            if is_piece_at(pos_X,pos_Y,tem_B)==True:
                elim = piece_at(pos_X,pos_Y,tem_B)
                idx=B[1].index(self)
                tem_B[1][idx].pos_x=pos_X
                tem_B[1][idx].pos_y=pos_Y
                tem_B[1].remove(elim)
                if isinstance(elim,King)==True:
                    return True
                elif is_check(self.side,tem_B)==False:
                    return True
                else:
                    return False
            else:
                idx=B[1].index(self)
                tem_B[1][idx].pos_x=pos_X
                tem_B[1][idx].pos_y=pos_Y
                if is_check(self.side,tem_B)==False:
                    return True
                else:
                    return False
        else:
            return False
        
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        modB=copy.deepcopy(B)
        if self.can_move_to(pos_X,pos_Y,B)== True:
            if is_piece_at(pos_X,pos_Y,B)==True:
                eliminated= piece_at(pos_X, pos_Y,modB)
                idx=B[1].index(self)
                modB[1][idx].pos_x=pos_X
                modB[1][idx].pos_y=pos_Y
                modB[1].remove(eliminated)
                return modB
            else:
                idx=B[1].index(self)
                modB[1][idx].pos_x=pos_X
                modB[1][idx].pos_y=pos_Y
                return modB
        else:
            return B   
        

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X , pos_Y, side_)
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on board B according to rule [Rule1] and [Rule4]'''
        list_w = list(splitb4w(B)[0].values())
        list_b = list(splitb4w(B)[1].values())
        if abs(self.pos_x-pos_X)==abs(self.pos_y-pos_Y) and (1<=self.pos_x and self.pos_y and pos_X and pos_Y<=B[0]):
                if (pos_X>self.pos_x) and (pos_Y>self.pos_y):
                    for j in range (1,abs(self.pos_x-pos_X)+1):
                        while (self.pos_x + j, self.pos_y + j) in list_w or (self.pos_x + j,self.pos_y + j) in list_b:
                            if (self.pos_x + j== pos_X) and (self.pos_y+j==pos_Y) and (((self.pos_x,self.pos_y) in list_w and (pos_X,pos_Y) in list_b) or ((self.pos_x,self.pos_y) in list_b and (pos_X,pos_Y) in list_w)):  
                                return True
                            return False
                        continue
                    return True
                elif (pos_X>self.pos_x) and (pos_Y<self.pos_y):
                    for j in range (1,abs(self.pos_x-pos_X)+1):
                        while (self.pos_x + j, self.pos_y - j) in list_w or (self.pos_x + j,self.pos_y - j) in list_b:
                            if (self.pos_x + j== pos_X) and (self.pos_y-j==pos_Y) and (((self.pos_x,self.pos_y) in list_w and (pos_X,pos_Y) in list_b) or((self.pos_x,self.pos_y) in list_b and (pos_X,pos_Y) in list_w)):  
                                return True
                            return False
                        continue
                    return True 
                elif (pos_X<self.pos_x) and (pos_Y>self.pos_y):
                    for j in range (1,abs(self.pos_x-pos_X)+1):
                        while (self.pos_x - j, self.pos_y + j) in list_w or (self.pos_x - j,self.pos_y + j) in list_b :
                            if (self.pos_x - j== pos_X) and (self.pos_y+j==pos_Y) and(((self.pos_x,self.pos_y) in list_w and (pos_X,pos_Y) in list_b) or((self.pos_x,self.pos_y) in list_b and (pos_X,pos_Y) in list_w)):  
                                return True
                            return False
                        continue
                    return True
                elif (pos_X<self.pos_x) and (pos_Y<self.pos_y):
                    for j in range (1,abs(self.pos_x-pos_X)+1):
                        while(self.pos_x - j, self.pos_y - j) in list_w or (self.pos_x - j,self.pos_y - j) in list_b:
                            if (self.pos_x - j== pos_X) and (self.pos_y-j==pos_Y) and (((self.pos_x,self.pos_y) in list_w and (pos_X,pos_Y) in list_b) or((self.pos_x,self.pos_y) in list_b and (pos_X,pos_Y) in list_w)):  
                                return True
                            return False
                        continue
                    return True
        else:
            return False        
                                                                           
                                                          
                           
            
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if self.can_reach(pos_X,pos_Y,B)==True:
            tem_B= copy.deepcopy(B)
            if is_piece_at(pos_X,pos_Y,tem_B)==True:
                elim = piece_at(pos_X,pos_Y,tem_B)
                idx=B[1].index(self)
                tem_B[1][idx].pos_x=pos_X
                tem_B[1][idx].pos_y=pos_Y
                tem_B[1].remove(elim)
                if isinstance(elim,King)==True:
                    return True
                elif is_check(self.side,tem_B)==False:
                    return True
                else:
                    return False
            else:
                idx=B[1].index(self)
                tem_B[1][idx].pos_x=pos_X
                tem_B[1][idx].pos_y=pos_Y
                if is_check(self.side,tem_B)==False:
                    return True
                else:
                    return False
        else:
            return False
        
        
        
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this bishop to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        modB=copy.deepcopy(B)
        if self.can_move_to(pos_X,pos_Y,B)== True:
            if is_piece_at(pos_X,pos_Y,B)==True:
                eliminated= piece_at(pos_X, pos_Y,modB)
                idx=B[1].index(self)
                modB[1][idx].pos_x=pos_X
                modB[1][idx].pos_y=pos_Y
                modB[1].remove(eliminated)
                return modB
            else:
                idx=B[1].index(self)
                modB[1][idx].pos_x=pos_X
                modB[1][idx].pos_y=pos_Y
                return modB
        else:
            return B  

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X , pos_Y, side_)
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]'''
        list_w = list(splitb4w(B)[0].values())
        list_b = list(splitb4w(B)[1].values())
        if (1<=self.pos_x and self.pos_y and pos_X and pos_Y<=B[0]) and (((self.pos_x+1==pos_X) and (self.pos_y==pos_Y)) or ((self.pos_x-1==pos_X) and (self.pos_y==pos_Y)) or ((self.pos_x==pos_X) and (self.pos_y+1==pos_Y)) or ((self.pos_x==pos_X) and (self.pos_y-1==pos_Y))):
            while((self.pos_x,self.pos_y) in list_b and (pos_X,pos_Y) in list_b) or ((self.pos_x,self.pos_y) in list_w and (pos_X,pos_Y)) in list_w:
                return False
            return True
        elif (1<=self.pos_x and self.pos_y and pos_X and pos_Y<=B[0]) and (abs(self.pos_x- pos_X)==abs(self.pos_y-pos_Y) and abs(self.pos_x-pos_X)==1 and abs(self.pos_y-pos_Y)==1):
            while ((self.pos_x,self.pos_y) in list_b and (pos_X,pos_Y) in list_b) or ((self.pos_x,self.pos_y) in list_w and (pos_X,pos_Y)) in list_w:
                return False
            return True       
        else:
            return False
        
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if self.can_reach(pos_X,pos_Y,B)==True:
            tem_B= copy.deepcopy(B)
            if is_piece_at(pos_X,pos_Y,tem_B)==True:
                elim = piece_at(pos_X,pos_Y,tem_B)
                idx=B[1].index(self)
                tem_B[1][idx].pos_x=pos_X
                tem_B[1][idx].pos_y=pos_Y
                tem_B[1].remove(elim)
                if isinstance(elim,King)==True:
                    return True
                elif is_check(self.side,tem_B)==False:
                    return True
                else:
                    return False
            else:
                idx=B[1].index(self)
                tem_B[1][idx].pos_x=pos_X
                tem_B[1][idx].pos_y=pos_Y
                if is_check(self.side,tem_B)==False:
                    return True
                else:
                    return False
        else:
            return False


    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        modB=copy.deepcopy(B)
        if self.can_move_to(pos_X,pos_Y,B)== True:
            if is_piece_at(pos_X,pos_Y,B)==True:
                eliminated= piece_at(pos_X, pos_Y,modB)
                idx=B[1].index(self)
                modB[1][idx].pos_x=pos_X
                modB[1][idx].pos_y=pos_Y
                modB[1].remove(eliminated)
                return modB
            else:
                idx=B[1].index(self)
                modB[1][idx].pos_x=pos_X
                modB[1][idx].pos_y=pos_Y
                return modB
        else:
            return B 


def bish_poss_moves(x : int, y : int, B : Board)  -> list[tuple[int,int]]:
    ''' Prepares a list of possible moves a Bishop can have according to the rules of the game without any 
    constraints like is_check etc. 'x' and 'y' are co-ordinates where the bishop stands currently.Once constraints are applied 
    the possible moves might get reduced from this list'''

    blst=[]
    i=x
    j=y
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i+1,j+1)
        blst.append(a)
        i+=1
        j+=1
        continue  
    i=x
    j=y    
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i-1,j-1)
        blst.append(a)
        i-=1
        j-=1
        continue 
    i=x
    j=y    
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i+1,j-1)
        blst.append(a)
        i+=1
        j-=1
        continue 
    i=x
    j=y    
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i-1,j+1)
        blst.append(a)
        i-=1
        j+=1
        continue 
    blst = [b for b in blst if 0<b[0]<=B[0] and 0<b[1]<=B[0]]
    return blst


def rook_poss_moves(x : int, y : int, B : Board)  -> list[tuple[int,int]]:
    ''' Prepares a list of possible moves a Rook can have according to the rules of the game without any 
    constraints like is_check etc. 'x' and 'y' are co-ordinates where the bishop stands currently.Once constraints are applied 
    the possible moves might get reduced from this list'''

    rlst=[]
    i=x
    j=y
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i+1,j)
        rlst.append(a)
        i+=1
        continue  
    i=x
    j=y    
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i-1,j)
        rlst.append(a)
        i-=1
        continue 
    i=x
    j=y    
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i,j+1)
        rlst.append(a)
        j+=1
        continue 
    i=x
    j=y    
    while i in range(1,B[0]+1) and j in range(1,B[0]+1): 
        a=(i,j-1)
        rlst.append(a)
        j-=1
        continue 
    rlst = [r for r in rlst if 0<r[0]<=B[0] and 0<r[1]<=B[0]]
    return rlst


def king_poss_moves(x : int, y : int, B : Board)  -> list[tuple[int,int]]:
    ''' Prepares a list of possible moves a King can have according to the rules of the game without any 
    constraints like is_check etc. 'x' and 'y' are co-ordinates where the bishop stands currently.Once constraints are applied 
    the possible moves might get reduced from this list'''

    klst=[]
    for i in (-1,1): 
        a=(x+i,y)
        klst.append(a)    
    for i in (-1,1): 
        a=(x,y+i)
        klst.append(a)   
    for i in (-1,1): 
        a=(x+i,y+i)
        klst.append(a)   
    for i in (-1,1): 
        a=(x+i,y-i)
        klst.append(a) 
    klst = [k for k in klst if 0<k[0]<=B[0] and 0<k[1]<=B[0]]
    return klst
    


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    for i in B[1]:
        if isinstance(i,King)==True and i.side== side:
            for j in B[1]:
                if j.can_reach(i.pos_x,i.pos_y,B)==True:
                    return True
                continue   
            return False    
                                                                                                          
                                                                                        

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''
    c=list(filter(lambda i:isinstance(i,King) and i.side==side,B[1]))
    if is_check(side,B)==True:
        k_esc= king_poss_moves(c[0].pos_x,c[0].pos_y,B)
        enem =[i for i in B[1] if i.side!=side]
        e=0
        for player in enem:
            while e < len(k_esc):
                if (player.can_reach(k_esc[e][0],k_esc[e][1],B)==True):
                    k_esc.remove(k_esc[e])
                    e=0
                elif player.can_reach(k_esc[e][0],k_esc[e][1],B)==False and c[0].can_move_to(k_esc[e][0],k_esc[e][1],B)==True:
                    k_esc=k_esc
                    e=1000
                elif player.can_reach(k_esc[e][0],k_esc[e][1],B)==False and c[0].can_move_to(k_esc[e][0],k_esc[e][1],B)==False:
                    k_esc.remove(k_esc[e])
                    e=0
                continue
            break
        
        if(len(k_esc))==0:
            return True
        else:
            return False
    else:
        return False


                                                                                      

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    try:
        file = open(filename,"r")
        dict1={index+1:line.strip() for index,line in enumerate(file)}
        brd= dict1[2].replace(" ", "").split(',')+ dict1[3].replace(" ", "").split(',')
        co_ord=[location2index(brd[i][1:]) for i in range(0,len(brd))]
        B1=[int(dict1[1])] 
        B2=[]
        if (dict1[2].count('K')==dict1[3].count('K')==1) and (len(brd)==len(set(brd))) and max(list(itertools.chain(*co_ord)))<=int(dict1[1]) and min(list(itertools.chain(*co_ord)))>=1 and 1<=B1[0]<=26:
            for wht in dict1[2].replace(" ", "").split(','):
                if wht[0]=='B':
                    loc =location2index(wht[1:])
                    wht= Bishop(loc[0],loc[1],True)
                    B2.append(wht)
                elif wht[0]=='R':
                    loc =location2index(wht[1:])
                    wht= Rook(loc[0],loc[1],True)
                    B2.append(wht)
                elif wht[0]=='K':
                    loc =location2index(wht[1:])
                    wht= King(loc[0],loc[1],True)
                    B2.append(wht)
                else:
                    raise IOError
                
            for blk in dict1[3].replace(" ", "").split(','):
                if blk[0]=='B':
                    loc =location2index(blk[1:])
                    blk= Bishop(loc[0],loc[1],False)
                    B2.append(blk)
                elif blk[0]=='R':
                    loc =location2index(blk[1:])
                    blk= Rook(loc[0],loc[1],False)
                    B2.append(blk)
                elif blk[0]=='K':
                    loc =location2index(blk[1:])
                    blk= King(loc[0],loc[1],False)
                    B2.append(blk) 
                else:
                    raise IOError
            B1.append(sorted(B2,key=lambda x:x.pos_y))
            return B1
        else:
            raise IOError
    except IOError:
        return ("File is invalid")
    except :
        return ("File is invalid")   

 

def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    try:
        w_ls=[w for w in B[1] if w.side==True]
        b_ls=[b for b in B[1] if b.side==False]   
        with open(filename,"w") as fp:   
            line= str(B[0])
            fp.write(line+"\n")
            inp1=""
            inp2=""
            for obj in w_ls:
                loc1= index2location(obj.pos_x, obj.pos_y)
                if isinstance(obj,King)==True:
                    inp1= inp1+'K'+loc1+","+" "
                elif isinstance(obj,Bishop)==True:
                    inp1= inp1+'B'+loc1+","+" "
                else:
                    inp1= inp1+'R'+loc1+","+" "
                continue
            inp1=inp1[:-2]    
            fp.write(inp1+'\n')
            for obj in b_ls:
                    loc2= index2location(obj.pos_x, obj.pos_y)
                    if isinstance(obj,King)==True:
                        inp2= inp2+'K'+loc2+","+" "
                    elif isinstance(obj,Bishop)==True:
                        inp2= inp2+'B'+loc2+","+" "
                    else:
                        inp2 = inp2+'R'+loc2+","+" "
                    continue
            inp2=inp2[:-2]    
            fp.write(inp2)
            fp.close()     
    except IOError:
        return None

        

def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''
    bl_move=0
    b_ls=[b for b in B[1] if b.side==False]
    b_ls.append(1)
    ran_pl=1
    while bl_move==0 and len(b_ls)>0:
        b_ls.remove(ran_pl)
        if len(b_ls)>0:
            ran_pl= random.choice(b_ls)
            if isinstance(ran_pl,Bishop)==True:
                bish= bish_poss_moves(ran_pl.pos_x,ran_pl.pos_y,B)
                bish= random.sample(bish,len(bish))
                for k in bish:
                    if ran_pl.can_move_to(k[0],k[1],B)==True:
                        bl_move=(ran_pl,k[0],k[1])
                        break
                    else:
                        continue
            elif isinstance(ran_pl,Rook)==True:
                ruk= rook_poss_moves(ran_pl.pos_x,ran_pl.pos_y,B)
                ruk=random.sample(ruk,len(ruk))
                for l in ruk:
                    if ran_pl.can_move_to(l[0],l[1],B)==True:
                        bl_move=(ran_pl,l[0],l[1])
                        break
                    else:
                        continue
            elif isinstance(ran_pl,King)==True:
                ruler= king_poss_moves(ran_pl.pos_x,ran_pl.pos_y,B)
                ruler=random.sample(ruler,len(ruler))
                for m in ruler:
                    if ran_pl.can_move_to(m[0],m[1],B)==True:
                        bl_move=(ran_pl,m[0],m[1])
                        break
                    else:
                        continue
                
    if len(b_ls)==0:
        return None
    else:
        return bl_move 

def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    uni= ""
    for row in range(B[0],0,-1):
            for column in range(1,B[0]+1):
                match=[j for j in B[1] if j.pos_x==column and j.pos_y==row]
                if len(match)!=0:
                    if match[0].side==True and type(match[0])== Bishop:
                        uni= uni + '\u2657' 
                    elif match[0].side== False and type(match[0])== Bishop:
                        uni = uni + '\u265D' 
                    elif match[0].side== True and type(match[0])== Rook:
                        uni = uni + '\u2656' 
                    elif match[0].side== False and type(match[0])== Rook:
                        uni = uni + '\u265C' 
                    elif match[0].side== True and type(match[0])== King:
                        uni = uni +'\u2654' 
                    elif match[0].side== False and type(match[0])== King:
                        uni = uni + '\u265A' 
                else:
                    uni= uni +'\u2001'
            if row==1 and column==B[0]:
                uni = uni
            else:
                uni=uni + "\n"
    return(uni)

def is_exception(read_board:callable,filename:str) -> bool:
    '''Function Returns whether any exceptions were raised in the read_board function'''
    if read_board(filename)=="File is invalid":
            return True
    else:
            return False


def traverse(move: str) -> tuple[str, str]:
    ''' Function splits the user defined chessmove(from and to combined) of the form for eg. 'a1b2' to ('b2','a1')'''

    for i in range(len(move)-1,0,-1):
        if move[i].isdigit()==False:
            index=i
        else:
            continue
    return(move[index:],move[0:index])
                       



def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''    
    filename = input("File name for initial configuration: ")
    done=True
    while done==True:
        try:   
                done= False
                while filename.lower()!='quit':
                    if is_exception(read_board,filename)== True:
                        filename= input("This is not a valid file. File name for initial configuration: ")
                        continue
                    else:
                        B = read_board(filename.lower())        
                        print("The current configuration is\n"+ str(conf2unicode(B)))
                        w_move = input("Next move of White: ")
                        while w_move!= None:
                            if w_move.lower()=='quit':
                                filename= input("File name to store the configuration: ")
                                save_board(filename.lower(), B)
                                w_move=None
                                filename='quit'
                                print("The game configuration is saved")
                                break
                            else:
                                w_from_loc = traverse(w_move.lower())[1]
                                w_to_loc= traverse(w_move.lower())[0]
                                w_from_ind= location2index(w_from_loc.lower())
                                w_to_ind= location2index(w_to_loc.lower())
                                if is_piece_at(w_from_ind[0], w_from_ind[1],B)==True and piece_at(w_from_ind[0], w_from_ind[1],B).side==True:
                                    w_piece=piece_at(w_from_ind[0], w_from_ind[1],B)
                                    if w_piece.can_move_to(w_to_ind[0], w_to_ind[1],B)==True and is_checkmate(True, B)==False :
                                        B=w_piece.move_to(w_to_ind[0], w_to_ind[1],B)
                                        print("The configuration after White's move is:\n"+str(conf2unicode(B)))
                                    elif is_checkmate(True, B)== True:    
                                        w_move=None
                                        filename='quit'
                                        print("Game Over. Black wins")
                                        break
                                    elif w_piece.can_move_to(w_to_ind[0], w_to_ind[1],B)==False:
                                        w_move=input("This is not a valid move. Next move of White: ")
                                        continue                  
                                elif is_piece_at(w_from_ind[0], w_from_ind[1],B)==True and piece_at(w_from_ind[0], w_from_ind[1],B).side==False:
                                     w_move=input("This is not a valid move. Next move of White: ")
                                     continue   
                                elif is_checkmate(True, B)== True:
                                    w_move=None
                                    filename='quit'
                                    print("Game Over. Black wins")
                                    break
                                elif is_piece_at(w_from_ind[0], w_from_ind[1],B)==False:
                                    w_move=input("This is not a valid move. Next move of White: ")
                                    continue
                            if find_black_move(B)!=None:
                                ran_pl,prob_x,prob_y=find_black_move(B)
                                b_from_loc=index2location(ran_pl.pos_x,ran_pl.pos_y)
                                b_to_loc= index2location(prob_x,prob_y)
                                b_from_ind= (ran_pl.pos_x,ran_pl.pos_y)
                                b_to_ind= (prob_x,prob_y)
                                B=ran_pl.move_to(prob_x, prob_y,B)
                                print ("Next move of Black is" +" "+ str(b_from_loc)+str(b_to_loc)+"."+" The configuration after Black's move is")
                                print (conf2unicode(B))
                                if is_checkmate(False, B)== False  :
                                    w_move= input("Next move of White: ")
                                    continue
                                elif is_checkmate(False, B)== True:
                                    w_move=None
                                    filename='quit'
                                    print("Game Over.White wins.")
                                    break
                            elif find_black_move(B)==None:
                                w_move=None
                                filename='quit'
                                print("Game Over. White wins")
                                continue
                                                
                print ('Exiting Game.Execute Main again to play')    
        except ValueError:
                print("This is not a valid move")
                filename= input("File name to store the temporary configuration.Game will continue: ")
                save_board(filename.lower(), B)
                done=True
        except IOError:
                done=True
                print("This is not a valid file")
        except UnboundLocalError:
                print("This is not a valid move")
                filename= input("File name to store the temporary configuration.Game will continue: ")
                save_board(filename.lower(), B)
                done=True
            
    
            
if __name__ == '__main__': #keep this in main
   main()
