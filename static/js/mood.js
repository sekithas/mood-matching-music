let searchTimeout;

function searchSongsLive() 
            {
                const text = document.getElementById("userInput").value.trim();
                const mood = document.getElementById("mood-container").dataset.mood;

                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => 
                    {
                        fetch(`/search/${mood}?q=${encodeURIComponent(text)}`)
                        .then(response => response.json())
                        .then(songs => updateTable(songs));
                    }
                    , 300); 
            }

function updateTable(songs) 
            {
                const tbody = document.querySelector("table tbody");
                tbody.innerHTML = ""; 

                songs.forEach(song => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${song.track_name}</td>
                        <td>${song.track_artist}</td>
                        <td style="text-align: center;">${song.track_popularity}</td>
                        <td style="text-align: center;">
                            <button class="btn btn-sm btn-outline-primary" onclick="loadPlayer('${song.track_id}')">▶</button>
                            <div id="player-${song.track_id}"></div>
                        </td>
                        <td style="text-align: center;">
                            <button class="btn btn-sm btn-outline-success" onclick="addToFavorites('${song.track_id}')">⭐</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }