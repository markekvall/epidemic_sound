# Backend app

Sound Playlist Management App
This app provides an API to manage sounds, playlists, and sound recommendations, built using FastAPI. It allows you to:

1. Create Sounds
POST /admin/sounds: Allows administrators to add multiple new sounds to the system. Each sound can be created with specific details like title, BPM, duration, genres, and credits.
2. Get All Sounds
GET /sounds: Retrieves a list of all available sounds in the system, including their associated genres and credits.
3. Create Playlists
POST /playlists: Allows users to create new playlists by specifying a title and the associated sounds (by sound IDs). It supports batch creation of multiple playlists.
4. Get Playlists by Sound
GET /playlists/by-sound: Given a sound ID, this endpoint retrieves all playlists that contain that specific sound.
5. Get Recommended Sound
GET /sounds/recommended: Based on a provided playlist ID, this endpoint recommends a random sound that shares genres with the sounds already in the playlist. If no matching sound is found, a random sound will be recommended.

