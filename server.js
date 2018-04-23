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
        console.log('hahah ')
        console.log(store);
        write_JSON(store)
        response.setHeader("Content-Type", "text/json");
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.end(store)
    });
 } 

 function write_JSON(store){
    var fs = require('fs');  
    data = store['bk_loc']
    lens = data.length
    remove_ = lens % 4
    data_r = data.slice(0,lens - remove_)
    fs.appendFile('./ajax.log',data_r,'utf8',function(err){  
        if(err)  
        {  
            console.log('write failed');  
        }else {
            console.log('write successed')
        }
    });  
 }