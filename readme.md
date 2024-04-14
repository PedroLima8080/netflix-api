# Netflix API

This API collection is designed to interact with a local server for managing videos, playlists, and user history, simulating some functionalities of a Netflix-like platform.

## Authentication

To access the endpoints, you need to authenticate using a bearer token. The token should be included in the `Authorization` header for each request.

## Start api
  - Run ```__main__.py``` file

## Run tests
  - Run ```python -m pytest``` in terminal

## Endpoints

### Authentication

- **Login**
  - **Description**: Authenticate user and obtain access token.
  - **Method**: POST
  - **URL**: `http://localhost:5000/auth/login`
  - **Headers**:
    - `Content-Type: application/json`
  - **Body**:
    ```json
    {
        "email": "ph.lima014@gmail.com",
        "password": "123"
    }
    ```

- **Register**
  - **Description**: Register a new user.
  - **Method**: POST
  - **URL**: `http://localhost:5000/auth/register`
  - **Headers**:
    - `Content-Type: application/json`
  - **Body**:
    ```json
    {
        "username": "Pedro Lima",
        "email": "ph.lima014@gmail.com",
        "password": "123"
    }
    ```


### Videos

- **List Videos**
  - **Description**: Retrieve a list of available videos.
  - **Method**: GET
  - **URL**: `http://localhost:5000/videos`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

- **Get Video**
  - **Description**: Retrieve details of a specific video.
  - **Method**: GET
  - **URL**: `http://localhost:5000/videos/1`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

- **Create Video**
  - **Description**: Add a new video to the collection.
  - **Method**: POST
  - **URL**: `http://localhost:5000/videos`
  - **Headers**:
    - `Content-Type: application/json`
    - `Authorization: Bearer {{token}}`
  - **Body**:
    ```json
    {
        "title": "Titulo aqui",
        "description": "Descrição aqui",
        "genre": "Genero aqui",
        "release_year": 2003,
        "rating": 5
    }
    ```

- **Update Video**
  - **Description**: Update details of an existing video.
  - **Method**: PUT
  - **URL**: `http://localhost:5000/videos/1`
  - **Headers**:
    - `Content-Type: application/json`
    - `Authorization: Bearer {{token}}`
  - **Body**:
    ```json
    {
        "title": "Titulo aquiiiiii",
        "description": "Descrição aqui",
        "genre": "Genero aqui",
        "release_year": 2003,
        "rating": 5
    }
    ```

- **Delete Video**
  - **Description**: Remove a video from the collection.
  - **Method**: DELETE
  - **URL**: `http://localhost:5000/videos/1`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

- **Play Video**
  - **Description**: Start playing a video.
  - **Method**: POST
  - **URL**: `http://localhost:5000/videos/1/play`
  - **Headers**:
    - `Authorization: Bearer {{token}}`


### Playlists

- **List Playlists**
  - **Description**: Retrieve a list of user playlists.
  - **Method**: GET
  - **URL**: `http://localhost:5000/playlist`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

- **Create Playlist**
  - **Description**: Create a new playlist.
  - **Method**: POST
  - **URL**: `http://localhost:5000/playlist`
  - **Headers**:
    - `Content-Type: application/json`
    - `Authorization: Bearer {{token}}`
  - **Body**:
    ```json
    {
        "name": "Nome aqui"
    }
    ```

- **Delete Playlist**
  - **Description**: Remove a playlist.
  - **Method**: DELETE
  - **URL**: `http://localhost:5000/playlist/1`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

### Playlist Videos

- **List Playlist Videos**
  - **Description**: Retrieve videos within a playlist.
  - **Method**: GET
  - **URL**: `http://localhost:5000/playlist/1/videos`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

- **Add Video to Playlist**
  - **Description**: Add a video to a playlist.
  - **Method**: POST
  - **URL**: `http://localhost:5000/playlist/1/videos`
  - **Headers**:
    - `Content-Type: application/json`
    - `Authorization: Bearer {{token}}`
  - **Body**:
    ```json
    {
        "video_id": 2
    }
    ```

- **Remove Video from Playlist**
  - **Description**: Remove a video from a playlist.
  - **Method**: DELETE
  - **URL**: `http://localhost:5000/playlist/1/videos/2`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

### History

- **List History**
  - **Description**: Retrieve user viewing history.
  - **Method**: GET
  - **URL**: `http://localhost:5000/history`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

- **Clear History**
  - **Description**: Clear user viewing history.
  - **Method**: DELETE
  - **URL**: `http://localhost:5000/history/1`
  - **Headers**:
    - `Authorization: Bearer {{token}}`

