# Gamestream Event Handler for PubNub BLOCKS

# Pubnub BLOCK creation.

We have two BLOCKs in this application. One handles the stats  (Gameplaystats) and the other handles the live score (Gameplaylive).


## Gameplaystats BLOCK

Step 1 : Login to your Pubnub account with the valid credentials.

Step 2 : Click the "CREATE NEW APP" by giving a name to your APP.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb1.png)

Step 3 : Click on the newly created APP.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb2.png)
         
You can see the Demo keyset for the new application created.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb3.png)         

Step 4 : Click on the Demo keyset and click on the "BLOCKS" (on the left side).

Save the PubNub publish subscribe keys.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb4.png)


Step 5 : Create a new BLOCK by giving the name and description.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb5.png)


Step 6 : Create the Event Handler by clicking "CREATE" button at the bottom.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb6.png)

Step 7 : Give the Name of the Event handler, Channel to communicate with the BLOCK and the option of when BLOCK 
code should execute(Before Publish or Fire).

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb7.png)

Step 8 : Copy the BLOCK code in the text area from [here](https://github.com/shyampurk/Gamestream/blob/master/Block/main.js). Update the code to point to your OpenWhisk instance REST API (Refer sub section BLOCK config under main README ) and save it.

Step 9 : Click on the "Start block" button(top right) to start the BLOCK.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb8.png)

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/opb9.png)

Your BLOCK code is now running              


## Gameplaylive BLOCK

Follow the steps below the spawn the Gameplaylive BLOCK

Step 1 : Create another Block by giving the BLOCK name and description.

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/b2_1.png)

Step 2 : Create the Event Handler by clicking "CREATE" button at the bottom.
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/b2_2.png)
Step 3 : Give the Name of the Event handler, Channel to communicate with the "BLOCK" and the option of when block 
code should execute(Before Publish or Fire).

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/b2_3.png)

Step 4 : Click on the "Start block" button(top right) to start the block.
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/b2_4.png)

![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/Block/b2_5.png)

Your block code is now running.

Note that for this block we use the default BLOCK code that just passes the live score traffic through it. No additional processing is done here. 
