import requests
import json

def main():
    CLIENT_ID = 'CLIENT_ID_GOES_HERE'
    CLIENT_SECRET = 'CLIENT_SECRET_GOES_HERE'

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    BASE_URL = 'https://api.spotify.com/v1/'

    artist_id = '7INMT690LmwS6H12syogmY' # STALLED

    # pull all artists albums
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                    headers=headers,
                    params={'include_groups': 'single', 'limit': 50})
    d = r.json()


    album_list = []

    for album in d.get('items'):
        album_id = album.get('id')
        r = requests.get(
            BASE_URL + 'albums/' + album_id + '/tracks', 
            headers=headers
        )
        d = r.json()
        album_list.append(d)

    track_dict = {}
    for album in album_list:
        items = album.get("items")
        for track in items:
            track_id = track.get("id")
            track_name = track.get("name")
            r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
            r = r.json()
            track_dict[track_name] = r

    with open('data.json', 'w') as f:
        json.dump(track_dict, f)

if __name__ == '__main__':
    main()