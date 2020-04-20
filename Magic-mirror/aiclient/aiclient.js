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
				wrapper.innerHTML = "<img src=\"" + this.imageURL + "\" style=\"border:1px solid black;width:1600px;height:900px;\">"
				break
			
			case "NOTICE":
				var title = document.createElement('div')
				title.innerHTML = "NOTICES"
				title.style.fontSize = "50px"
				title.style.color = "#cccccc"
				title.style.margin = "30px"

				wrapper.appendChild(title)

				var table1 = document.createElement("table");
				table1.className = "medium";
				table1.style.border = "1px solid white"

				var t_row = document.createElement("tr");
				// t_row.style.padding = "5 px"	
				table1.appendChild(t_row);

				var s = document.createElement("th");
				s.style.color= "#f5c842"
				s.innerHTML = "NOTICE NO.";
				s.style.padding = "15px"
				s.style.borderTop = "1px solid white" 
				s.style.borderBottom = "1px solid white"
				t_row.appendChild(s);

				var d = document.createElement("th");
				d.style.color= "#f5c842"
				d.innerHTML = "DATE";
				//d.style.padding = "30px"
				d.style.borderBottom = "1px solid white" 
				d.style.borderTop = "1px solid white"
				t_row.appendChild(d);

				var des = document.createElement("th");
				des.style.color= "#f5c842"
				des.innerHTML = "DESCRIPTION"
				//des.style.padding = "30px"
				des.style.borderBottom = "1px solid white" 
				des.style.borderTop = "1px solid white"
				t_row.appendChild(des);

				for (var n in this.notices) {
					var notices = this.notices[n];

					var row = document.createElement("tr");
					// row.style.padding = "5 px"
					table1.appendChild(row);

					var s_no = document.createElement("td");
					s_no.className = "light";
					s_no.innerHTML = "BPIT/ECE/" + notices.serial;
					s_no.style.padding = "8px"
					s_no.style.borderTop = "1px solid white" 
					s_no.style.borderBottom = "1px solid white" 
					row.appendChild(s_no);

					var n_date = document.createElement("td");
					n_date.className = "light";
					n_date.innerHTML = notices.date;
					//n_date.style.padding = "30px"
					n_date.style.borderTop = "1px solid white" 
					n_date.style.borderBottom = "1px solid white" 
					row.appendChild(n_date);

					var desc = document.createElement("td");
					desc.className = "light";
					//desc.style.margin = "15px"
					desc.innerHTML = notices.description
					desc.style.borderTop = "1px solid white" 
					desc.style.borderBottom = "1px solid white" 
					row.appendChild(desc);
					
				}
				
				wrapper.appendChild(table1)
				break
				
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
		} else if (notification == "NOTICE") {
			this.current_selection = "NOTICE"
			this.notices = payload.notices
			this.updateDom(this.config.animationSpeed);
		}
	}
});
