# create a app to download a movie from uqload (https://uqload.net/x7drc8msiwpu.html) with the best quality use yt_dlp:
import yt_dlp
import os

def download_movie(url):
    # Ensure downloads directory exists
    os.makedirs('downloads', exist_ok=True)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Guardar en la carpeta 'downloads'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        ydl.download([url])
        # Fix: Get the actual file extension from the format
        ext = info_dict.get('ext', 'mp4')
        return os.path.join('downloads', f"{video_title}.{ext}")

# download a movie
movie_url = input("Enter the movie link: ")
movie_file = download_movie(movie_url)