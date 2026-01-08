function loadPlayer(trackId) 
            {
                const container = document.getElementById(`player-${trackId}`);

                if (container.innerHTML !== "") 
                    {
                        return;
                    }
                    
                container.innerHTML = `
                    <br>
                    <iframe
                        src="https://open.spotify.com/embed/track/${trackId}"
                        width="300"
                        height="80"
                        frameborder="0"
                        allow="encrypted-media">
                    </iframe>
                `;
            }