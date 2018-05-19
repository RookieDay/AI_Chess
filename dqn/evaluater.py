# // Evaluater.js
# // Created by MonkeyShen 2012
# // 估值器，根据棋盘局面进行估值
# // 考虑：
# // * 基础棋子价值
# // * 棋子机动性
# // * 棋子攻击点
# // * 棋子防守点
# // * 空心炮
# // * 窝心马

# // 不同棋子的基本价值
 VAL_PAWN        = 120 
 VAL_BISHOP      = 250
 VAL_ELEPHANT    = 250
 VAL_CAR         = 500
 VAL_HORSE       = 350
 VAL_CANNON      = 350
 VAL_KING        = 10000

 _chess_values = [] 

// +7为的是让他们能状态数组中
_chess_values[7 + R_PAWN]       = VAL_PAWN;
_chess_values[7 + R_BISHOP]     = VAL_BISHOP;
_chess_values[7 + R_ELEPHANT]   = VAL_ELEPHANT;
_chess_values[7 + R_CAR]        = VAL_CAR;
_chess_values[7 + R_HORSE]      = VAL_HORSE;
_chess_values[7 + R_CANNON]     = VAL_CANNON;
_chess_values[7 + R_KING]       = VAL_KING;
_chess_values[7 + NOCHESS]      = 0;
_chess_values[7 + B_PAWN]       = VAL_PAWN;
_chess_values[7 + B_BISHOP]     = VAL_BISHOP;
_chess_values[7 + B_ELEPHANT]   = VAL_ELEPHANT;
_chess_values[7 + B_CAR]        = VAL_CAR;
_chess_values[7 + B_HORSE]      = VAL_HORSE;
_chess_values[7 + B_CANNON]     = VAL_CANNON;
_chess_values[7 + B_KING]       = VAL_KING;

// 不同棋子的灵活度
 FLEXIBILITY_PAWN        = 15 
 FLEXIBILITY_BISHOP      = 1
 FLEXIBILITY_ELEPHANT    = 1
 FLEXIBILITY_CAR         = 6
 FLEXIBILITY_HORSE       = 12
 FLEXIBILITY_CANNON      = 6
 FLEXIBILITY_KING        = 0

 _chess_fexibility = []
//  卒 士 象 车 马 炮 将
_chess_fexibility[7 + R_PAWN]       = FLEXIBILITY_PAWN;
_chess_fexibility[7 + R_BISHOP]     = FLEXIBILITY_BISHOP;
_chess_fexibility[7 + R_ELEPHANT]   = FLEXIBILITY_ELEPHANT;
_chess_fexibility[7 + R_CAR]        = FLEXIBILITY_CAR;
_chess_fexibility[7 + R_HORSE]      = FLEXIBILITY_HORSE;
_chess_fexibility[7 + R_CANNON]     = FLEXIBILITY_CANNON;
_chess_fexibility[7 + R_KING]       = FLEXIBILITY_KING;
_chess_fexibility[7 + NOCHESS]      = 0;
_chess_fexibility[7 + B_PAWN]       = FLEXIBILITY_PAWN;
_chess_fexibility[7 + B_BISHOP]     = FLEXIBILITY_BISHOP;
_chess_fexibility[7 + B_ELEPHANT]   = FLEXIBILITY_ELEPHANT;
_chess_fexibility[7 + B_CAR]        = FLEXIBILITY_CAR;
_chess_fexibility[7 + B_HORSE]      = FLEXIBILITY_HORSE;
_chess_fexibility[7 + B_CANNON]     = FLEXIBILITY_CANNON;
_chess_fexibility[7 + B_KING]       = FLEXIBILITY_KING;

// 兵在不同位置的价值
 _pawn_values =
[
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
	[90,90,110,120,120,120,110,90,90  ],
	[90,90,110,120,120,120,110,90,90  ],
	[70,90,110,110,110,110,110,90,70  ],
	[70,70,70, 70, 70,  70, 70,70,70  ],
	[0,  0,  0,  0,  0,  0,  0,  0,  0],
	[0,  0,  0,  0,  0,  0,  0,  0,  0],
	[0,  0,  0,  0,  0,  0,  0,  0,  0],
	[0,  0,  0,  0,  0,  0,  0,  0,  0],
	[0,  0,  0,  0,  0,  0,  0,  0,  0],
];




def evalute(chesses, camp_turn):

 
     relate_poses = []
     cur_chess;
     cur_target_chess;
     sum_value = 0;
    
    # // 初始化二维数组
     chess_values = new Array(10);
     flex_poses   = new Array(10);
     guard_poses  = new Array(10);
     attack_poses = new Array(10);

    for i in range(10) :
        chess_values[i] = new Array(0,0,0,0,0,0,0,0,0);
        flex_poses[i]   = new Array(0,0,0,0,0,0,0,0,0);
        guard_poses[i]  = new Array(0,0,0,0,0,0,0,0,0);
        attack_poses[i] = new Array(0,0,0,0,0,0,0,0,0);
    
    # // 估值
    for i in range(10):
        for j in range(9):
            if(chesses[i][j] == NOCHESS):
                continue;
            # // 获取所有与本棋子相关的位置
            cur_chess = chesses[i][j];
            _get_relate_piece(chesses, j, i);

            # // 求机动性/防守值/攻击值
            for k in range(relate_poses.length) :
                cur_target_chess = chesses[relate_poses[k].y][relate_poses[k].x];
                if (cur_target_chess == NOCHESS) :
                    flex_poses[i][j]++;	
                else :
                     y = relate_poses[k].y;
                     x = relate_poses[k].x;

                    if (cur_chess * cur_target_chess > 0) :
                        guard_poses[y][x]++;
                    
                    else :
                        attack_poses[y][x]++;
                        flex_poses[i][j]++;	
                        for case in switch (cur_target_chess):
                            if case(R_KING):
                                if (camp_turn == CAMP_BLACK):
                                    return 18888;
                                break;
                            if case(B_KING):
                                if (camp_turn == CAMP_RED):
                                    return 18888;
                                break;
                            if case():
                                // 考虑攻击的棋子的价值
                                // attack_poses[relate_poses[k].y][relate_poses[k].x] += (30 + (_chess_values[cur_target_chess + 7] - _chess_values[cur_chess + 7])/10)/10;
                                attack_poses[y][x] += _chess_values[cur_target_chess + 7] / 100;
                                break;
            # // 空心炮
            if (cur_chess == R_CANNON) :
                # // 红炮
                 x = j;
                 y = i - 1;
                 flag = true;
                while (y >= 0) :
                     tc = chesses[y][x];
                    if (tc != NOCHESS && tc != B_KING) :
                        flag = false;
                        break;
                    y --;
                if (flag):
                    chess_values[i][j] += 150 * camp_turn;
            elif (cur_chess == B_CANNON) :
                # // 黑炮
                 x = j;
                 y = i + 1;
                 flag = true;
                while (y < 10) :
                     tc = chesses[y][x];
                    if (tc != NOCHESS && tc != R_KING) :
                        flag = false;
                        break;
                    y ++;
                if (flag):
                    chess_values[i][j] -= 150 * camp_turn;

            # // 窝心马
            if (cur_chess == R_HORSE) :
                if (x == 4 && y == 1) :
                    chess_values[i][j] -= 100 * camp_turn;
             
            elif (cur_chess == B_HORSE) :
                if (x == 4 && y == 8) :
                    chess_values[i][j] += 100 * camp_turn;
                

    # // 小兵的价值 + 机动性
    for i in range(10)：
        for j in range(9):
            if(chesses[i][j] != NOCHESS) :
                cur_chess = chesses[i][j];
                # // 机动性
                chess_values[i][j] += _chess_fexibility[cur_chess + 7] * flex_poses[i][j];

                # // 小兵价值
                chess_values[i][j] += _get_bing_value(j, i, chesses);
    

    # // 综合攻击点/防守点 改变每个棋子本身的价值
     half_value;
    for i in range(10):
        for j in rage(9):
            cur_chess = chesses[i][j];
            if(cur_chess):
            
                half_value = _chess_values[cur_chess + 7]/16;

                # // 基础价值
                chess_values[i][j] += _chess_values[cur_chess + 7];
                
                if (cur_chess > 0):
                
                    # // 红棋
                    if (attack_poses[i][j]):
                    
                        if (camp_turn == CAMP_RED):
                        
                            if (cur_chess == R_KING):
                            
                                chess_values[i][j]-= 20;
                            
                            else:
                            
                                chess_values[i][j] -= half_value * 2;
                                if (guard_poses[i][j]):
                                    chess_values[i][j] += half_value;
                            
                        else:
                        
                            if (cur_chess == R_KING):
                                return 18888;
                            chess_values[i][j] -= half_value*10;
                            if (guard_poses[i][j]):
                                chess_values[i][j] += half_value*9;
                        
                        chess_values[i][j] -= attack_poses[i][j];
                    
                    else:
                    
                        if (guard_poses[i][j]):
                            chess_values[i][j] += 5;
                    
                
                else:
                
                    // 黑棋
                    if (attack_poses[i][j]):
                
                        if (camp_turn == CAMP_BLACK)：
                        
                            if (cur_chess == B_KING)：
                            
                                chess_values[i][j]-= 20;
                            
                            else：
                            
                                chess_values[i][j] -= half_value * 2;
                                if (guard_poses[i][j])：
                                    chess_values[i][j] += half_value;
                            
                        
                        else:
                        
                            if (cur_chess == B_KING):
                                return 18888;
                            chess_values[i][j] -= half_value*10;
                            if (guard_poses[i][j]):
                                chess_values[i][j] += half_value*9;
                        
                        chess_values[i][j] -= attack_poses[i][j];
                    
                    else:
                    
                        if (guard_poses[i][j]):
                            chess_values[i][j] += 5;


    // 总结棋子价值
    for i in range(10):
        for j in range(9):
        
            cur_chess = chesses[i][j];
            if (cur_chess != NOCHESS):
            
                 val = chess_values[i][j];
                if (cur_chess > 0):
                    sum_value += val;
                else:
                    sum_value -= val;
            
    
    return sum_value * camp_turn;


    # // 增加相关点
def _add_point (x, y):
    
    relate_poses.push({x : x, y : y});
    

    // 获取小兵价值
 def _get_bing_value(x, y, chesses):
    
    if (chesses[y][x] == R_PAWN):
        return _pawn_values[y][x];
    
    if (chesses[y][x] == B_PAWN):
        return _pawn_values[9 - y][x];

    return 0;

    // 获取相关棋子
def _get_relate_piece(chesses, j, i):
         flag;
         x,y;

        relate_poses = [];
        chess = chesses[i][j];

        for case in switch(chess):
            
            if case(R_KING) || case(B_KING ):
                
                for y in range(3):
                    for x in range(3,6):
                        if (MoveGenerator.is_valid_move(j, i, x, y)):
                            _add_point(x, y);
                for y in range(7,10):
                    for x in range(3,6):
                        if (MoveGenerator.is_valid_move(j, i, x, y))
                            _add_point(x, y);
                break;
                                
            if case(R_BISHOP):
                
                for y in range(7,10):
                    for x in range(3,6):
                        if (MoveGenerator.is_valid_move(j, i, x, y))
                            _add_point(x, y);
                break;
            if case(B_BISHOP):                       
                for y in range(3):
                    for x in range(3,6):
                        if (MoveGenerator.is_valid_move(j, i, x, y))
                            _add_point(x, y);
                break;
            if case(R_ELEPHANT) || case(B_ELEPHANT):                 
                x=j+2;
                y=i+2;
                if(x < 9 && y < 10  && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                
                x=j+2;
                y=i-2;
                if(x < 9 && y>=0  &&  MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                
                x=j-2;
                y=i+2;
                if(x>=0 && y < 10  && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                
                x=j-2;
                y=i-2;
                if(x>=0 && y>=0  && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);

                break;
                
            if case(R_HORSE) || case(B_HORSE):		
                x=j+2;
                y=i+1;
                if((x < 9 && y < 10) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                        
                x=j+2;
                y=i-1;
                if((x < 9 && y >= 0) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                
                x=j-2;
                y=i+1;
                if((x >= 0 && y < 10) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                
                x=j-2;
                y=i-1;
                if((x >= 0 && y >= 0) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                
                x=j+1;
                y=i+2;
                if((x < 9 && y < 10) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                x=j-1;
                y=i+2;
                if((x >= 0 && y < 10) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                x=j+1;
                y=i-2;
                if((x < 9 && y >= 0) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                x=j-1;
                y=i-2;
                if((x >= 0 && y >= 0) && MoveGenerator.is_valid_move(j, i, x, y)):
                    _add_point(x, y);
                break;
                
            if case(R_CAR) || case(B_CAR):
                x = j + 1;
                y = i;
                while(x < 9):
                
                    if( NOCHESS == chesses[y][x] ):
                        _add_point(x, y);
                    else:
                    
                        _add_point(x, y);
                        break;
                    
                    x++;
                
                
                x = j-1;
                y = i;
                while(x >= 0):
                
                    if( NOCHESS == chesses[y][x] ):
                        _add_point(x, y);
                    else:
                    
                        _add_point(x, y);
                        break;
                    
                    x--;
                
                
                x = j;
                y = i + 1;
                while(y < 10):
                
                    if( NOCHESS == chesses[y][x]):
                        _add_point(x, y);
                    else:
                    
                        _add_point(x, y);
                        break;
                    
                    y++;
                
                
                x = j;
                y = i-1;
                while(y>=0):
                
                    if( NOCHESS == chesses[y][x]):
                        _add_point(x, y);
                    else:
                    
                        _add_point(x, y);
                        break;
                    
                    y--;
                
                break;
                
            if case(R_PAWN):
                y = i - 1;
                x = j;
                
                if(y >= 0):
                    _add_point(x, y);
                
                if(i < 5):
                
                    y=i;
                    x=j+1;
                    if(x < 9 ):
                        _add_point(x, y);
                    x=j-1;
                    if(x >= 0 ):
                        _add_point(x, y);
                
                break;
                
            if case(B_PAWN) :
                y = i + 1;
                x = j;
                
                if(y < 10 ):
                    _add_point(x, y);
                
                if(i > 4):
                
                    y=i;
                    x=j+1;
                    if(x < 9):
                        _add_point(x, y);
                    x=j-1;
                    if(x >= 0):
                        _add_point(x, y);
                
                break;
                
            if case(B_CANNON) ||  case(R_CANNON) :
                
                x = j + 1;
                y = i;
                flag=false;
                while(x < 9)	:	
                
                    if( NOCHESS == chesses[y][x] ):
                    
                        if(!flag):
                            _add_point(x, y);
                    
                    else:
                    
                        if(!flag):
                            flag=true;
                        else :
                        
                            _add_point(x, y);
                            break;
                        
                    
                    x++;
                
                
                x = j - 1;
                flag = false;	
                while(x>=0):
                
                    if( NOCHESS == chesses[y][x] ):
                    
                        if(!flag):
                            _add_point(x, y);
                    
                    else
                    
                        if(!flag):
                            flag=true;
                        else :
                        
                            _add_point(x, y);
                            break;
                    
                    
                    x--;
                
                x = j;	
                y = i + 1;
                flag = false;
                while(y < 10):
                
                    if( NOCHESS == chesses[y][x] ):
                    
                        if(!flag):
                            _add_point(x, y);
                    
                    else:
                    
                        if(!flag):
                            flag=true;
                        else :
                        
                            _add_point(x, y);
                            break;
                        
                    
                    y++;
                
                
                y= i - 1;
                flag = false;	
                while(y >= 0):
                
                    if( NOCHESS == chesses[y][x] ):
                    
                        if(!flag):
                            _add_point(x, y);
                    
                    else:
                    
                        if(!flag):
                            flag=true;
                        else :
                        
                            _add_point(x, y);
                            break;
                        
                    
                    y--;
                
                break;
                
            if case():
                break;
            
   