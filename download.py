import yt_dlp
import os
import sys

def download_youtube_music_as_mp3(url, output_path='.'):
    """
    YouTube 음악을 MP3 파일로 다운로드합니다.

    Args:
        url (str): 다운로드할 YouTube 음악 URL.
        output_path (str, optional): MP3 파일을 저장할 출력 경로. 기본값은 현재 디렉토리('.')입니다.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



def download_youtube_playlist_as_mp3(playlist_url, output_path='.'):
    """
    YouTube 재생 목록을 MP3 파일로 다운로드합니다. 각 곡은 재생 목록 제목으로 된 폴더에 저장됩니다.

    Args:
        playlist_url (str): 다운로드할 YouTube 재생 목록 URL.
        output_path (str, optional): MP3 파일을 저장할 출력 경로. 기본값은 현재 디렉토리('.')입니다.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': False,  # 플레이리스트 전체 다운로드
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist_url)

if __name__ == "__main__":
    # Check if the playlist URL is provided as the first argument
    if len(sys.argv) < 2:
        print("Please provide the YouTube playlist URL as the first argument.")
        sys.exit(1)

    playlist_url = sys.argv[1]

    for folder in ["music_downloads"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    download_youtube_playlist_as_mp3(playlist_url, "./music_downloads")