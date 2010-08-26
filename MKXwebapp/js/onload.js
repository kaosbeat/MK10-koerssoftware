  function initialize() {
    var latlng = new google.maps.LatLng({{latitude}}, {{longitude}});
    // var latlng = new google.maps.LatLng(51.23057,3.18637);
    var myOptions = {
      zoom: 18,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
      var marker = new google.maps.Marker({
      position: latlng, 
      map: map, 
      title:'{{device_label}}'
      
  }); 
   var rvvPoly = [
    {% for pos in positions%}
      new google.maps.LatLng({{pos.latitude}}, {{pos.longitude}}),
	{% endfor %}
    ]
  
     function updateRealPos ()  {
     
      $.getJSON('http://sporzakoers.appspot.com/realPos', function(json) {
                $('#longitude').html("longitude: " + json.longitude+"<br>")
		$('#latitude').html("latitude: " + json.latitude);
		$('#speed').html("speed: " + json.speed + " km/h" );
		$('#heading').html("heading: " + json.heading + ' graden');
		$('#heading').html("climbrate: " + json.climbrate + "&#37;");
 
		var newpos = new google.maps.LatLng(json.latitude,json.longitude);
		marker.setPosition(newpos);
		map.setCenter(newpos);
     });
     setTimeout(updateRealPos, 2499); 
  }
   updateRealPos();
   setTimeout(updateRealPos, 2499); 
 
 
  
   
    var rvvPath = new google.maps.Polyline({
      path: rvvCoordinates,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
 
   rvvPath.setMap(map);
 
 
 
 
    var rvvPoly = new google.maps.Polyline({
      path: rvvPoly,
      strokeColor: "#00FF00",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });
 
   rvvPoly.setMap(map);
   updateElevation();
   
   
 
////########### trying elevations her #######
elevationService = new google.maps.ElevationService();
 
  // Trigger the elevation query for point to point
  // or submit a directions request for the path between points
  function updateElevation() {
        elevationService.getElevationAlongPath({
          path: rvvCoordinates,
          samples: 256
        }, writeResults);
      }
function writeResults(results, status) {  
	if (status == google.maps.ElevationStatus.OK) {
		var elevationdata = new Array()
		elevations = results;
		 for (var i = 0; i < results.length; i++) {
			elevationdata[i] = elevations[i].elevation;
			document.write('<li>' + elevationdata[i]  + '</li>');
			}
		}
    }
}
  