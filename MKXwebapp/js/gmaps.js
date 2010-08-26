  function initialize() {
    //var latlng = new google.maps.LatLng({{latitude}}, {{longitude}});
    var latlng = new google.maps.LatLng(51.23057,3.18637);
    var myOptions = {
      zoom: 18,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    var marker = new google.maps.Marker({
      position: latlng, 
      map: map, 
      title:'{{device_label}}',
	  icon: '/img/KoerseurAnimatie10pt.gif'
	      //~ icon: '/img/bike.png'
    });
  /* var rvvPoly = [
    {% for pos in positions%}
      new google.maps.LatLng({{pos.latitude}}, {{pos.longitude}}),
	{% endfor %}
    ]
  */
  var polltime = 2499; 
     function updateRealPos ()  {
     
      $.getJSON('http://sporzakoers.appspot.com/realPos', function(json) {
                //~ $('#longitude').html("longitude: " + json.longitude+"<br>")
		//~ $('#latitude').html("latitude: " + json.latitude);
		$('#speed').html(Math.round(json.speed)+ " km/h" );
		$('#heading').html(json.heading + ' graden');
		$('#distance').html(json.distance + ' km');
		$('#climbrate').html(json.climbrate + "&#37;");
		polltime = parseInt( json.polltime); 
		var newpos = new google.maps.LatLng(json.latitude,json.longitude);
		marker.setPosition(newpos);
		map.panTo(newpos);
     });
     setTimeout(updateRealPos, polltime); 
  }
   updateRealPos();
   setTimeout(updateRealPos, polltime); 
 
 
  
   
    var rvvPath1 = new google.maps.Polyline({
      path: rvvCoordinates1,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
    rvvPath1.setMap(map);

    var rvvPath2 = new google.maps.Polyline({
      path: rvvCoordinates2,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
    rvvPath2.setMap(map);

    var rvvPath3 = new google.maps.Polyline({
      path: rvvCoordinates3,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
    rvvPath3.setMap(map);
 
    var rvvPoly = new google.maps.Polyline({
      path: rvvPoly,
      strokeColor: "#00FF00",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
 
   rvvPoly.setMap(map);
   updateElevation();
   
}