var express = require("express"), 
    app = express(), 
    bodyParser = require('body-parser'), 
    path = require('path');
    fs = require('fs')
    port = process.env["PORT"] || 8080; 
 
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false })); 
const random = (min, max) => Math.floor(Math.random() * (max - min)) + min;

// Fetch recipes and send random to client
app.get("/index", function(req, res) { 
    // read json file
    fs.readFile('./oppskrifter.json', 'utf8', (err, jsonString) => {
        const recipes = JSON.parse(jsonString)
        var nrRecipes = Object.keys(recipes.recipes).length
        // send random recipe to client
        res.json(recipes.recipes[random(0, nrRecipes)])
        //res.sendStatus(200)
       // res.send(recipes.recipes[random(0, nrRecipes)]);
        //res.end();
    })
  
}).listen(port) 
console.log("listening to server on port:", port); 



