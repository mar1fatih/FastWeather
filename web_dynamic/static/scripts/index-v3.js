$(document).ready(function() {
            $("#button_create").click(function(event) {
		    event.preventDefault();
                
                // Check if all input fields are filled
                var allFilled = true;
		let uniqname = true;
		let uniqemail = true;
                $("input[type='text'], input[type='email'], input[type='password']").each(function() {
                    if ($(this).val() === "") {
                        allFilled = false;
                        return false;  // Exit the each loop
                    }
                });


		$.ajax({
                        url: "http://127.0.0.1:5001/api/v1/users/",
                        type: "GET",
                        success: function(response) {
                                $.each(response, function(index, user) {
                                    if (user.username === $("input[type='text']").val()) {
                                        uniqname = false;
					return false;
                                   }
                                });
				$.each(response, function(index, user) {
				    if (user.email === $("input[type='email']").val()) {
                                       	uniqemail = false;
					return false;
                                   }
				});
				if (allFilled && uniqname && uniqemail) {
                        		alert("All fields are filled. Proceeding...");
                    			$.ajax({
                        			url: "http://127.0.0.1:5001/api/v1/users/",
                        			type: "POST",
                        			contentType: "application/json",
                        			data: JSON.stringify({ username: $(".input_username").val(), email: $(".input_email").val(), password: $(".input_password").val()}),
                        			success: function(response) {
                                			window.location.href = "http://127.0.0.1:5000/login";
                        			},
                        			error: function(xhr, status, error) {
                            				console.error("Error:", status, error);
                        			}
                    			});
                		} else if (!allFilled) {
                    			alert("Please fill all fields.");
                		} else if (!uniqname){
                    			alert("username already exist");
                		} else {
                    			alert("you already signed-in")
                		}
                        },
                        	error: function(xhr, status, error) {
			    		console.error("Error:", status, error);
                        	}
                    });
            });
        });
