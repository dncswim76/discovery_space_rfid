$(document).ready(function() {
    $("#tag").focus();
    window.scrollTo(0,0);
	$(document).keypress(function(e) {
		if(e.which === 13) {
			$.getJSON($SCRIPT_ROOT + '/_validate_challenge_tag', {
				tag: $('input[name="tag"]').val(),
				game_id: $('input[name="game_id"]').val(),
                question_id: $('input[name="question_id"]').val()
			}, function(data) {
				if(data.valid === "true") {
					var html = '<h1>Correct! You scanned: <b><font color=blue>' + data.device__name + '</font></b></h1>';
                    html += '<h2>' + data.device__description + '</h2>';
                    if(data.media === "image") {
                        html += '<img src="' + data.file_loc + '" id="myImg"></img>';
                    } else if(data.media === "audio") {
                        html += '<audio controls><source src="' + data.file_loc + '" type="audio/mpeg"></audio>'
                    } else if(data.media === "video") {
                        html += '<video id="video" width="320" controls><source src="' + data.file_loc + '" type="video/mp4"></video>'
                    }
					$('#challenge-content').html(html);
					$('#challengeModal').css('display', 'inline');

                    $('.shade').css('display', 'inline');
                    $('#tag').prop('disabled',true);

					sizeModalWindow();
                    //Text-to-Speech for description
                    responsiveVoice.speak(data.device__description, "US English Male");
				} //end if
				else
					alert("Not quite. Try again!");
                    $('#tag').val('');
			}); //end getJSON
			return false;
		}
	});//end kepyress function

	$(".close").click(function(){
        $('#challengeModal').css('display', 'none');
        $('.shade').css('display', 'none');
        $("#tag").prop('disabled',false).focus();
	});//end click function for close button
});//end of doc ready function

$(window).resize(sizeModalWindow);

function sizeModalWindow(){
    var docW = $(document).width();
    var docH = $(document).height();

    var mod = $('#challengeModal');

    mod .css('width', 2*docW/3 + "px")
        .css('height', 2*docH/3 + "px")
        .css('left', ((docW/2)-(mod.width()/2)) + "px")
        .css('top', ((docH/2)-(mod.height()/2)) + "px");

    //fix the image height, if there is an image
    var imgTop = $('#myImg').position().top;
    $('#myImg').css('max-height', ((mod.height()-imgTop)-10) + "px");
};//end of sizeModalWindow function
