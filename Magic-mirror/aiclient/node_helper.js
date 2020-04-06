//node_helper.js

var NodeHelper = require("node_helper");

module.exports = NodeHelper.create({
	// Subclass start method.
	start: function() {
		var self = this;
		var events = [];

		this.fetchers = [];

		console.log("Starting node helper for: " + this.name);

	    this.expressApp.get('/statement', function (req, res) {
	        text = req.query.text
	        self.sendSocketNotification("STATEMENT", {"text":text})
	        res.sendStatus(200);
	    });


		this.expressApp.get('/info', function (req, res) {
			text = req.query.text
			console.log("./photos/faculty/"+text+".jpg");
	        self.sendSocketNotification("INFO", {"text":text})
	        res.sendStatus(200);
   			
	    });
	    
   		this.expressApp.get('/data', function (req, res) {
			text = req.query.text
			console.log(text);
	        self.sendSocketNotification("DATA", {"text":text})
	        res.sendStatus(200);
   			
	    }); 
	
	   
		this.expressApp.get('/faculty', function (req, res) {
			text = req.query.text
			console.log(text);
	        self.sendSocketNotification("FACULTY", {"text":text})
	        res.sendStatus(200);
   			
	    });
	    
		this.expressApp.get('/class', function (req, res) {
			text = req.query.text
			console.log(text);
	        self.sendSocketNotification("CLASS", {"text":text})
	        res.sendStatus(200);
   			
	    });
	 

	    this.expressApp.get('/image', function (req, res) {
	    	imageUrl = req.query.text;
	        self.sendSocketNotification("IMAGE", {"image":imageUrl})
	        res.sendStatus(200);
   			
	    });

	    this.expressApp.post('/weather', function (req, res) {
	        var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
	        	self.sendSocketNotification("WEATHER", req.jsonBody)
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.get('/listening', function (req, res) {
	        self.sendSocketNotification("LISTENING", {})
	        res.sendStatus(200);
	    });

	    this.expressApp.post('/holidays', function (req, res) {
	        var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			holiday = req.jsonBody.holiday
	        	self.sendSocketNotification("HOLIDAYS", {"holiday": holiday})
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.post('/news', function (req, res) {
	       var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			articles = req.jsonBody.articles
	        	self.sendSocketNotification("NEWS", {"articles":articles})
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.get('/clear', function (req, res) {
	        text = req.query.text
	        self.sendSocketNotification("CLEAR", {})
	        res.sendStatus(200);
	    });




	},

	// Subclass socketNotificationReceived received.
	socketNotificationReceived: function(notification, payload) {
		console.log("helper received: " + notification)
	}
})