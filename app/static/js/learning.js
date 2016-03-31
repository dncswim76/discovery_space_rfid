$(document).ready(function() {
    $("#tag").focus();
    window.scrollTo(0,0);
	$(document).keypress(function(e) {
		if(e.which === 13) {
			$.getJSON($SCRIPT_ROOT + '/_validate_learning_tag', {
				tag: $('input[name="tag"]').val(),
				game_id: $('input[name="game_id"]').val()
			}, function(data) {
				if(data.valid === "true") {
					var html = '<h1>You scanned: <b>' + data.device__name + '</b></h1>';
                    html += '<h2>' + data.device__description + '</h2>';
                    if(data.media === "image") {
                        html += '<img src="' + data.file_loc + '"></img>';
                    } else if(data.media === "audio") {
                        html += '<audio controls><source src="' + data.file_loc + '" type="audio/mpeg"></audio>'
                    } else if(data.media === "video") {
                        html += '<video id="video" width="320" controls><source src="' + data.file_loc + '" type="video/mp4"></video>'
                    }
					$('#learning-content').html(html);
					$('#learningModal').css('display', 'inline');
				} //end if
				else
					alert("The object you scanned was not a part of this game. Try again!");
			}); //end getJSON
			return false;
		}
	});//end kepyress function
});//end of function
