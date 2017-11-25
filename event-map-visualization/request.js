function requestFromFinnair(destination, date, firstname, lastname, headerlink, headerimg, title, description, destination) {
	var url = 'https://offer-junction.ecom.finnair.com/api/offerList?adults=1&locale=en&departureLocationCode=HEL&destinationLocationCode='+destination+'&departureDate='+date;
	$.ajax({
	  url: url,
	  success: function (suc) {
	  	console.log('suc', suc);
	  	var price = '€' + suc.offers[0].totalPrice;
	  	clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price);
	  }
	});
}


function clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price) {
	var template = $('#template').html();
	Mustache.parse(template);
	var rendered = Mustache.render(template, {
		firstname: "Liang",
		lastname: "Guo",
		headerlink: "http://google.fi",
		headerimg: "https://s1.ticketm.net/dam/a/e00/87b95498-5258-4ee6-850d-ade6bc44ae00_565471_RETINA_PORTRAIT_3_2.jpg",
		title: "hello, check out this event",
		description: "this event you might interesting, we want to offer this event to you",
		destination: 'Barcelona',
		price: '€199'
	});
	
	var w = window.open();
	var html = $("#toNewWindow").html(rendered);
	$(w.document.body).html(html);
}