export default (request) => {
	 // Required modules  
    const pubnub = require('pubnub'); // Pubnub for communication
    const db = require('kvstore'); // kvstore to store the data
    const xhr = require('xhr'); // xhr for REST calls
    
    // Authorization for the REST call
    // This Authorization we have to get it from the openwhisk cURL call
    // Edit the auth variable as per OpenWhisk credentials
    var auth = 'Basic OGI2ZWY0NDUtYTUxOS00Yzg5LWJlMjktZjk5ZGNiOGUxYmVkOmMxN2NNVDVKcllOVmJHWUd5VU9vTHRyVmpPVTBaaHhielQ3NnJXakNvY3pFeU1yMEhxVm9LelltUnZvOGtwNDI=';
        
    /*
    Name - broadcastMessage
    Description - Function used to send message to users via pubnub
    Parameters - pubchannel : Channel for braodcasting the message
                 message : Message to be sent to users

    */ 
    function broadcastMessage(pubchannel,message){

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
    
    // URL For the openwhisk
    // You will get it from the openwhisk
    // Edit url parameter as per OpenWhisk credentials
    const url = ('https://openwhisk.ng.bluemix.net/api/v1/namespaces/shyam@radiostud.io_M2M-Traffic-Control/actions/openwhisk_gamestats?blocking=true');

    // xhr POST call.  
    return xhr.fetch(url,http_options).then((url_fetched_data) =>{
        var fetched_message_body = JSON.parse(url_fetched_data.body);
        
        // Pubnub Publish channel on which we will broadcast the messages.
        var pubchannel = "Gameplaystats_resp";
        // Calling broadcastMessage function to send the message to UI
        broadcastMessage(pubchannel,fetched_message_body.response.result);
        return request;

    }).catch((err) => {
    console.log("THE API CALL ERROR --> ",err);
    return request.ok();
    });

    
     
};

    


