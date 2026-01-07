function loadPlayer(trackId) {
    const container = document.getElementById(`player-${trackId}`);

    if (container.innerHTML !== "") return 404;

    container.innerHTML = `
        <iframe
            src="https://open.spotify.com/embed/track/${trackId}"
            width="300"
            height="80"
            frameborder="0"
            allow="encrypted-media">
        </iframe>
    `;
}