


$(document).ready(function(){
	
	//Animates pressed key's block animatelettercode from http://buildinternet.com/2009/05/make-an-animated-alphabet-using-keypress-events-in-jquery/
	function animateLetter(letter){
		$(".letter-" + letter).stop(true,false).animate({top:'190px'},{easing: 'easeInBack', duration:700}).animate({opacity: 1.0}, 300).animate({top:'0px'},{duration:500});
		$
	
	}
	
	$(document).keypress(function(e){
		
		if (e.which >= 97 && e.which <= 122) {
			animateLetter(String.fromCharCode(e.which));
		}
		else if(e.which == 32){
			$(".space-alert").show()
				.animate({opacity: 1.0}, 400)
				.fadeOut(400);
		}
		
	});
	
});
