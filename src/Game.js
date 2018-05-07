// Game.js
// Created by MonkeyShen 2012
// 游戏对象，单件

var cocos = require('cocos2d');
var geo = require('geometry');
var ChessRender = require('ChessRender').ChessRender;

require('Util')
require('AI')
require('MainFrame')
require('Board')

Game = {
    chess_render : null,
    king_count : 0,
	first_king_chess : 0,    //是否第一次将军
	king_chess : 0,          //保存上一次将军棋子
	king_chess_step : 0,          //保存上一次将军手数
    win_game: false,
    red_Campstep: 0,
    black_Camstep: 0,
    scoreLabel_red: null,  // 对战红方手数的控件
    scoreLabel_black: null,  // 对战黑方手数的控件

    // 当前可以移动的正营
    cur_camp : null,

    // 玩家身份（人类还是AI）
    player_red : null,
    player_black : null,

    // 是否已经结束
    is_over : false,

    // 赢家
    winner : null,

    // 提醒被将军的sprite
    red_king_sprite : null,
    black_king_sprite : null,

    // 初始化
    init : function(layer) {

        // 初始化主界面
        MainFrame.init(layer);

        // 初始化AI
        AI.init();

        // 创建棋盘
        Board.clear_board();
        this.chess_render = ChessRender.create();
        this.chess_render.set('position', new geo.Point(174, 50));
        layer.addChild({child : this.chess_render});

        Board.add_board_listener(this);

        // 创建被将军时用于提醒的sprite
        this.red_king_sprite = cocos.nodes.Sprite.create({
            file : '/resources/jiangjun.png',
        });
        this.black_king_sprite = cocos.nodes.Sprite.create({
            file : '/resources/jiangjun.png',
        });

        this.red_king_sprite.set('position', geo.ccp(100, 100));
        this.black_king_sprite.set('position', geo.ccp(100, 500));
        this.red_king_sprite.set('visible', false);
        this.black_king_sprite.set('visible', false);

        layer.addChild(this.red_king_sprite);
        layer.addChild(this.black_king_sprite);


        // 红方手数/数量
        var label_red = cocos.nodes.Label.create({string: '红方手数：', 
                                          fontColor: '#000000',
                                          fontName: 'Arial', 
                                          fontSize: 18});
        layer.addChild({child: label_red, z:1});
        label_red.set('position', geo.ccp(78,105));

        this.scoreLabel_red = cocos.nodes.Label.create({string: '0', 
                                          fontColor: '#000000',
                                          fontName: 'Arial', 
                                          fontSize: 18});
        layer.addChild({child: this.scoreLabel_red, z:1});
        this.scoreLabel_red.set('position', geo.ccp(138,105));


        // 黑方手数/数量
        var label_black = cocos.nodes.Label.create({string: '黑方手数：', 
                                          fontColor: '#000000',
                                          fontName: 'Arial', 
                                          fontSize: 18});
        layer.addChild({child: label_black, z:1});
        label_black.set('position', geo.ccp(78,340));

        this.scoreLabel_black = cocos.nodes.Label.create({string: '0', 
                                          fontColor: '#000000',
                                          fontName: 'Arial', 
                                          fontSize: 18});
        layer.addChild({child: this.scoreLabel_black, z:1});
        this.scoreLabel_black.set('position', geo.ccp(138,340));

    },
    // 开始棋局，传入先手正营
    start : function(first_camp) {
        this.cur_camp = first_camp;
        this.is_over = false;
        Board.init_board();
        this.save_black(first_camp);
        this.step();
    },

    // 停止棋局
    stop : function() {
        this.cur_camp = null;
        this.scoreLabel_red.set('string', '0');
        this.scoreLabel_black.set('string', '0');    
        this.win_game = false;
        this.red_Campstep = 0;
        this.black_Camstep = 0;
        this.king_count = 0;
	    this.first_king_chess = 0;    //是否第一次将军
	    this.king_chess = 0;          //保存上一次将军棋子
        this.king_chess_step = 0;       //保存上一次将军手数
		Board.clear_board();
        this.is_over = true;
    },

    // 重新开始
    restart : function() {
        AI.black_loc = []
        this.win_game = false;
        this.scoreLabel_red.set('string', '0');
        this.scoreLabel_black.set('string', '0');
        this.red_Campstep = 0;
        this.black_Camstep = 0;
        this.king_count = 0;
		this.first_king_chess = 0;    //是否第一次将军
	    this.king_chess = 0;          //保存上一次将军棋子
        this.king_chess_step = 0;       //保存上一次将军手数
		Board.init_board();
        this.step();
    },
    save_black : function(start_camp){
        if(start_camp == CAMP_BLACK){
            var arr = []
            chess_ = MoveGenerator.get_chesses()
            for (var y = 0; y < 10; ++y) {
                for (var x = 0; x < 9; ++x) {
                    arr.push(chess_[y][x]);
                }
            }
            AI.black_loc.push(arr)
        }
    },
    // 悔棋
    regret : function() {
        Board.unmove_chess();

        // 如果对方不是人类，也unmove一下
        if (this.cur_camp == CAMP_RED && ! this.player_black.get('human')) {
            Board.unmove_chess();
        }
        else if (this.cur_camp == CAMP_BLACK && ! this.player_red.get('human')) {
            Board.unmove_chess();
        }
        else {
            this.step();
        }
    },

    // 玩家是否已设定
    is_player_seted : function() {
        console.log(this.player_red, this.player_black);
        return this.player_red != null && this.player_black != null;
    },

    // 某一方赢了
    win : function(camp,long_king) {
        var text;
        if (camp == CAMP_RED)
            text = long_king == true?'黑方长将,红方胜利了' :'红方胜利了';
        else
            text = long_king == true?'红方长将,黑方胜利了' :'黑方胜利了';
        this.win_game = true

        // $.ajax({
        //   type: "POST",
        //   url: "http://127.0.0.1:8000/",
        //   crossDomain:true, 
        //   dataType: "json",
        //   // JSON.stringify()用于从一个对象解析出字符串
        //   data:JSON.stringify({bk_loc: AI.black_loc})
        //             }).done(function ( data ) {
        //                     alert('hahah'+data);
        // })

        $.ajax({
          type: "POST",
          url: "http://127.0.0.1:8000/",
          crossDomain:true, 
          dataType: "json",
          // JSON.stringify()用于从一个对象解析出字符串
          data:JSON.stringify({bk_loc: AI.black_loc}),
          success:function(data) { 
                if(data.msg =="true" ){ 
                    console.log("修改成功！"); 
                }else{ 
                    console.log("修改失败！"); 
                } 
         }
        })

        // 回调
        function callback(v) {
            if (v == 'replay')
                Game.restart();
            else
                Game.stop();
        }

        $.prompt(text, {
            buttons : {
                重新开始 : 'replay',
                退出 : 'quit',
            },
            callback : callback,
        });
    },
    // 判定为和棋
    draw_chess : function () {
        var text;
        text = '对战超多150手,和棋';

        this.win_game = true
        // 回调

        $.ajax({
          type: "POST",
          url: "http://127.0.0.1:8000",
          crossDomain:true, 
          dataType: "json",
          // JSON.stringify()用于从一个对象解析出字符串
          data:JSON.stringify({bk_loc: AI.black_loc})
                    }).done(function ( data ) {
                            alert("ajax callback response:"+JSON.stringify(data));
        })

        
        $.ajax({
          type: "POST",
          url: "http://127.0.0.1:8000/",
          crossDomain:true, 
          dataType: "json",
          // JSON.stringify()用于从一个对象解析出字符串
          data:JSON.stringify({bk_loc: AI.black_loc}),
          success:function(data) { 
                $.ajax({
                  type: "POST",
                  url: "http://127.0.0.1:8000",
                  crossDomain:true, 
                  success:function(data){
                    ....
                  },
                  error:function(){
                    ...
                  }
                })
         },
         error:function(){
            console.log('error')
         }
        })
        function callback(v) {
            if (v == 'replay')
                Game.restart();
            else
                Game.stop();
        }

        $.prompt(text, {
            buttons : {
                重新开始 : 'replay',
                退出 : 'quit',
            },
            callback : callback,
        });
    },
    // 移一步
    step : function() {
        this.red_king_sprite.set('visible', false);
        this.black_king_sprite.set('visible', false);

       if (this.cur_camp == CAMP_RED) {
            this.player_black.stop();
            this.player_red.run();
        }
        else {
            this.player_red.stop();
            this.player_black.run();
        }      
        if(this.red_Campstep + this.black_Camstep > 150){
            this.draw_chess();
            this.red_Campstep = 0 
            this.black_Camstep = 0
        }   
    },

    set_Redscore : function (s) {
        this.scoreLabel_red.set('string',String(s))
    },

    set_Blackscore : function (s) {
        this.scoreLabel_black.set('string',String(s))
    },

    // 设置玩家
    set_player : function(camp, name, player_class) {
        if (camp == CAMP_RED)
            this.player_red = player_class.create(name, camp);
        else
            this.player_black = player_class.create(name, camp);
    },

    // 移动棋子
    move_chess : function(x, y, tx, ty, move_info) {
        // 移动棋子
        if (Board.move_chess(x, y, tx, ty, move_info) && !this.win_game) {

            // 添加对战手数
           if (this.cur_camp == CAMP_RED) {
                this.red_Campstep = this.red_Campstep + 1
                this.set_Redscore(String(this.red_Campstep))
            }
            else {
                this.black_Camstep = this.black_Camstep + 1
                this.set_Blackscore(String(this.black_Camstep))
            }  

            // 切换阵营
            this.cur_camp = -this.cur_camp;

            // 移动一步
            setTimeout("Game.step()", 300);
        }
    },

    // 检查是否被将军
    check_king : function() {
        var move_list = MoveGenerator.create_possible_moves(-this.cur_camp);
        var chesses = MoveGenerator.get_chesses()
        if (this.check_chessState(chesses)) {
            this.opp_win(-this.cur_camp)
        }
        var king = R_KING * this.cur_camp;
        for (var i = 0; i < move_list.length; ++i) {
            var move = move_list[i];
            var tc = MoveGenerator.get_chess(move.tx, move.ty);
            if (tc == king) {
                if(this.first_king_chess == 0){   //第一次将军
					this.king_chess = chesses[move.fy][move.fx]  //保存上一次将军棋子
					this.king_chess_step = this.red_Campstep     //保存上一次将军手数
					this.king_count = 1                          //将军次数累计
					this.first_king_chess = 1
					if (this.cur_camp == CAMP_RED)
						this.red_king_sprite.set('visible', true);
					else
						this.black_king_sprite.set('visible', true);
					//if(this.king_count > 2) {
						//this.win(this.cur_camp == CAMP_RED?CAMP_BLACK:CAMP_RED,true);
				}
				else if(this.king_chess_step == (this.red_Campstep - 1) && this.king_chess ==chesses[move.fy][move.fx]){  //同一棋子且连续手数将军
					this.king_count = this.king_count + 1    //将军次数累加
					this.king_chess = chesses[move.fy][move.fx]
					this.king_chess_step = this.red_Campstep
					if (this.cur_camp == CAMP_RED)
						this.red_king_sprite.set('visible', true);
					else
						this.black_king_sprite.set('visible', true);
					if(this.king_count > 2) {
						this.win(this.cur_camp == CAMP_BLACK?CAMP_BLACK:CAMP_RED,true);
					}
				}
				else{
					this.king_chess = chesses[move.fy][move.fx]
					this.king_chess_step = this.red_Campstep
					if (this.cur_camp == CAMP_RED)
						this.red_king_sprite.set('visible', true);
					else
						this.black_king_sprite.set('visible', true);
					this.king_count = 1     //将军次数清零
				}					
			}
				
		}
    },

    // 对将
    opp_win : function(camp) {
        var text;
        if (camp == CAMP_RED)
            text = '红方对将，黑方胜利';
        else
            text = '黑方对将，红方胜利';
        this.win_game = true
        // 回调
        function callback(v) {
            if (v == 'replay')
                Game.restart();
            else
                Game.stop();
        }

        $.prompt(text, {
            buttons : {
                重新开始 : 'replay',
                退出 : 'quit',
            },
            callback : callback,
        });
    },
    // 检测对将
    check_chessState: function (chesses) {
        red_king = []
        black_king = []
        for (var y = 0; y < 10; ++y) {
            for (var x = 0; x < 9; ++x) {
                var chess = chesses[y][x];
                if (chess == 5){
                    red_king = [y,x]
                }
                if (chess == -5){
                    black_king = [y,x]
                }
            }
        }
        // 判断king是否在同一列
        if (red_king[1] == black_king[1]) {
            for(var y = black_king[0]+1; y < red_king[0]; ++y) {
                var chess = chesses[y][black_king[1]]
                if (chess != 0) {
                    return false
                }
			}	
            return true
        }
        return false;  
    },
    // 监听：棋子被杀掉
    on_chess_killed: function(chess) {
        if (chess.name == 'R_KING')
            this.win(CAMP_BLACK);
        else if (chess.name == 'B_KING')
            this.win(CAMP_RED);
    },
}

