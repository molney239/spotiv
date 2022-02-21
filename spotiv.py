import vk_api
import config
import time
import requests


def get_track(access_token):
    response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )

    if response.status_code == 204:
        return {
            "success": True,
            "status_code": response.status_code,
            "id": None,
            "track_name": None,
            "artists": None
        }
    if response.status_code != 200:
        return {
            "success": False,
            "status_code": response.status_code
        }
    
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]
    artists = [artist['name'] for artist in artists]

    return {
        "success": True,
        "status_code": response.status_code,
    	"id": track_id,
    	"track_name": track_name,
    	"artists": artists
    }


def set_status(access_token, text):
    vk_session = vk_api.VkApi(token = access_token)
    vk_session.method("status.set", {"text": text})


if __name__ == "__main__":

    print("Inited")

    last_id = None
    while True:
        current_id = None
        track = None

        try:
            track = get_track(config.SPOTIFY_ACCESS_TOKEN)
        except Exception as e:
            print("Failed to get current track: ", e.with_traceback)
            continue

        if track["success"]:
            current_id = track["id"]
        else:
            print("Failed to get current track: Server returned code", track["status_code"])
            continue
        
        if current_id != last_id:
            last_id = current_id
            new_status = ""
            if current_id != None:
                new_status = f"Listening to {', '.join(track['artists'])} - \"{track['track_name']}\" in Spotify"

            try:
                set_status(config.VK_ACCESS_TOKEN, new_status)
                print(f"Succesfully changed status: {new_status}")
            except Exception as e:
                print("An error occured while changing status:", e.with_traceback)
                continue
        else:
            print("Track not changed")

        time.sleep(config.DELAY_SECONDS)
