#!/usr/bin/python
import os
import shutil
from os.path import expanduser

from youtube_list import Youtube_List
from downloader import Downloader

URI = expanduser("~") + os.path.sep + "MusyncMusic"

#This is the main method
def dialy_execution():
    try:
        playlists = []
        fileList = open("playlist.csv","r")
        for line in fileList:
            playlists.append(line.rstrip('\n'))
        for playlist in playlists:
            print("Deleting old files")
            delete_old_files()
            print("PlayList selected: " + playlist)
            donwload_playlist(playlist)
            print("Moving files")
            moveFiles(playlist,URI)
    except Exception,e:
        print(str(e))

#This method organizes how to download a playlist
def donwload_playlist(playlist):
    youtube = Youtube_List()
    lista = youtube.list_playlist(playlist)
    #Check if some files are already downloaded
    list_to_download = youtube.getDiferences(playlist,lista)
    download = Downloader()
    list_errors = download.download_list(list_to_download)
    #Create the logs files
    youtube.save_playlist_on_file(playlist + ".err",list_errors)
    youtube.save_playlist_on_file(playlist,lista)

#This method moves all downloaded files to the respective folder in URI
def moveFiles(playlist,uri):
    #List all files in the current folder
    list_all_files = os.listdir(os.getcwd())
    #Check and list what kind of files has to be moved
    list_to_move = []
    for item in list_all_files:
        if ((".mp3" in item) or (".m4a" in item)  or (".webm" in item)):
            list_to_move.append(item)
            print(item + " will be moved")
    print(str(item))
    #Check if the destination folder already exists
    try:
        os.makedirs(uri + os.path.sep + playlist)
        print("Creating folder: "+uri + os.path.sep + playlist)
    except:
        print("The destination folder already exists")
    #Move files
    try:
        for item in list_to_move:
            shutil.move(os.getcwd()+os.path.sep+item,uri + os.path.sep + playlist + os.path.sep + item)
            print(item + " has been moved to ->" + uri + os.path.sep + playlist + os.path.sep + item)
    except Exception, e:
        print(str(e))
    print("All files have been moved to: "+ uri + os.path.sep + playlist + os.path.sep)

#This method removes .part files
def delete_old_files():
    list_all_files = os.listdir(os.getcwd())
    for item in list_all_files:
        if (".part" in item):
            os.remove(item)


dialy_execution()