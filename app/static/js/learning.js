$(document).ready(function(){
	$(document).keypress(function(e){
		if(e.which === 13){
			$.getJSON($SCRIPT_ROOT + '/_validate_learning_tag',{
				tag: $('input[name="tag"]').val(),
				game_id: $('input[name="game_id"]').val()
			}, function(data){
				if(data.valid === "true"){
					var html = '<h1>' + data.device__name + '</h1>'
						+ '<img src="' + data.file_loc + '"></img>';
					$('#learning-content').append(html);
					$('#learningModal').css('display', 'inline');
				}//end if
				else
					alert("The object you scanned was not a part of this game.");
			});//end getJSON
			return false;
		}
	});//end kepyress function
});//end of function