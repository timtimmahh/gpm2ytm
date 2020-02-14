from gmusicapi import Mobileclient
from os import remove
from os.path import isfile
from pathlib import Path
from json import loads, dumps


client = Mobileclient()


def do_login():
    cred_file = f'{Path().absolute()}/.gpm_token'
    print(f'Checking if credentials are saved at {cred_file}')
    if not isfile(cred_file):
        print('No credentials saved. Opening browser to perform authentication...')
        client.perform_oauth(storage_filepath=cred_file, open_browser=True)
    print('Logging in...')
    if not client.oauth_login(device_id=Mobileclient.FROM_MAC_ADDRESS,
                              oauth_credentials=cred_file,
                              locale='en_US'):
        remove(cred_file)
        return do_login()
    print('Logged in!' if client.is_authenticated() else 'Login failed!')
    return client.is_authenticated()


def transfer_gpm_to_ytm():
    authenticated = do_login()
    print(f'Authentication status: {authenticated}')
    if not authenticated:
        return
    client.get_all_songs()
    client.get_all_playlists()


if __name__ == '__main__':
    print('Logging in...')
    if do_login():
        tracks = client.get_all_songs()
        ids = ['648b82b7-015f-3823-bf21-3d31d7dc822d', '02a9b776-8606-37bd-8a92-c723e558c8d5']
        pEntry = None
        for track in tracks:
            if track['id'] in ids or track.get('storeId', None) in ids or track.get('nid', None) in ids:
                pEntry = track
        if pEntry is not None:
            print('Playlist Entry')
            print(dumps(pEntry, indent=4))
        print(dumps(tracks[0], indent=4))
        print(dumps(client.get_all_playlists()[0], indent=4))
        print(dumps(client.get_all_user_playlist_contents()[0], indent=4))
