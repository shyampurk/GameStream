export default (request) => { 
    const pubnub = require('pubnub');
    const db = require('kvstore');
    const xhr = require('xhr');
    
    var auth = 'Basic OGI2ZWY0NDUtYTUxOS00Yzg5LWJlMjktZjk5ZGNiOGUxYmVkOmMxN2NNVDVKcllOVmJHWUd5VU9vTHRyVmpPVTBaaHhielQ3NnJXakNvY3pFeU1yMEhxVm9LelltUnZvOGtwNDI=';
    

    
    /*
    Name - broadcastMessage
    Description - Function used to send message to users via pubnub
    Parameters - pubchannel : Channel for braodcasting the message
                 message : Message to be sent to users

    */ 
    function broadcastMessage(pubchannel,message){

        // Broadcasting the Message to all the Users.
        console.log(message);
        pubnub.publish({
        channel   : pubchannel,
        message   : message,
        callback  : function(e) { 
            console.log( "SUCCESS!", e );
        },
        error     : function(e) { 
            console.log( "FAILED! RETRY PUBLISH!", e );
        }
    }); 

    }   





    // http options for the rest call.
    const http_options = {
        "method": "POST",
        
        "headers": {
                "Content-Type": "application/json",
                "Authorization":auth
    },
            "body":request.message
    };
    
    const url = ('https://openwhisk.ng.bluemix.net/api/v1/namespaces/shyam@radiostud.io_M2M-Traffic-Control/actions/dashdbaccessnode?blocking=true');

    return xhr.fetch(url,http_options).then((url_fetched_data) =>{
        var fetched_message_body = JSON.parse(url_fetched_data.body);
        // request.message = fetched_message_body.response.result;
        // Pubnub Publish channel on which we will broadcast the messages.
        var pubchannel = "Gameplaystats_resp";
        broadcastMessage(pubchannel,fetched_message_body.response.result);
        return request;

    }).catch((err) => {
    console.log("THE API CALL ERROR --> ",err);
    return request.ok();
    });

    

    // return request.ok();
   

     
};

    


