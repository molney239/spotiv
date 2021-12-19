import vk_api
import config
import time
import spotipy

def authorize_spotify():
    token = spotipy.util.prompt_for_user_token(config.USERNAME, "user-read-currently-playing", config.CLIENT_ID, config.CLIENT_SECRET, "http://localhost:8888/callback")
    return spotipy.Spotify(auth=token)

if __name__ == "__main__":

    vk_session = vk_api.VkApi(token = config.VK_ACCESS_TOKEN)
    vk = vk_session.get_api()

    print("VK authorization succesful")

    sp = authorize_spotify()

    print(f"Spotify authorization succesful")

    last_id = -1
    while True:
        current_id = -1
        track = None

        try:
            track = sp.current_user_playing_track()
        except Exception as e:
            print("Failed to get current song:", e)
            continue

        if track != None:
            current_id = track['item']['id']
        
        if current_id != last_id:
            last_id = current_id
            new_status = ""
            if current_id != -1:
                new_status = f"Listening to {track['item']['artists'][0]['name']} - \"{track['item']['name']}\" in Spotify"

            try:
                vk_session.method("status.set", {"text": new_status})
                print(f"Succesfully changed status: {new_status}")
            except Exception as e:
                print("An error occured while changing status:", e.with_traceback)
                continue
        else:
            print("Track not changed")

        time.sleep(5)
