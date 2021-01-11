import os
import pprint
import random

board = [
    [0,8,5,3,0,0,0,0,0],
    [7,0,0,0,0,0,0,2,0],
    [2,0,9,0,4,0,0,8,3],
    [0,0,0,1,0,0,0,0,8],
    [0,0,0,0,0,4,9,3,0],
    [1,0,0,0,3,0,0,4,0],
    [9,0,0,7,0,0,0,0,0],
    [0,0,3,5,0,0,0,0,9],
    [0,0,1,0,0,0,7,0,0]
]

# board = [
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0]
# ]


# ans = [
#     [6,8,5,3,2,1,4,9,7],
#     [7,3,4,9,8,5,1,2,6],
#     [2,1,9,6,4,7,5,8,3],
#     [3,4,2,1,5,9,6,7,8],
#     [5,6,8,2,7,4,9,3,1],
#     [1,9,7,8,3,6,2,4,5],
#     [9,2,6,7,1,8,3,5,4],
#     [4,7,3,5,6,2,8,1,9],
#     [8,5,1,4,9,3,7,6,2]
# ]



def empty_cell(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return i, j
    return -1, -1

def solve(b):
    i, j = empty_cell(b)
    if i == -1:
        return True
    else:
        while True:
            for k in range(1,11):
                if k == 10:
                    b[i][j] = 0
                    return False
                valid = True
                #row check
                if k in b[i]:
                    valid = False
                #col check
                for x in range(len(b)):
                    if k == b[x][j]:
                        valid = False
                #box check, find box to check
                big_y = (i // 3) * 3 #big y
                big_x = (j // 3) * 3 #big x
                for y in range(big_y, big_y + 3):
                    for x in range(big_x, big_x + 3):
                        if k == b[y][x]:
                            valid = False
                
                #if valid, recurse, otherwise try next number
                if valid:
                    b[i][j] = k
                    if solve(b):
                        return True
                
            
def main():
    print('------UNSOLVED------')
    pprint.pprint(board)
    solve(board)
    print('-------SOLVED-------')
    pprint.pprint(board)

if __name__ == "__main__":
    main()
