from pytube import YouTube 
import os

def download_youtube_to_mp3(links: list[str], download_location: str) -> None:
    """downloads an mp3 from a list of youtube links"""
    os.makedirs(download_location, exist_ok=True)
    for link in links:
        youtube_link = YouTube(link)
        mp3 = youtube_link.streams.filter(only_audio=True).first()
        mp3.download(download_location)
