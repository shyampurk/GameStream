var Cloudant = require('cloudant');


// Define url parameter that you obtained while creating the cloudantdb service
var url = "https://ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix:138917f496921df5a30bf85f79d9d37315df23ace5f456a48b47998b4f8ca23e@ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix.cloudant.com";
var cloudant = Cloudant(url);
// selecting the database
var database_name = "gameplaystats"
// creating the db client
var db = cloudant.db.use(database_name);

function main(params) {
    
    delete params.message; // deleting unnecessary parameters from the input message
    delete params.messagetype; // deleting unnecessary parameters from the input message
    // creating a new promise 
    return new Promise(function(resolve,reject){
        // Getting all the docs stored in the cloudant db. 
        db.list({"include_docs":true},function(err, body) {
            // Storing the team name 
            var team = params.team;
            delete params.team; //deleting unnecessary parameters from the input message
            // checking if the db call returned error or success
            if (!err) 
            {
                body.rows.forEach(function(doc) {
                // checking for the docs that are only for the team that we got as input 
                if (team == doc.doc.Team){
                // storing it the docs   
                params[doc.key] = doc.doc;
                }
                
                });
            }
            console.log(params);
            // Inititalizing the variables
            var Maxscore = 0;
            var PlayedGames = 0;
            var Winpercentage = 0;
            var win = 0;
            var loss = 0;
            // Doing calculation to get the win percentage,playedgames,maxscore,numberof wins/losses.
            for (val in params){
                if (Maxscore<params[val].Totalscore){
                    Maxscore = params[val].Totalscore // calculating the maximum score
                }
                
                PlayedGames += params[val].Game;
                win += params[val].Win; // calculating the number of wins
                loss += params[val].Loss; // calculating the number of losses
                delete params[val]; 
            }
            temp = (win/PlayedGames)
            // calculating the win percentage
            Winpercentage = (temp*(100));
            // updating the params with the calculated values
            params.Maxscore = Maxscore;
            params.Winpercentage = Winpercentage;
            params.PlayedGames = PlayedGames;
            params.Win = win;
            params.Loss = loss;
            params.Team = team;
            params.messagetype = "resp";
            // resoving the promise
            resolve(params);   
        });
    });
        
    return Promise;
}
