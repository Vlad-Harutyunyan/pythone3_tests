#######################################
###### EIQHT QUEEN PROBLEM ############
#######################################


import random
desk_r = 8
desk_c = 8
a = [['.' for i in range(desk_r)] for j in range(desk_c)]
dirs = [[1,1],[1,-1],[-1,1],[-1,-1],[-1,0],[0,-1],[0,1],[1,0]]

def Q_move(x,y):
    for j in range(len(dirs)):
        tempx1 = x
        tempx2 = y
        while 0 <= tempx1 < 8 and 0 <= tempx2 < 8 :
            a[tempx1][tempx2] = 'x'
            tempx1 += dirs[j][0]
            tempx2 += dirs[j][1]
    a[x][y] = 'Q'

def print_board (board):
    for row in board : 
        print(' '.join(map(str,row))) 


check = True
cnt_m = 0
while check :
    for x in range(len(a)) :
        for y in range(len(a[x])):
            rand_pos_x = random.randint(0,7)
            rand_pos_y = random.randint(0,7)
            if a[rand_pos_x][rand_pos_y] == '.':
                Q_move(rand_pos_x,rand_pos_y)
                cnt_m +=1
    
    if cnt_m == 8 :
        check = False
    else:
        a = [['.' for i in range(desk_r)] for j in range(desk_c)]
    cnt_m = 0



print_board(a)
print('\n')
