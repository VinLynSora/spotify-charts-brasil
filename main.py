import os
import time
import unicodedata
import requests
import spotipy

from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


# ==========================================
# 1. CONFIGURAÇÕES
# ==========================================

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_BEARER = os.getenv("SPOTIFY_BEARER")

if not all([
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_BEARER
]):
    raise ValueError(
        "Verifique as variáveis de ambiente no arquivo .env"
    )

scope = "playlist-modify-private"


# ==========================================
# 2. CONECTAR AO SPOTIFY
# ==========================================

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        cache_path=".spotify_cache"
    )
)


# ==========================================
# 3. INFORMAR A DATA
# ==========================================

date = input(
    "Para qual data você quer viajar no tempo? "
    "Digite YYYY-MM-DD: "
)

try:
    datetime.strptime(date, "%Y-%m-%d")
except ValueError:
    raise ValueError(
        "Data inválida! Utilize o formato YYYY-MM-DD."
    )


# ==========================================
# 4. BUSCAR O RANKING DO BRASIL
# ==========================================

def get_brazil_chart(date):

    url = (
        "https://charts-spotify-com-service.spotify.com/"
        f"auth/v0/charts/regional-br-daily/{date}"
    )

    headers = {
        "Authorization": f"Bearer {SPOTIFY_BEARER}",
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    if response.status_code == 401:
        raise RuntimeError(
            "Token do Spotify Charts expirado ou inválido. "
            "Atualize o SPOTIFY_BEARER no arquivo .env."
        )

    if response.status_code == 404:
        raise RuntimeError(
            "Ranking não encontrado para essa data."
        )

    response.raise_for_status()

    chart_data = response.json()

    entries = chart_data.get("entries", [])

    if not entries:
        raise RuntimeError(
            "Nenhuma música foi encontrada nesse ranking."
        )

    songs = []

    for entry in entries:

        metadata = entry.get("trackMetadata", {})
        chart_info = entry.get("chartEntryData", {})

        song_name = metadata.get("trackName")
        artists = metadata.get("artists", [])

        if not song_name or not artists:
            continue

        artist_names = [
            artist["name"]
            for artist in artists
        ]

        songs.append({
            "rank": chart_info.get("currentRank"),
            "name": song_name,
            "artist": ", ".join(artist_names),
            "primary_artist": artist_names[0],
            "uri": metadata.get("trackUri")
        })

    return songs


print("\nBuscando as músicas do Spotify Brasil...")

songs = get_brazil_chart(date)

print(f"\n{len(songs)} músicas encontradas!\n")

for song in songs:
    print(
        f"{song['rank']}. "
        f"{song['name']} - {song['artist']}"
    )


# ==========================================
# 5. NORMALIZAR NOMES
# ==========================================

def normalize_text(text):

    text = unicodedata.normalize("NFKD", text)

    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    return text.casefold().strip()


# ==========================================
# 6. BUSCAR URIS DAS MÚSICAS
# ==========================================

def get_song_uris(song_list):

    results = []

    for song in song_list:

        # Aproveita o URI do próprio ranking,
        # quando ele estiver disponível.

        if song["uri"]:
            results.append({
                **song,
                "spotify_uri": song["uri"]
            })

            continue

        # Caso não exista URI, pesquisa no catálogo.

        search_result = sp.search(
            q=(
                f'track:"{song["name"]}" '
                f'artist:"{song["primary_artist"]}"'
            ),
            type="track",
            limit=10,
            market="BR"
        )

        tracks = search_result["tracks"]["items"]

        matched_track = None

        for track in tracks:

            same_name = (
                normalize_text(track["name"])
                == normalize_text(song["name"])
            )

            track_artists = [
                normalize_text(artist["name"])
                for artist in track["artists"]
            ]

            same_artist = (
                normalize_text(song["primary_artist"])
                in track_artists
            )

            if same_name and same_artist:
                matched_track = track
                break

        if matched_track:

            results.append({
                **song,
                "spotify_uri": matched_track["uri"]
            })

        else:

            results.append({
                **song,
                "spotify_uri": None
            })

        # Pequeno intervalo entre pesquisas.
        time.sleep(0.1)

    return results


print("\nProcurando as músicas no catálogo do Spotify...")

matched_songs = get_song_uris(songs)

track_uris = []

not_found = []

seen_uris = set()

for song in matched_songs:

    uri = song["spotify_uri"]

    if uri and uri not in seen_uris:

        track_uris.append(uri)
        seen_uris.add(uri)

    elif not uri:

        not_found.append(song)


# ==========================================
# 7. EXIBIR RESULTADOS
# ==========================================

print("\nRESULTADO DA PESQUISA\n")

for song in matched_songs:

    print(
        f"{song['name']} - {song['artist']} "
        f"-> {song['spotify_uri']}"
    )


print("\nTotal de músicas no ranking:", len(songs))
print("Músicas encontradas:", len(track_uris))
print("Músicas não encontradas:", len(not_found))


# ==========================================
# 8. CRIAR A PLAYLIST
# ==========================================

if track_uris:

    playlist = sp.current_user_playlist_create(
        name=f"Brasil - {date}",
        public=False,
        description=(
            f"Top músicas mais ouvidas no Brasil "
            f"em {date}. Criada automaticamente com Python."
        )
    )

    # Adicionar músicas em lotes de até 100.

    for i in range(0, len(track_uris), 100):

        batch = track_uris[i:i + 100]

        sp.playlist_add_items(
            playlist_id=playlist["id"],
            items=batch
        )

    print("\nPlaylist criada com sucesso!")

    print(
        "Spotify URL:",
        playlist["external_urls"]["spotify"]
    )

else:

    print(
        "\nNenhuma música foi encontrada. "
        "A playlist não foi criada."
    )


# ==========================================
# 9. EXIBIR MÚSICAS NÃO ENCONTRADAS
# ==========================================

if not_found:

    print("\nMÚSICAS NÃO ENCONTRADAS:\n")

    for song in not_found:

        print(
            f"- {song['name']} - {song['artist']}"
        )
