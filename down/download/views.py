import os.path
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import re


# Create your views here.
def index(request):
    # if request.method == 'POST':
    #     video_link = request.POST.get('video_link')

    return render(request, 'index.html')


def is_youtube_url(url):
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu.be)/.+$'
    return re.match(youtube_pattern, url) is not None


def download(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if is_youtube_url(video_url):
            try:
                yt = YouTube(video_url)
                video_stream = yt.streams.get_highest_resolution()
                download_dir = os.path.expanduser("~/Downloads")
                # file_path = os.path.join(download_dir, yt.title + ".mp4")
                video_stream.download(output_path=download_dir)
                return HttpResponse("Download Complete!")

            except RegexMatchError:
                return HttpResponse("Invalid YouTube URL. Please enter a valid YouTube URL.")
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Please enter a valid YouTube URL.")
    else:
        return HttpResponse("Only POST requests are supported")
