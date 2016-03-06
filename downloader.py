#!/usr/bin/python

import youtube_dl

class Downloader:
    
    #This method checks a list to download each item
    def download_list(self,list_to_download):
        list_errors = []
        for item in list_to_download:
            if not self.download(item):
                list_errors.append(item)
        return list_errors
    
    #This method downloads an item calling Youtube_DL    
    def download(self,item):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(["http://www.youtube.com/watch?v=" + item])
            print(item + " was downloaded")
            return True
        except:
            return False