#  Created by Jacob CM.
import random
global row
global rightDiagonal
global leftDiagonal
global emptyRows

def toRightDiagonal(x,y):
    return x+y-1

def toLeftDiagonal(x,y,n):
    return x+(n-y)

def findNewY(x,n,board):
    global rightDiagonal
    global leftDiagonal
    global row
    global inConflict
    
    y=board[x]
    if y+1<=n:
        minConflicts=rightDiagonal[toRightDiagonal(x,y+1)]+leftDiagonal[toLeftDiagonal(x,y+1,n)]+row[y+1]
        minY=y+1
    else:
        minConflicts=rightDiagonal[toRightDiagonal(x,y-1)]+leftDiagonal[toLeftDiagonal(x,y-1,n)]+row[y-1]
        minY=y-1
    y+=1
    while y<=n:
        numConflicts=rightDiagonal[toRightDiagonal(x,y)]+leftDiagonal[toLeftDiagonal(x,y,n)]+row[y]
        if numConflicts==0:
            return y
        elif numConflicts<minConflicts:
            minConflicts=numConflicts
            minY=y
        y+=1
    y=board[x]-1
    while y>0:
        numConflicts=rightDiagonal[toRightDiagonal(x,y)]+leftDiagonal[toLeftDiagonal(x,y,n)]+row[y]
        if numConflicts==0:
            return y
        if numConflicts<minConflicts:
            minConflicts=numConflicts
            minY=y
        y-=1
        
    return minY

def repair(board,n):
    global rightDiagonal
    global leftDiagonal
    global row
    changes=1
    count=0
    while changes!=0 or count>100:
        changes=0
        for x in range(n):
            if inConflict(x,board[x],n):
                newY=findNewY(x,n,board)
                
                rightDiagonal[toRightDiagonal(x,board[x])]-=1
                leftDiagonal[toLeftDiagonal(x,board[x],n)]-=1
                row[board[x]]-=1
                rightDiagonal[toRightDiagonal(x,newY)]+=1
                leftDiagonal[toLeftDiagonal(x,newY,n)]+=1
                row[newY]+=1
                
                board[x]=newY
                changes+=1
        count+=1
    if changes==0:
        return board
    else:
        repair(createGreedyBoard(n),n)

def findNewYBig(x,n,board):
    global rightDiagonal
    global leftDiagonal
    global row
    global emptyRows
    
    for i in emptyRows:
        if row[i] + rightDiagonal[toRightDiagonal(x,i)] + leftDiagonal[toLeftDiagonal(x,i,n)] == 0:
            return i
    while True:
        y=random.randint(1,n)
        if row[y] + rightDiagonal[toRightDiagonal(x,y)] + leftDiagonal[toLeftDiagonal(x,y,n)] == 1 and y!=board[x]:
            return y

def repairBig(board,n):
    global rightDiagonal
    global leftDiagonal
    global row
    global emptyRows
    changes=1
    count=0
    while changes!=0 or count>100:
        changes=0
        for x in range(n):
            if inConflict(x,board[x],n):
                newY=findNewYBig(x,n,board)
                
                rightDiagonal[toRightDiagonal(x,board[x])]-=1
                leftDiagonal[toLeftDiagonal(x,board[x],n)]-=1
                row[board[x]]-=1
                if row[board[x]]==0:
                    emptyRows+=[board[x]]
                rightDiagonal[toRightDiagonal(x,newY)]+=1
                leftDiagonal[toLeftDiagonal(x,newY,n)]+=1
                row[newY]+=1
                if newY in emptyRows:
                    emptyRows.remove(newY)               
                board[x]=newY
                changes+=1
        count+=1
    if changes==0:
        return board
    else:
        repair(createRandBoard(n),n)

def createBoard(n):
    global rightDiagonal
    global leftDiagonal
    global row
    global emptyRows
    
    row=[0]*(n+1)
    rightDiagonal=[0]*((2*n)-1)
    leftDiagonal=[0]*((2*n)-1)
    board=[None]*n
    y=n
    for i in range(n):
        if y<1:
            y=n-1
        board[i]=y
        row[y]+=1
        rightDiagonal[toRightDiagonal(i,y)]+=1
        leftDiagonal[toLeftDiagonal(i,y,n)]+=1
        y-=2

    emptyRows=[]
        
    return board

def createRandBoard(n):
    global rightDiagonal
    global leftDiagonal
    global row
    global emptyRows

    row=[0]*(n+1)
    rightDiagonal=[0]*((2*n)-1)
    leftDiagonal=[0]*((2*n)-1)
    board=[None]*n
    
    y=random.randint(1,n)

    for i in range(n):
        board[i]=y
        row[y]+=1
        rightDiagonal[toRightDiagonal(i,y)]+=1
        leftDiagonal[toLeftDiagonal(i,y,n)]+=1
        bestCost=n
        for i in range(5):
            rand=random.randint(1,n)
            randCost=cost(i,rand,n)
            if randCost==0:
                y=rand
                break
            elif randCost<bestCost:
                bestCost=randCost
                y=rand
                
    emptyRows=[]
    for i in range(1,n+1):
        if i not in board:
            emptyRows+=[i]
    return board
    
def cost(x,y,n):
    return row[y] + rightDiagonal[toRightDiagonal(x,y)] + leftDiagonal[toLeftDiagonal(x,y,n)]

def inConflict(x,y,n):
    return row[y] + rightDiagonal[toRightDiagonal(x,y)] + leftDiagonal[toLeftDiagonal(x,y,n)] >3

def printBoard(board,out):
    n=len(board)
    for y in range(n):
        row=""
        for x in range(n):
            if board[x]==n-y:
                row+="q "
            else:
                row+="x "
        out.write(row+"\n")

def printToShell(board):
    n=len(board)
    for y in range(n):
        row=""
        for x in range(n):
            if board[x]==n-y:
                row+="q "
            else:
                row+="x "
        print(row)

def main():

    file = open("nqueens.txt", 'r')
    out = open("nqueens_out.txt", 'w')

    lines=file.readlines()

    for i in range(len(lines)):
        n=int(lines[i])
        if n>1000:
            result=repairBig(createBoard(n),n)
        else:
            result=repair(createBoard(n),n)
        if n<256:
            printBoard(result,out)
        out.write(str(result))
        out.write("\n\n")

main()
    
