

var units = "metric";

//$("#city").html('seoul' + ", " + 'south Korea')

//Open weather API request
$.getJSON('http://api.openweathermap.org/data/2.5/weather?q=' +'seoul' + '&units=' + units + '&APPID=e95d958a11128b11ad3eb0fa101dae38', function(json){
console.log(json);
$("#city").html(json.name+','+json.sys.country);
$("#temperature-celcius").html(json.main.temp + ' C&deg');
$("#temperature-farenheit").html((json.main.temp * 1,8 + 32) + ' F&deg');
$("#humidity").html(json.main.humidity + ' %');
$("#overall").html(json.weather[0].main);
$("#icon").html('<img src="http://openweathermap.org/img/w/' + json.weather[0].icon + '.png"</img>');
});
