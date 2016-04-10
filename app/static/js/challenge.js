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
					var html = '<h1>Correct! You scanned: <b>' + data.device__name + '</b></h1>';
                    html += '<h2>' + data.device__description + '</h2>';
                    if(data.media === "image") {
                        html += '<img src="' + data.file_loc + '"></img>';
                    } else if(data.media === "audio") {
                        html += '<audio controls><source src="' + data.file_loc + '" type="audio/mpeg"></audio>'
                    } else if(data.media === "video") {
                        html += '<video id="video" width="320" controls><source src="' + data.file_loc + '" type="video/mp4"></video>'
                    }
					$('#challenge-content').html(html);
					$('#challengeModal').css('display', 'inline');

					sizeModalWindow();
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
        $("#tag").focus();
	});//end click function for close button
});//end of doc ready function

$(window).resize(sizeModalWindow);

function sizeModalWindow(){
	var docW = $(document).width();
	var docH = $(document).height();
	$('#challengeModal').css('width', docW/2 + "px")
		.css('right', docW/16 + "px")
		.css('top', docH/4 + "px");
};//end of sizeModalWindow function
