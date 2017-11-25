$(document).ready(function(){
    var mymap = L.map('mapid').setView([55.6791491, 12.8415219], 5);


    L.tileLayer(
	'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
	{
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	    maxZoom: 18,
	    id: 'mapbox.streets',
	    accessToken: 'pk.eyJ1IjoieGlhb2hhbjIwMTIiLCJhIjoiY2phZjkyd2QwMjE0NzMzbndnNjcwanhjYiJ9.hiLwYcuu_iWC7jOKawViwg'
	}).addTo(mymap);


    var num_events_to_show = 3;
    
    $.getJSON('city2loc.json', function(city2loc){
	console.log(city2loc);
	$.getJSON('events_grouped.json', function(all_rows){
	    $.each(all_rows, function(city, events){
		// console.log(city);
		// console.log(city2loc[city]);
		var loc = city2loc[city];
		var circle = L.circle([loc['lat'], loc['lon']], {
		    color: 'red',
		    fillColor: '#f03',
		    fillOpacity: 0.5,
		    radius: 500 * 50
		}).addTo(mymap);

		var top_events = _.take(events, num_events_to_show);
		var html = '<ul class="collapsible popout" data-collapsible="accordion">';
		$.each(top_events, function(i, e){
		    // console.log(e);
		    html += '<li>';
		    html += '<div class="collapsible-header">';  // <i class="material-icons">subtitles</i>
		    html += e.name;
		    html += '</div>';
		    html += '<div class="collapsible-body"><span>';
		    html += e.dates;
		    html += '</span></div>'
		    html += '</li>';
		});
		html += '</ul>';
		circle.bindPopup(html).on('click',function(e){
		    console.log('clicked');
		    $('.collapsible').collapsible();
		});
		
	    });
	});
    });
})
