var port = 8000;
var http = require("http");
var fs = require('fs')
var server = http.createServer();
server.on('request', request);

//  开启监听，设置监听成功之后的处理函数
server.listen(3000, () => {
  console.log('server is listennig at port 3000');
});

function request(request, response) {
    var store = '';

    request.on('data', function(data) 
    {
        store += data;

    });
    request.on('end', function() 
    {  
        console.log(store);
        parse_JSON(store)
        response.setHeader("Content-Type", "text/json");
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.end(store)
    });
 } 

 function parse_JSON(store){
    var fs = require('fs');  
    console.log('------------------------')
    // parse用于从一个字符串中解析出json对象
    data_json = JSON.parse(store)
    data = data_json["bk_loc"]
    // lens = data.length
    // remove_ = lens % 4
    // data_r = data.slice(0,lens - remove_)
    for(var i = 0; i < data.length;i++){
        var temp = []
        if(data[i].length == undefined){
            temp.push(data[i])
        } else{
            temp.push(data[i].join(','))
        }
        write_txt(temp)
    }

 }







function write_txt(temp) {
    fs.appendFile('./ajax.txt',temp+'\n','utf8',function(err){  
        if(err)  
        {  
            console.log('write failed');  
        }else {
            console.log('write successed')
        }
    });  
}


// function write_txt(temp) {
//     fs.appendFile('./ajax.txt',JSON.stringify(temp)+',','utf8',function(err){  
//         if(err)  
//         {  
//             console.log('write failed');  
//         }else {
//             console.log('write successed')
//         }
//     });  
// }