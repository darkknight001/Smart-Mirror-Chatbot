//aiclient.js

Module.register("aiclient",{

	// Default module config.
	defaults: {
		animationSpeed: 0.5 * 1000,
		iconTable: {
			"clear-day": "wi-day-sunny",
			"partly-cloudy-day": "wi-day-cloudy",
			"cloudy": "wi-cloudy",
			"wind": "wi-cloudy-windy",
			"rain": "wi-rain",
			"thunderstorm": "wi-thunderstorm",
			"snow": "wi-snow",
			"fog": "wi-fog",
			"clear-night": "wi-night-clear",
			"partly-cloudy-night": "wi-night-cloudy",
			"hail": "wi-rain",
			"tornado": "wi-rain"
		}
	},

	// Define required translations.
	getTranslations: function() {
		// The translations for the defaut modules are defined in the core translation files.
		// Therefor we can just return false. Otherwise we should have returned a dictionairy.
		// If you're trying to build your own module including translations, check out the documentation.
		return false;
	},

	// Define required scripts.
	getStyles: function() {
		return ["weather-icons.css", "currentweather.css"];
	},

	// Define start sequence.
	start: function() {
		Log.log("Starting module: " + this.name);

		this.sendSocketNotification("INITIALIZE", {})
		
	},

	// Override dom generator.
	getDom: function() {
		var div = document.createElement("div");
		var span = document.createElement("span");
	//	div.style.display="flex";
	//	div.style.alignContent="center";
	//	div.style.alignItems="center";
		span.innerHTML="";
	//	span.style.display="flex";
	//	span.style.alignContent="center";
	//	span.style.alignItems="center";
		var wrapper = document.createElement("span");
	//	wrapper.style.display="flex";
	//	wrapper.style.alignContent="center";
	//	wrapper.style.alignItems="center";
		div.appendChild(span);
		div.appendChild(wrapper); 
		
		switch(this.current_selection) {
			case "STATEMENT":
				wrapper.innerHTML = this.text;
				console.log(this.text);
				wrapper.className = "medium bright";
				break
			case "IMAGE":
				wrapper.innerHTML = "<img src=\"" + this.imageURL + "\" style=\"border:1px solid black;max-width:100%;\">"
			case "DATA":
				span.innerHTML="";
				var imag = document.createElement("img");
				imag.style.height="800px";
				imag.src=this.file("./photos/"+this.text+".jpg");
				wrapper.appendChild(imag);
				break
			case "INFO":
				span.innerHTML="";
				var imag = document.createElement("img");
				imag.style.height="800px";
				imag.src=this.file("./photos/faculty/"+this.text+".jpg");
				wrapper.appendChild(imag);
				break
			case "FACULTY":
				span.innerHTML="";
				var imag = document.createElement("img");
				imag.style.height="550px";
				imag.src=this.file("./photos/Time_table/Faculty_time_table/"+ this.text +".png");
				wrapper.appendChild(imag);
				break
			case "CLASS":
				span.innerHTML="";
				var imag = document.createElement("img");
				imag.style.height="600px";
				imag.src=this.file("./photos/Time_table/students_time_table/"+ this.text +".png");
				wrapper.appendChild(imag);
				break
				
//				if(this.text=="ece a third year"){
//					var imag = document.createElement("img");
//					imag.style.height="550px";
//					imag.src=this.file("./photos/ece.png")//"https://drive.google.com/file/d/1DoMrowKZWqCCsy-lheTrNRmD4dlPzmzf/view";
//					wrapper.appendChild(imag);
//				}else if(this.text=="Niranjan Bhattacharyya"){
//					var imag = document.createElement("img");
//					imag.style.height="700px";
//					imag.src=this.file("./photos/HOD_ECE.jpg")//"https://drive.google.com/file/d/1DoMrowKZWqCCsy-lheTrNRmD4dlPzmzf/view";
//					wrapper.appendChild(imag);
//				}else if(this.text=="ece"){
//					var imag = document.createElement("img");
//					imag.style.height="700px";
//					imag.src=this.file("./photos/ECE_department.jpg")//"https://drive.google.com/file/d/1DoMrowKZWqCCsy-lheTrNRmD4dlPzmzf/view";
//					wrapper.appendChild(imag);
//				}else if(this.text=="risheek kumar mishra"){
//					var imag = document.createElement("img");
//					imag.style.height="490px";
//					imag.src=this.file("./photos/risheekSir.png")//"https://drive.google.com/file/d/1DoMrowKZWqCCsy-lheTrNRmD4dlPzmzf/view";
//					wrapper.appendChild(imag);
//				}
//				else if(this.text=="contacts"){
//					var imag = document.createElement("img");
//					imag.style.height="600px";
//					imag.src=this.file("./photos/contacts.jpg")//"https://drive.google.com/file/d/1DoMrowKZWqCCsy-lheTrNRmD4dlPzmzf/view";
//					wrapper.appendChild(imag);
//				}
				
//				break

			case "WEATHER":
				var small = document.createElement("div");
				small.className = "normal medium";
				small.style.margin = "10px 0px"

				var windIcon = document.createElement("span");
				windIcon.className = "wi wi-strong-wind dimmed";
				small.appendChild(windIcon);

				var windSpeed = document.createElement("span");
				windSpeed.innerHTML = " " + this.weather.windSpeed + " mph" //this.windSpeed
				small.appendChild(windSpeed);

				var spacer = document.createElement("span");
				spacer.innerHTML = "&nbsp;";
				small.appendChild(spacer);

				var sunriseSunsetIcon = document.createElement("span"); 
				if (this.weather.hour >= 4 && this.weather.hour < 10) {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-sunrise"; //this.sunriseSunsetIcon
				} else if (this.weather.hour >=10 && this.weather.hour < 18) {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-day-sunny"; //this.sunriseSunsetIcon
				} else if (this.weather.hour >=18 && this.weather.hour < 22) {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-sunset"; //this.sunriseSunsetIcon
				} else {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-night-clear"; //this.sunriseSunsetIcon
				}
				small.appendChild(sunriseSunsetIcon);

				var sunriseSunsetTime = document.createElement("span");
				sunriseSunsetTime.innerHTML = " " +  "Now" //this.sunriseSunsetTime;
				small.appendChild(sunriseSunsetTime);

				var large = document.createElement("div");
				large.className = "xlarge light";

				var weatherIcon = document.createElement("span");
				weatherIcon.className = "wi weathericon " + this.config.iconTable[this.weather.icon] //this.weatherType;
				large.appendChild(weatherIcon);

				var temperature = document.createElement("span");
				temperature.className = "bright";
				temperature.innerHTML = " " + this.weather.temperature + "&deg;"; //this.temperature
				large.appendChild(temperature);

				large.style.margin = "20px 0px"

				wrapper.appendChild(small);
				wrapper.appendChild(large);
				break;
			case "LISTENING":
				var icon = document.createElement("span");
				icon.innerHTML = "<img src=\"" + this.file("mic.gif") + "\" style=\"width:50px;height:65px;\">"
				icon.style.margin = "10px 0px"
				wrapper.appendChild(icon);

				var title = document.createElement("span");
				title.className = "xlarge light";
				title.innerHTML = "Listening";
				wrapper.appendChild(title);
				
				//wrapper.innerHTML = "<img src=\"" + this.file("face.gif") + "\" style=\"border:1px solid black;max-width:100%;\">"
				break
			case "HOLIDAYS":
				var title = document.createElement('div')
				title.innerHTML = this.holiday.localName
				title.className = "large bright";
				title.style.margin = "10px"

				var date = new Date(this.holiday.date.year, this.holiday.date.month - 1, this.holiday.date.month)

				var subtitle = document.createElement('div')
				subtitle.innerHTML = date.toDateString()
				subtitle.className = "medium bright";
				subtitle.style.margin = "10px" 

				wrapper.appendChild(title)
				wrapper.appendChild(subtitle)
				break
			case "NEWS":
				var title = document.createElement('div')
				title.innerHTML = "News"
				title.className = "medium bright";
				title.style.margin = "20px"

				wrapper.appendChild(title)

				var table = document.createElement("table");
				table.className = "medium";

				for (var a in this.articles) {
					var article = this.articles[a];

					var row = document.createElement("tr");
					table.appendChild(row);

					var iconCell = document.createElement("td");
					iconCell.className = "bright weather-icon";
					row.appendChild(iconCell);

					var icon = document.createElement("span");
					icon.innerHTML = "<img src=\"" + this.file("newspaper_icon.png") + "\" style=\"width:30px;height:30px;\">"
					icon.style.margin = "10px 10px"
					iconCell.appendChild(icon);

					var title = document.createElement("span");
					title.className = "day";
					title.innerHTML = article;
					iconCell.appendChild(title);
				}

				wrapper.appendChild(table)
				break
			default:
				break
		}
		return div
	},

	// Override socket notification handler.
	socketNotificationReceived: function(notification, payload) {
		console.log("module received: " + notification)
		var self = this

		if (notification == "STATEMENT"){
			this.current_selection = "STATEMENT"
			this.text = payload.text
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "IMAGE") {
			this.imageURL = payload.imageurl
			this.current_selection = "IMAGE"
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "WEATHER") {
			this.current_selection = "WEATHER"
			this.weather = payload
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "CLEAR") {
			this.current_selection = ""
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "LISTENING") {
			this.current_selection = "LISTENING"
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "NEWS") {
			this.current_selection = "NEWS"
			this.articles = payload.articles
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "HOLIDAYS") {
			this.current_selection = "HOLIDAYS"
			this.holiday = payload.holiday
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "DATA") {
			this.current_selection = "DATA"
			this.text = payload.text
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "INFO") {
			this.current_selection = "INFO"
			this.text = payload.text
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "FACULTY") {
			this.current_selection = "FACULTY"
			this.text = payload.text
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "CLASS") {
			this.current_selection = "CLASS"
			this.text = payload.text
			this.updateDom(this.config.animationSpeed);
		}
	}
});
