Array.prototype.randomElement = function () {
    return this[Math.floor(Math.random() * this.length)]    
}

function requestFromFinnair(destination, date, firstname, lastname, headerlink, headerimg, title, description) {
    var url = 'https://offer-junction.ecom.finnair.com/api/offerList?adults=1&locale=en&departureLocationCode=HEL&destinationLocationCode='+destination+'&departureDate='+date;
    // $.getJSON(url, function(data){
    // 	console.log('get data', data);

    // })
    // $.ajax({
    // 	type: 'GET',
    // 	url: url,
    // 	dataType: 'json',
    // 	success: function (data) {
    // 	    console.log(data);
    // 	    var price = '€' + data.totalPrice;
    // 	    clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price);
    // 	}	    
    // });    
	// $.ajax({
	//     url: url,	    
	//     success: function (suc) {
	//   	var price = '€' + suc.offers[0].totalPrice;
	//   	clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price);
	//     },
	//     error: function (code) {
	// 	var price = '€299';
	// 	clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price);
	// 	// console.log('code', code);
	//     }
    // });
    var prices = [199, 299, 287, 336, 138, 399];
    var price = "€" + prices.randomElement();
    clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price);
}


function clicksend(firstname, lastname, headerlink, headerimg, title, description, destination, price) {
	var template = $('#template').html();
	Mustache.parse(template);
	var rendered = Mustache.render(template, {
		firstname: firstname,
		lastname: lastname,
		headerlink: headerlink,
		headerimg: headerimg,
		title: title,
		description: description,
		destination: destination,
		price: price
	});
	
    var w = window.open();
        var html = $("#toNewWindow").html(rendered);
    $(w.document.body).html(html);
    window.location.reload();
}
