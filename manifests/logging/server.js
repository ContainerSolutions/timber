var http = require('http');

var handleRequest = function(request, response) {
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.end("Hello World!\n");
};
var www = http.createServer(handleRequest);
www.listen(8080);

console.log("Server is running at http://127.0.0.1:8080");
