// PlayerAIEasy.js
// Created by MonkeyShen 2012
// 简单AI玩家 

var cocos = require('cocos2d');

var Player = BObject.extend({
    name : null,
    camp : null,

    init : function(name, camp) {
        this.name = name;
        this.camp = camp;
    },

    run : function() {
        AI.set_max_depth(3);
        // AI.play_a_chess(this.camp);
        AI.play_DQN_chess(this.camp);
        // 检查是否被将军
        Game.check_king();
    },

    stop : function() {
    },
});

exports.player = Player;
