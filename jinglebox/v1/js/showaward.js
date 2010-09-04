$(document).ready(function(){
        
        $("#avatar").hide();
        for (var i=1; i < 70; i++){
        showAward();
        window.setTimeout(500);
        showAvatar();
        window.setTimeout(100);
        flashAward();
        window.setTimeout(100);
        flashAvatar();
        } 

});
        
        
        function showAward(){
            $("#award").fadeIn('slow');
            $("#avatar").fadeOut('slow');
        }
        
        function showAvatar() {
            $("#avatar").fadeIn('slow');
            $("#award").fadeOut('slow');
        }
            
         function flashAward(){
            $("#award").show();
            $("#avatar").hide();
        }
        
        function flashAvatar() {
            $("#avatar").show();
            $("#award").hide();
        }
            
        
