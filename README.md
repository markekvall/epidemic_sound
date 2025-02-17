# Sound Playlist Management App

## **Overview**

This app provides an API to manage sounds, playlists, and sound recommendations, built using FastAPI. It allows you to:

1. **Create Sounds**  
   `POST /admin/sounds`: Allows administrators to add multiple new sounds to the system. Each sound can be created with specific details like title, BPM, duration, genres, and credits.

2. **Get All Sounds**  
   `GET /sounds`: Retrieves a list of all available sounds in the system, including their associated genres and credits.

3. **Create Playlists**  
   `POST /playlists`: Allows users to create new playlists by specifying a title and the associated sounds (by sound IDs). It supports batch creation of multiple playlists.

4. **Get Recommended Sound**  
   `GET /sounds/recommended`: Based on a provided playlist ID, this endpoint recommends a random sound that shares genres with the sounds already in the playlist. If no matching sound is found, a random sound will be recommended.

---

## **Extra Endpoint**

### **Get Playlists by Sound**  
`GET /playlists/by-sound`: Given a sound ID, this endpoint retrieves all playlists that contain that specific sound.

---

## **Running the App**

### **Run the App Locally**

To run the app locally using Poetry:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### **Run the app using docker**

```bash
docker build -t my-awesome-epidemic-app .
docker run -p 8080:8080 my-awesome-epidemic-app
```
The app will be accessible at http://localhost:8080.

## **Running the tests**
```bash
poetry run pytest
```
