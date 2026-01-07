function addToFavorites(songId) 
            {
                fetch("/favorites", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: "song_id=" + encodeURIComponent(songId)
                })
                //modern AJAX to tell flask to conduct the flask route without reloading and passing in: value as the songId

                .then(response => {
                if (response.ok) 
                {
                    showMessage("⭐ Added to favorites!");
                }
                });
                //if the response is correct, then a function showMessage is called
            }

            function showMessage(text) 
            {
            const msg = document.getElementById("message");
            msg.textContent = text;
            msg.style.display = "block";

            setTimeout(() => 
            {
                msg.style.display = "none";
            }, 2000);
            }
            //this function displays the "Added to favorites" box in the top (styled with CSS & Bootstrap) which goes away after 2 seconds
