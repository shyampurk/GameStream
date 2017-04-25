var Cloudant = require('cloudant');
var cloudant = Cloudant("https://ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix:138917f496921df5a30bf85f79d9d37315df23ace5f456a48b47998b4f8ca23e@ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix.cloudant.com");
var db = cloudant.db.use("gameplaystats");



function main(params) {
    
    delete params.message;
    delete params.messagetype;
    return new Promise(function(resolve,reject){
        db.list({"include_docs":true},function(err, body) {
            
            var team = params.team;
            delete params.team;

            if (!err) 
            {
                body.rows.forEach(function(doc) {
                // console.log(doc)
                // console.log("the key",doc.doc.Team)     
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
