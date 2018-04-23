// AI.js
// Created by MonkeyShen 2012
// 下棋的AI
require('Evaluater')
require('Util')
// var json_file = require('test.json')
var MAX_BOUND = 9999999;
var MIN_BOUND = -MAX_BOUND;

var HASH_TYPE_EXACT = 0;
var HASH_TYPE_LOWER_BOUND = 1;
var HASH_TYPE_UPPER_BOUND = 2;

AI = {

    // 当前激活的阵营
    active_camp : null,

    // 搜索深度
    max_depth : 3,

    // 搜索次数
    search_time : 0,

    // 剪枝次数
    break_time : 0,

    // hash表访问成功次数
    hash_hit_time : 0,

    // 最佳走法
    best_move : null,

    // 历史表，剪枝成功，记录下来，以后排前面，加速剪枝
    history_table : [],
    // add now to store traninstion
    arr_B_CAR : [],
    arr_B_HORSE : [],
    arr_B_ELEPHANT : [],
    arr_B_BISHOP : [],
    arr_B_KING : [],
    arr_B_CANNON : [],
    arr_B_PAWN : [],
    arr_R_CAR : [],
    arr_R_HORSE : [],
    arr_R_ELEPHANT : [],
    arr_R_BISHOP : [],
    arr_R_KING : [],
    arr_R_CANNON : [],
    arr_R_PAWN : [],
    arr_NOCHESS : [],

    black_loc: [],
    camp_MSG : [],

    // 时间
    start_time : 0,
    end_time : 0,

    // hash相关
    chess_hash_key : null,
    chess_hash_checksum : null,
    chess_hash_keys : [],
    chess_hash_checksums : [],
    chess_hash_items : [{}, {}],


    // 初始化
    init : function() {
        this._init_hash_key();
    },

    // 下一步棋
    play_a_chess : function(camp) {
        this.best_move = null;
        this.break_time = 0;
        this.search_time = 0;
        this.hash_hit_time = 0;
        this.active_camp = camp;
        this._reset_history_table();
        this._calc_cur_hash_key();
        // 如果棋子个数少，增加搜索深度
        var depth_levels = [16, 8, 6, 4]; 
        for (var i = 0; i < depth_levels.length; ++i) {
            if (Board.chess_num <= depth_levels[i])
                this.max_depth ++;
        }

        this.start_time = new Date().getTime();

        var val = this._alpha_beta(0, MIN_BOUND, MAX_BOUND);

        // $.ajax({
        //   type: "POST",
        //   url: "http://localhost:3000",
        //   crossDomain:true, 
        //   dataType: "json",
        //   data:JSON.stringify({name: "Dennis", address: {city: "Dub", country: "IE"}})
        //             }).done(function ( data ) {
        //                     alert("ajax callback response:"+JSON.stringify(data));
        // })
        
        this.end_time = new Date().getTime();

        // 执行计算出来的走法
        var m = this.best_move;
        Game.move_chess(m.fx, m.fy, m.tx, m.ty, {move_action : true});
        this.store_tranisition(camp,m,val,MoveGenerator.get_chesses())

        // chesses_before = MoveGenerator.get_origin_chesses()
        // chesses_after = MoveGenerator.get_chesses()

        console.log('depth = ', this.max_depth);
        console.log('break time = ', this.break_time);
        console.log('search time = ', this.search_time);
        console.log('hash hit time = ', this.hash_hit_time);
        console.log('score = ', val);
        console.log('time = ', (this.end_time - this.start_time) / 1000);
    },
    store_tranisition : function(camp,move,val,chesses_store){


        for (var y = 0; y < 10; ++y) {
            for (var x = 0; x < 9; ++x) {
                var chess = chesses_store[y][x];
                if (chess == NOCHESS){
                    break;
                }

                // black 
                if (chess == B_CAR){
                    this.arr_B_CAR.push([y,x]) 
                }
                if (chess == B_HORSE){
                    this.arr_B_HORSE.push([y,x]) 
                }
                if (chess == B_ELEPHANT){
                    this.arr_B_ELEPHANT.push([y,x]) 
                }
                if (chess == B_BISHOP){
                    this.arr_B_BISHOP.push([y,x]) 
                }
                if (chess == B_KING){
                    this.arr_B_KING.push([y,x]) 
                }
                if (chess == B_CANNON){
                    this.arr_B_CANNON.push([y,x]) 
                }
                if (chess == B_PAWN){
                    this.arr_B_PAWN.push([y,x]) 
                }

                // red 
                if (chess == R_CAR){
                    this.arr_R_CAR.push([y,x]) 
                }
                if (chess == R_HORSE){
                    this.arr_R_HORSE.push([y,x]) 
                }
                if (chess == R_ELEPHANT){
                    this.arr_R_ELEPHANT.push([y,x]) 
                }
                if (chess == R_BISHOP){
                    this.arr_R_BISHOP.push([y,x]) 
                }
                if (chess == R_KING){
                    this.arr_R_KING.push([y,x]) 
                }
                if (chess == R_CANNON){
                    this.arr_R_CANNON.push([y,x]) 
                }
                if (chess == B_PAWN){
                    this.arr_R_PAWN.push([y,x]) 
                }
            }
        }

        while(this.arr_B_CAR.length != 2){
            this.arr_B_CAR.push([-1,-1])
        } 
        while(this.arr_B_HORSE.length != 2){
            this.arr_B_HORSE.push([-1,-1])
        } 
        while(this.arr_B_ELEPHANT.length != 2){
            this.arr_B_ELEPHANT.push([-1,-1])
        } 
        while(this.arr_B_BISHOP.length != 2){
            this.arr_B_BISHOP.push([-1,-1])
        } 
        while(this.arr_B_KING.length != 2){
            this.arr_B_KING.push([-1,-1])
        } 
        while(this.arr_B_CANNON.length != 2){
            this.arr_B_CANNON.push([-1,-1])
        } 
        while(this.arr_B_PAWN.length != 2){
            this.arr_B_PAWN.push([-1,-1])
        } 


        // red
        while(this.arr_R_CAR.length != 2){
            this.arr_R_CAR.push([-1,-1])
        } 
        while(this.arr_R_HORSE.length != 2){
            this.arr_R_HORSE.push([-1,-1])
        } 
        while(this.arr_R_ELEPHANT.length != 2){
            this.arr_R_ELEPHANT.push([-1,-1])
        } 
        while(this.arr_R_BISHOP.length != 2){
            this.arr_R_BISHOP.push([-1,-1])
        } 
        while(this.arr_R_KING.length != 2){
            this.arr_R_KING.push([-1,-1])
        } 
        while(this.arr_R_CANNON.length != 2){
            this.arr_R_CANNON.push([-1,-1])
        } 
        while(this.arr_R_PAWN.length != 2){
            this.arr_R_PAWN.push([-1,-1])
        } 


        this.camp_MSG.push(this.arr_R_CAR[0])
        this.camp_MSG.push(this.arr_R_CAR[1])
        this.camp_MSG.push(this.arr_R_HORSE[0])
        this.camp_MSG.push(this.arr_R_HORSE[1])
        this.camp_MSG.push(this.arr_R_ELEPHANT[0])
        this.camp_MSG.push(this.arr_R_ELEPHANT[1])
        this.camp_MSG.push(this.arr_R_BISHOP[0])
        this.camp_MSG.push(this.arr_R_BISHOP[1])
        this.camp_MSG.push(this.arr_R_KING[0])
        this.camp_MSG.push(this.arr_R_KING[1])
        this.camp_MSG.push(this.arr_R_CANNON[0])
        this.camp_MSG.push(this.arr_R_CANNON[1])
        this.camp_MSG.push(this.arr_R_PAWN[0])
        this.camp_MSG.push(this.arr_R_PAWN[1])        
        this.camp_MSG.push(this.arr_B_CAR[0])
        this.camp_MSG.push(this.arr_B_CAR[1])
        this.camp_MSG.push(this.arr_B_HORSE[0])
        this.camp_MSG.push(this.arr_B_HORSE[1])
        this.camp_MSG.push(this.arr_B_ELEPHANT[0])
        this.camp_MSG.push(this.arr_B_ELEPHANT[1])
        this.camp_MSG.push(this.arr_B_BISHOP[0])
        this.camp_MSG.push(this.arr_B_BISHOP[1])
        this.camp_MSG.push(this.arr_B_KING[0])
        this.camp_MSG.push(this.arr_B_KING[1])
        this.camp_MSG.push(this.arr_B_CANNON[0])
        this.camp_MSG.push(this.arr_B_CANNON[1])
        this.camp_MSG.push(this.arr_B_PAWN[0])
        this.camp_MSG.push(this.arr_B_PAWN[1])     


        if(camp == CAMP_RED){
            this.black_loc.push(this.camp_MSG)
        }
        if(camp == CAMP_BLACK){
            this.black_loc.push([move['fx'],move['fy'],move['tx'],move['ty']])  
            this.black_loc.push(val)          
        }
            

        this.camp_MSG = []
        this.arr_B_CAR = []
        this.arr_B_HORSE = []
        this.arr_B_ELEPHANT = []
        this.arr_B_BISHOP = []
        this.arr_B_KING = []
        this.arr_B_CANNON = []
        this.arr_B_PAWN = []
        this.arr_R_CAR = []
        this.arr_R_HORSE = []
        this.arr_R_ELEPHANT = []
        this.arr_R_BISHOP = []
        this.arr_R_KING = []
        this.arr_R_CANNON = []
        this.arr_R_PAWN = []
        this.arr_NOCHESS = []

    },
    // 设置最大深度
    set_max_depth : function(depth) {
        this.max_depth = depth;
    },

    // 重置历史表
    _reset_history_table : function() {
        this.history_table = new Array(90);
        for (var f = 0; f < 90; ++f) {
            this.history_table[f] = new Array(90);
            for (var t = 0; t < 90; ++t) {
                this.history_table[f][t] = 10;
            }
        }
    },

    // 计算hash键值
    _init_hash_key : function(chesses) {
        this.chess_hash_keys = new Array(15);
        this.chess_hash_checksums = new Array(15);
        for (var c = 0; c < 15; ++c) {
            this.chess_hash_keys[c] = new Array(10);
            this.chess_hash_checksums[c] = new Array(10);
            for (var y = 0; y < 10; ++y) {
                this.chess_hash_keys[c][y] = new Array(9);
                this.chess_hash_checksums[c][y] = new Array(9);
                for (var x = 0; x < 9; ++x) {
                    this.chess_hash_keys[c][y][x] = Math.random() * Math.pow(2, 32);
                    this.chess_hash_checksums[c][y][x] = Math.random() * Math.pow(2, 32);
                }
            }
        }
    },

    // 计算当前的hash值
    _calc_cur_hash_key : function() {
        var chesses = MoveGenerator.get_chesses();

        var key = 0;
        var checksum = 0;

        for (var y = 0; y < 10; ++y) {
            for (var x = 0; x < 9; ++x) {
                var chess = chesses[y][x];
                if (chess != NOCHESS) {
                    key = key ^ this.chess_hash_keys[chess + 7][y][x];
                    checksum = checksum ^ this.chess_hash_checksums[chess + 7][y][x];
                }
            }
        }
        
        this.chess_hash_key = key;
        this.chess_hash_checksum = checksum;
    },

    // 查找hash表，看看能不能直接获取估值
    _lookup_hash_table : function(alpha, beta, depth, camp) {
        var table_id = (camp == CAMP_RED ? 0 : 1);
        var item = this.chess_hash_items[table_id][this.chess_hash_key];

        if (item == null)
            return null;

        // 检查checksum
        if (item.checksum != this.chess_hash_checksum) {
            return null;
        }

        // 检查深度（深度过深的估值不准）
        if (item.depth > depth) {
            return null;
        }

        if (item.type == HASH_TYPE_EXACT)
            return item.score;
        else if (item.type == HASH_TYPE_LOWER_BOUND)
            if (item.score >= beta)
                return item.score;
        else if (item.type == HASH_TYPE_UPPER_BOUND)
            if (item.score <= alpha)
                return item.score;

        return null;
    },

    // 把当前局面信息记录进hash表
    _record_hash_table : function(type, score, depth, camp) {
        var table_id = (camp == CAMP_RED ? 0 : 1);
        var item = {
            type : type,
            depth : depth,
            checksum : this.chess_hash_checksum,
            score : score,
        };
        this.chess_hash_items[table_id][this.chess_hash_key] = item;
    },

    // hash移动一次，修改当前局面的hash值
    _hash_make_move : function(move) {
        var key = this.chess_hash_key;
        var checksum = this.chess_hash_checksum;

        key = key ^ this.chess_hash_keys[move.fc + 7][move.fy][move.fx];
        checksum = checksum ^ this.chess_hash_checksums[move.fc + 7][move.fy][move.fx];

        if (move.tc != NOCHESS) {
            key = key ^ this.chess_hash_keys[move.tc + 7][move.ty][move.tx];
            checksum = checksum ^ this.chess_hash_checksums[move.tc + 7][move.ty][move.tx];
        }

        key = key ^ this.chess_hash_keys[move.fc + 7][move.ty][move.tx];
        checksum = checksum ^ this.chess_hash_checksums[move.fc + 7][move.ty][move.tx];

        this.chess_hash_key = key;
        this.chess_hash_checksum = checksum;
    },

    // hash反向移动一次，修改当前局面的hash值
    _hash_unmake_move : function(move) {
        var key = this.chess_hash_key;
        var checksum = this.chess_hash_checksum;

        key = key ^ this.chess_hash_keys[move.fc + 7][move.ty][move.tx];
        checksum = checksum ^ this.chess_hash_checksums[move.fc + 7][move.ty][move.tx];

        key = key ^ this.chess_hash_keys[move.fc + 7][move.fy][move.fx];
        checksum = checksum ^ this.chess_hash_checksums[move.fc + 7][move.fy][move.fx];
        
        if (move.tc != NOCHESS) {
            key = key ^ this.chess_hash_keys[move.tc + 7][move.ty][move.tx];
            checksum = checksum ^ this.chess_hash_checksums[move.tc + 7][move.ty][move.tx];
        }

        this.chess_hash_key = key;
        this.chess_hash_checksum = checksum;
    },

    // 记录进历史表
    _record_history_score : function(move, depth) {
        var f = move.fy * 9 + move.fx;
        var t = move.ty * 9 + move.tx;
        this.history_table[f][t] += 2 << depth;
    },

    // 获取历史值
    _get_history_score : function(move, depth) {
        var f = move.fy * 9 + move.fx;
        var t = move.ty * 9 + move.tx;
        return this.history_table[f][t];
    },

    // 虚拟地走一步
    _move : function(move) {
        MoveGenerator.move_chess(move);
    },

    // 虚拟返回一步
    _unmove : function(move) {
        MoveGenerator.unmove_chess(move);
    },

    // alpha-beta搜索
    _alpha_beta : function(depth, alpha, beta) {
        var a =  0;
        var bestmove = null;

        // 增加搜索次数
        this.search_time++;

        // 决定阵营
        var camp;
        var flag;

        if (depth % 2 == 0)
            flag = 1;
        else
            flag = -1;
                    // -1
        camp = this.active_camp * flag;

        // 查找hash表，直接获取估值
        if (depth > 0) {
            var score = this._lookup_hash_table(alpha, beta, depth, camp);
            if (score != null) {
                this.hash_hit_time ++;
                return score;
            }
        }

        // 如果已经搜索到最后一层
        if(depth == this.max_depth) {
            // 估值
            var val = Evaluater.evalute(MoveGenerator.get_chesses(), camp);
            this._record_hash_table(HASH_TYPE_EXACT, val, depth, camp);
            return val;
        }

        // 创建所有可能的走法
        var move_list = MoveGenerator.create_possible_moves(camp, depth);

        // 初始化历史值
        for (var i = 0; i < move_list.length; ++i) {
            var move = move_list[i];
            move.score = this._get_history_score(move, depth, camp);
        }

        // 对move_list排一下序，提高剪枝准确性
        move_list.sort(function (a, b) {
            return b.score - a.score;
        });

        // 是否被剪枝
        var is_cutted = false;

        for(var i =0; i < move_list.length ; ++i) {
            var move = move_list[i];

            this._move(move);

            // 检查一下是不是把王给灭了
            if (move.tc == R_KING || move.tc == B_KING) {

                this._unmove(move);

                // 记录最佳走法
                if (depth == 0) {
                    this.best_move = move;
                }

                // 直接返回一个很高的分，就是这一步了
                return 18888;
            }
            else {
                this._hash_make_move(move);

                score = -this._alpha_beta(depth +1, -beta, -alpha);

                this._hash_unmake_move(move);
                this._unmove(move);
            }

            // 如果发现比上限要好
            if (score  > alpha) {
                // 保留最大值
                alpha = score;
                bestmove = move;

                // 记录最佳走法
                if (depth == 0) {
                    this.best_move = move;
                }
            }

            // 剪枝
            if (score >= beta) {
                this.break_time ++;

                // 记录历史
                this._record_history_score(move, depth);

                // 记录hash
                this._record_hash_table(HASH_TYPE_LOWER_BOUND, score, depth, camp);
                
                // 直接返回
                return score;
            }
        }

        // 将最佳走法记录进历史表，虽然它没有造成剪枝
        if (bestmove != null) {
            this._record_hash_table(bestmove, depth);
            this._record_hash_table(HASH_TYPE_EXACT, alpha, depth, camp);
        }
        else {
            this._record_hash_table(HASH_TYPE_UPPER_BOUND, alpha, depth, camp);
        }

        return alpha;
    }
}

