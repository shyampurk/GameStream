var Cloudant = require('cloudant');

// Refer step1 under Openwhisk code in README file in repo root folder.
var url = "https://ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix:138917f496921df5a30bf85f79d9d37315df23ace5f456a48b47998b4f8ca23e@ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix.cloudant.com";
var cloudant = Cloudant(url);
var database_name = "gameplaystats"
var db = cloudant.db.use(database_name);

function main(params) {
    
    delete params.message;
    delete params.messagetype;
    return new Promise(function(resolve,reject){
        // Getting the docs stored in the cloudant db. 
        db.list({"include_docs":true},function(err, body) {
            
            var team = params.team;
            delete params.team;

            if (!err) 
            {
                body.rows.forEach(function(doc) {
                if (team == doc.doc.Team){
                params[doc.key] = doc.doc;
                }
                
                });
            }
            console.log(params);
            var Maxscore = 0;
            var PlayedGames = 0;
            var WinLosspercentage = 0;
            var win = 0;
            var loss = 0;
            // Doing calculation to get the winloss percentage,playedgames,maxscore,numberof wins/losses.
            for (val in params){
                if (Maxscore<params[val].Totalscore){
                    Maxscore = params[val].Totalscore
                }
                
                PlayedGames += params[val].Game;
                win += params[val].Win;
                loss += params[val].Loss;
                delete params[val]; 
            }
            temp = (win/PlayedGames)

            WinLosspercentage = (temp*(100));
            params.Maxscore = Maxscore;
            params.WinLosspercentage = WinLosspercentage;
            params.PlayedGames = PlayedGames;
            params.Win = win;
            params.Loss = loss;
            params.Team = team;
            params.messagetype = "resp";
            resolve(params);   
        });
    });
        
    return Promise;
}
