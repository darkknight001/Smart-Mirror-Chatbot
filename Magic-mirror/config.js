/* Magic Mirror Config Sample
/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 */

var config = {
	port: 8080,

	language: 'en',
	timeFormat: 12,
	units: 'metric',

	modules: [
    {
        module: 'aiclient',
        position: 'middle_center' // This can be any of the regions.
    },
    {
    	module: 'aiclientdebugger',
    	position: 'bottom_right'
	},
	
		// {
		// 	module: "alert",
		// },
	{
		module: "updatenotification",
		position: "top_bar"
	},
	{
		module: "clock",
		position: "top_left"
	},
	{
		module: "calendar",
		header: "Indian Holidays",
		position: "top_left",
		config: {
			calendars: [
					{
						symbol: "calendar-check",
						url: "webcal://www.calendarlabs.com/ical-calendar/ics/33/India_Holidays.ics",
						color: '#ffc300'	
					}
				   ]
			}
	},
	// {
	// 	module: "compliments",
	// 	position: "lower_third"
	// },
	{
		module: "currentweather",
		position: "top_right",
		degreeLabel: "true",
			config: {
				location: "National Capital Territory of Delhi ",
				locationID: "1273293",  //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
				appid: "a6ca8aac3488196c4d79075708e299f9"
			}
		},
	//	{
	//		module: "weatherforecast",
	//		position: "top_right",
	//		header: "Weather Forecast",
	//		config: {
	//			location: "Kolkata",
	//			locationID: "1275004", //ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
	//			appid: "a6ca8aac3488196c4d79075708e299f9"
	//		}
	//	},
		{
			module: "newsfeed",
			position: "bottom_bar",
			config: {
				feeds: [
					{
						title: "News, Electronics",
						url: "https://www.realwire.com/rss/?id=342&row=&view=Synopsis"
					}
				],
				showSourceTitle: true,
				showPublishDate: false,
				broadcastNewsFeeds: true,
				broadcastNewsUpdates: true
			}
		},
	
	]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== 'undefined') {module.exports = config;}
