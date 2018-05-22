import numpy as np
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json
# from maze_env import Maze
from DQN_modified import DeepQNetwork
from server import testHTTPServer_RequestHandler
from evaluater import *
# 阵营
CAMP_RED = 1
CAMP_BLACK = -1


S_test=np.array([[-1,-2,-3,-4,-5,-4,-3,-2,-1],
                 [0,0,0,0,0,0,0,0,0],
                 [0,-6,0,0,0,0,0,-6,0],
                 [-7,0,-7,0,-7,0,-7,0,-7],
                 [0,0,0,0,0,0,0,0,0],

                 [0,0,0,0,0,0,0,0,0],
                 [7,0,7,0,7,0,7,0,7],
                 [0,6,0,0,0,0,0,6,0],
                 [0,0,0,0,0,0,0,0,0],
                 [1,2,3,4,5,4,3,2,1]
                ])
action_test=np.array([7,2,4,2])  #黑炮八平5


S_init=np.array([[1,-1,-1],[2,-1,-1],[3,-1,-1],[4,-1,-1],[5,-1,-1],[6,-1,-1],[7,-1,-1],
                 [8,-1,-1],[9,-1,-1],[10,-1,-1],[11,-1,-1],[13,-1,-1],[14,-1,-1],[21,-1,-1],[28,-1,-1],[35,-1,-1],
                 [-1,-1,-1],[-2,-1,-1],[-3,-1,-1],[-4,-1,-1],[-5,-1,-1],[-6,-1,-1],[-7,-1,-1],
                 [-8,-1,-1],[-9,-1,-1],[-10,-1,-1],[-11,-1,-1],[-13,-1,-1],[-14,-1,-1],[-21,-1,-1],[-28,-1,-1],[-35,-1,-1]
		        ])

number_init=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) #棋子计数器1*15，遍历棋盘矩阵过程中棋子-7～-1，0，1～7出现的次数。

chess_action=np.array([[-1,0,1],[-1,0,2],[-1,0,3],[-1,0,4],[-1,0,5],[-1,0,6],[-1,0,7],[-1,0,8],[-1,0,9],
                       [-1,0,-1],[-1,0,-2],[-1,0,-3],[-1,0,-4],[-1,0,-5],[-1,0,-6],[-1,0,-7],[-1,0,-8],[-1,0,-9],
					   [-1,1,0],[-1,2,0],[-1,3,0],[-1,4,0],[-1,5,0],[-1,6,0],[-1,7,0],[-1,8,0],
					   [-1,-1,0],[-1,-2,0],[-1,-3,0],[-1,-4,0],[-1,-5,0],[-1,-6,0],[-1,-7,0],[-1,-8,0],#车1
					   [-8,0,1],[-8,0,2],[-8,0,3],[-8,0,4],[-8,0,5],[-8,0,6],[-8,0,7],[-8,0,8],[-8,0,9],
                       [-8,0,-1],[-8,0,-2],[-8,0,-3],[-8,0,-4],[-8,0,-5],[-8,0,-6],[-8,0,-7],[-8,0,-8],[-8,0,-9],
					   [-8,1,0],[-8,2,0],[-8,3,0],[-8,4,0],[-8,5,0],[-8,6,0],[-8,7,0],[-8,8,0],
					   [-8,-1,0],[-8,-2,0],[-8,-3,0],[-8,-4,0],[-8,-5,0],[-8,-6,0],[-8,-7,0],[-8,-8,0],#车2
					   [-2,-2,-1],[-2,-2,1],[-2,-1,-2],[-2,-1,2],[-2,1,-2],[-2,1,2],[-2,2,-1],[-2,2,1],#马1
					   [-9,-2,-1],[-9,-2,1],[-9,-1,-2],[-9,-1,2],[-9,1,-2],[-9,1,2],[-9,2,-1],[-9,2,1],#马2
					   [-3,-2,2],[-3,-2,-2],[-3,2,-2],[-3,2,2],#相1
					   [-10,-2,2],[-10,-2,-2],[-10,2,-2],[-10,2,2],#相2
					   [-4,-1,1],[-4,-1,-1],[-4,1,-1],[-4,1,1],#士1
					   [-11,-1,1],[-11,-1,-1],[-11,1,-1],[-11,1,1],#士2
					   [-5,-1,0],[-5,1,0],[-5,0,-1],[-5,0,1],#将
					   [-6,0,1],[-6,0,2],[-6,0,3],[-6,0,4],[-6,0,5],[-6,0,6],[-6,0,7],[-6,0,8],[-6,0,9],
                       [-6,0,-1],[-6,0,-2],[-6,0,-3],[-6,0,-4],[-6,0,-5],[-6,0,-6],[-6,0,-7],[-6,0,-8],[-6,0,-9],
					   [-6,1,0],[-6,2,0],[-6,3,0],[-6,4,0],[-6,5,0],[-6,6,0],[-6,7,0],[-6,8,0],
					   [-6,-1,0],[-6,-2,0],[-6,-3,0],[-6,-4,0],[-6,-5,0],[-6,-6,0],[-6,-7,0],[-6,-8,0],#炮1
					   [-13,0,1],[-13,0,2],[-13,0,3],[-13,0,4],[-13,0,5],[-13,0,6],[-13,0,7],[-13,0,8],[-13,0,9],
                       [-13,0,-1],[-13,0,-2],[-13,0,-3],[-13,0,-4],[-13,0,-5],[-13,0,-6],[-13,0,-7],[-13,0,-8],[-13,0,-9],
					   [-13,1,0],[-13,2,0],[-13,3,0],[-13,4,0],[-13,5,0],[-13,6,0],[-13,7,0],[-13,8,0],
					   [-13,-1,0],[-13,-2,0],[-13,-3,0],[-13,-4,0],[-13,-5,0],[-13,-6,0],[-13,-7,0],[-13,-8,0],#炮2
					   [-7,-1,0],[-7,1,0],[-7,0,1],#兵1
					   [-14,-1,0],[-14,1,0],[-14,0,1],#兵2
					   [-21,-1,0],[-21,1,0],[-21,0,1],#兵3
					   [-28,-1,0],[-28,1,0],[-28,0,1],#兵4
					   [-35,-1,0],[-35,1,0],[-35,0,1]#兵5
					  ])  #黑棋动作区间，[chess+7*number*camp,deta_x,deta_y]

#定义个trans_action_to_A()，输入棋盘矩阵、动作矩阵，返回0～176的整数作为A（chess_action中对应的动作）
def trans_action_to_A(chesses,action):
    tmp = np.array(np.where(chesses == chesses[action[1],action[0]]))  #保存动作黑棋在棋盘内的所有坐标
    #print(tmp)
    for i in range(tmp.shape[1]):  #遍历相同棋子
        #print(tmp[:,i])
        action_tmp = action[:2]   #保存动作黑棋坐标
        #print(action_tmp[::-1])
        if np.array_equal(action_tmp[::-1],tmp[:,i]):   #动作黑棋坐标与遍历坐标相等
            chess_action_tmp = [chesses[action[1],action[0]]-i*7,action[2]-action[0],action[3]-action[1]]   #保存动作矩阵元素
            return np.where((chess_action == chess_action_tmp).all(1))[0]   #返回动作矩阵元素位置
            #if chesses[action[1],action[0]] < 0:
                #chess_action_tmp=[chesses[action[1],action[0]]-i*7,action[3]-action[1],action[2]-action[0]]
            #else:
                #chess_action_tmp=[chesses[action[1],action[0]]+i*7,action[3]-action[1],action[2]-action[0]]
    return False
#定义一个trans_movelist_to_A，输入move_list二维数组，输出所有对应的A数组,数组形式为长度为186的一维数组：A[0,0,0,1,0,1,...,0,0]，1对应action中可能的走法
def trans_movelist_to_A(chesses,move_list):
    A = np.zeros(186,int)
    print(len(move_list))
    for i in range(len(move_list)):
        print(move_list[i])
        A[trans_action_to_A(chesses,move_list[i])] = 1

    return A

#定义个trans_A_to_action()，输入棋盘矩阵、A，返回A对应的action(x,y,tx,ty)
def trans_A_to_action(chesses,A):
    i = 0  #计数器（棋盘中第几个棋子）
    chess_action_tmp = chess_action[A]  #保存动作矩阵中A的元素
    print('*********************')
    print(chess_action_tmp)
    #print(chess_action[A,1])
    while(chess_action_tmp[0,0] < -7):   
        i = i + 1
        chess_action_tmp[0,0] =chess_action_tmp[0,0] + 7  #动作黑棋
    tmp = np.array(np.where(chesses == chess_action_tmp[0,0]))  #保存动作黑棋在棋盘内的所有坐标
    action1 = tmp[:,i]
    action1 = action1[ : :-1]  #保存x,y    
    action2 = np.array([action1[0]+chess_action[A,1],action1[1]+chess_action[A,2]])   #保存tx,ty
    return np.append(action1,action2)


#定义一个trans_S，输入棋盘矩阵，遍历整个矩阵，输出S[],一维数组1*96
def trans_S(chesses):
    S = S_init        #初始化
    #number = number_init
    for i in range(15):   #遍历棋子
        tmp = np.array(np.where(chesses == (i-7)))   #保存棋子坐标
        #print(tmp.shape[1])
        for j in range(tmp.shape[1]):
            if i < 7:  #如果为黑棋
                S[np.where(S[:,0]==(i-7-j*7))] = np.array([(i-7-j*7),tmp[0,j],tmp[1,j]])   #黑棋棋子放入棋盘
            else:
                S[np.where(S[:,0]==(i-7+j*7))] = np.array([(i-7+j*7),tmp[0,j],tmp[1,j]])   #红棋棋子放入棋盘
    #print(S)
    return S.flatten()

def state_chess(data):
    if data.__len__() == 90:
        # line_loc = data.strip().split(',')
        numbers_loc = [int(l) for l in data]
        origin_chess = np.array(numbers_loc).reshape(10, 9)
        # 拉长后的chess 1*96
        long_chess = trans_S(numbers_loc)
        return origin_chess, long_chess
        #     # print(chess.shape)

def action_chess(origin_chess,data):
    if data.strip().__len__() == 7 and data.strip().__contains__(',') == True:
        move = data.strip().split(',')
        numbers_move = [int(l) for l in move]
        move_way = trans_action_to_A(origin_chess, numbers_move)
        return  move_way

def reward_chess(data):
    print(data)
    if data.strip().__contains__(',') == False:
        move = data.strip().split(',')
        reward_value = [float(l) for l in move]
        return  reward_value[0]

def parse_txt(file_path):
    with open(file_path,'r') as f:
        data = f.readlines()
        origin_chess =[]
        move_way = []
        data_len = data.__len__() - data.__len__() % 3
        step = 0
        for line in data:
            if len(line.strip()) != 0:
                state_char, action_char, reward_char, state_char_ = line.strip().split('|')
                # print(line.strip().split('|'))
                origin_chess, long_chess = state_chess(state_char[0:-1])
                move_way = action_chess(origin_chess,action_char.strip(','))
                reward_value = reward_chess(reward_char.strip(','))
                origin_chess_, long_chess_ = state_chess(state_char_[1:])
                # print(trans_A_to_action(origin_chess,move_way))
                RL.store_transition(long_chess, move_way, reward_value, long_chess_)
            if (step > 10) and (step % 5 == 0):
                RL.learn()
            step = step + 1

def run_this(chesses):
    print(chesses)
    # 90          1*96的
    origin_chess, long_chess = state_chess(chesses)
    action = RL.choose_action(long_chess)
    move_way = trans_A_to_action(origin_chess,[action])
    reward = evalute(origin_chess,-1)
    print(reward)
    # move_way = action_chess(origin_chess,action_char.strip(','))
    # reward_value = reward_chess(reward_char.strip(','))
    # origin_chess_, long_chess_ = state_chess(state_char_[1:])

class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.flush_headers()
    
    def do_POST(self):
        print('*'*30)
        print(self.headers['content-type'])
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self._set_headers()

        # for python 3.6
        # data = json.loads(demjson.decode(self.data_string))
        # for python 3.5
        data = json.loads(self.data_string.decode())
        chesses = data['chess_state']
        run_this(chesses)
        js_da = {"ana":"11"}
        js_du = json.dumps(js_da)
        # print(js_du.encode())
        self.wfile.write(js_du.encode())


def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == "__main__":
    #print(S_test[9,8])
    #print(trans_S(S_test))
    RL = DeepQNetwork(187, 96,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    file_path = os.getcwd() + '\\ajax_aa.txt'
    run()
    # parse_txt(file_path)
    # RL.plot_cost()
    # s = '11.200000000000728'
    # print(s.__contains__('.'))
    # print(np.loadtxt(file_path))
    # print(trans_action_to_A(S_test,action_test))
    # print(trans_A_to_action(S_test,trans_action_to_A(S_test,action_test)))