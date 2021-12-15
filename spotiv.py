import vk_api
import requests
import config
import time


def get_current_track(access_token):
    response = requests.get(
        'https://api.spotify.com/v1/me/player/currently-playing',
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    if (response.status_code == 204):
        return {
            "is": False,
            "id": None
        }

    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "is": True,
    	"id": track_id,
    	"track_name": track_name,
    	"artists": artist_names,
    	"link": link
    }

    return current_track_info


if __name__ == "__main__":

    vk_session = vk_api.VkApi(token = config.VK_ACCESS_TOKEN)
    vk = vk_session.get_api()

    last_id = -1
    while True:
        try:
            track = get_current_track(config.SPOTIFY_ACCESS_TOKEN)

            if (track['id'] != last_id):
                last_id = track['id']
                new_status = ""
                if track["is"]:
                    new_status = f"Listening to {track['artists']} - \"{track['track_name']}\" in Spotify"
                vk_session.method("status.set", {"text": new_status})
                print(f"Succesfully changed status: {new_status}")
            else:
                print("Track not changed")
        except Exception as e:
            print("An error occured: ", e)
        time.sleep(5)
