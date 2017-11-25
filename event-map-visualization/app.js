$(document).ready(function(){
    $('#modal').modal();
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
	// console.log(city2loc);
	$.getJSON('music200_by_city.json', function(groups){
	    $.each(groups, function(city_index, group){
		// console.log(city_index);
		// console.log(city2loc[city]);
		// console.log(group);
		var city = group.city;
		var num_users = group.num_users;
		var events = group.events;
		
		var loc = city2loc[city];
		var circle = L.circle([loc['lat'], loc['lon']], {
		    color: 'red',
		    fillColor: '#f03',
		    fillOpacity: 0.5,
		    radius: 1750 * Math.sqrt(num_users)
		}).addTo(mymap);

		// events = _.sortBy(events, function(e){ return -e['users'].length; });
		var top_events = _.take(events, num_events_to_show);
		var html = '';
		html += '<ul class="collapsible popout" data-collapsible="accordion">';
		$.each(top_events, function(event_index, e){
		    // console.log(event_index);
		    html += '<li>';
		    html += '<div class="collapsible-header">';  // <i class="material-icons">subtitles</i>
		    html += e.name;
		    // html += '<span class="right grey-text lighten-3" style="display:block">' + e.date + '</span>';
		    html += '</div>';
		    html += '<div class="collapsible-body">';
		    html += '<p class="valign-wrapper"><i class="small material-icons">equalizer</i><span>';
		    html += e.users.length + ' users might be interested';
		    html += '</span></p>'		    
		    html += '<p class="valign-wrapper"><i class="small material-icons">access_time</i><span>';
		    html += e.date;
		    html += '</span></p>';
		    html += '<p class="valign-wrapper"><i class="small material-icons">location_on</i><span>';
		    html += e.address;
		    html += '</span></p>';
		    html += '<button class="btn waves-effect waves-light offer-btn modal-trigger" style="width:50%" data-target="modal"';
		    html += (' data-city-index="' + city_index + '" ' + 'data-event-index="' + event_index + '"');
		    html += '>Make offers <i class="material-icons right">submit</i></button>';
		    html += '</div>';
		    html += '</li>';

		});
		html += '</ul>';
		circle.bindPopup(html).on('click',function(){
		    $('.collapsible').collapsible();
		    $('.offer-btn').on('click', function(){
			var cid = $(this).data('city-index');
			var eid = $(this).data('event-index');

			var event = groups[cid]['events'][eid];
			var m = $('#modal');
			m.find('.name').text(event.name);	
		
			var html = '<ul class="collection with-header">';
			html += '<li class="collection-header"><h5>They might be interested:</h5></li>';

			$.each(event.users, function(uid, users){
			    var name;
			    for(var k in users){
				name = k;
				// break;
			    }
			    // console.log(interests);
			    html += '<li class="collection-item"><div>';
			    html += name;
			    html += '<a href="#!" class="secondary-content send-offer" ';
			    html += 'data-city-index="' + cid + '" data-event-index="' + eid + '" ';
			    html += 'data-user-index="' + uid + '"';
			    html += '><i class="material-icons">send</i></a></div></li>';
			});
			html += '</ul>';
			// m.find('.body').
			m.find('.body').empty();
			m.find('.body').append(html);

			console.log(event);
			$('.send-offer').on('click', function(){
			    var cid = $(this).data('city-index');
			    var eid = $(this).data('event-index');
			    var uid = $(this).data('user-index');
			    var event = groups[cid]['events'][eid];
			    var date = event.date, city = event.city, event_link = event.url, image_link = event.image, event_title = event.name, desc = '', destination = event.city;
			    var user = event['users'][uid];
			    var name;
			    for(var k in user){
				name = k;
				// break;
			    }
			    console.log('name', name);
			    var firstname = name.split(' ')[0];
			    var lastname = name.split(' ')[1];
			    console.log(city, date, firstname, lastname,
					event_link, image_link, event_title,
					desc, destination);
			    requestFromFinnair(city, date, firstname, lastname, event_link, image_link, event_title, desc, destination);
			});
		    });
		});		
	    });
	});
    });


})
