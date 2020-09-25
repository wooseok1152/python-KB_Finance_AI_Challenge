const port = process.env.PORT || 3000,
    fs = require('fs'),
    express = require('express'),
    app = express(),
    server = require('http').createServer(app),
    // io = require('socket.io')(server),
    bodyParser = require('body-parser'),
    session = require("express-session")({
        secret: "my-secret",
        resave: true,
        saveUninitialized: true
    }),
    {PythonShell} = require('python-shell');

let options = {
    encoding: 'utf8',
    pythonPath: 'C:\\Users\\KSC\\AppData\\Local\\Microsoft\\WindowsApps\\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\\python.exe',
    scriptPath: "./",
    args: ["1"]
};

app.use(session);
app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));

app.get("/", (req, res)=>{
    res.render('index.ejs');
});

app.post("/", (req, res)=>{
    options.args = [req.body.userID];
    PythonShell.run("chatbotDeployVersion.py", options, function(err, data) {
        if (err) throw err;
        else {
            res.render("result.ejs", {
                resultData: data
            });
        }
    });
});

server.listen(port);
// Put a friendly message on the terminal
console.log('Server running at http://127.0.0.1:' + port + '/');
