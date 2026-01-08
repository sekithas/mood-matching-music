function addToFavorites(songId) 
            {
                fetch("/favorites", 
                    {
                        method: "POST",
                        headers: 
                            {
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                        body: "song_id=" + encodeURIComponent(songId)
                    })

                .then(response => 
                    {
                        if (response.ok) 
                            {
                                showMessage("⭐ Added to favorites!");
                            }
                    });
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
