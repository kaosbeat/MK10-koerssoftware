$(document).ready(function(){
        
        

});


function centerTextAndScale(divID){
      var voornaamwidth = $("#Voornaam").width();  
     //alert(voornaamwidth);
     var windowwidth = $(document).width();
     //voornaamtextpx = 50*(windowwidth/voornaamwidth);
     var currentFontSize = $("#Voornaam").css('font-size');
     var currentFontSizeNum = parseFloat(currentFontSize, 10);
     var newFontSize = currentFontSizeNum*(windowwidth/voornaamwidth)*0.6;
     //alert(newFontSize);
     $('#Voornaam').css('font-size', newFontSize);
     var voornaamwidth = $("#Voornaam").width();
     var offset = (windowwidth - voornaamwidth)/2+"px";
     //alert(voornaamwidth);
     //alert(offset);
     $("#Voornaam").css("left", offset);
     
     //$("Voornaam").css("font-size", voornaamtextpx);    
    
}
