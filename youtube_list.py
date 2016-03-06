#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

class Youtube_List:

    #This method define how to connect with the Youtube API
    def connect(self):
        CLIENT_SECRETS_FILE = "client_secrets.json"


        MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

           %s

        with information from the Developers Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

        # This OAuth 2.0
        YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
          message=MISSING_CLIENT_SECRETS_MESSAGE,
          scope=YOUTUBE_READONLY_SCOPE)

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
          flags = argparser.parse_args()
          credentials = run_flow(flow, storage, flags)

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))
        return youtube

    #This method returns in a list all videos in a playlist
    def list_playlist(self, lista):
        #Connection
        youtube = self.connect()

        #List
        list = []

        # PlayList to analize
        print("PlayList to check:" + lista)
        playlistitems_list_request = youtube.playlistItems().list(playlistId=lista,
        part="snippet",
        maxResults=50)

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()
            # Print information about each video.
            for playlist_item in playlistitems_list_response["items"]:
                title = playlist_item["snippet"]["title"]
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                print "%s (%s)" % (title.encode('ascii','ignore'), video_id.encode('ascii','ignore'))
                list.append(video_id.encode('ascii','ignore'))
            playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)
        return list

    #This method saves a log of a playlist
    def save_playlist_on_file(self,list_id,list):
        try:
            os.makedirs("history"+os.path.sep+"playlists/")
            print("Creating folder: "+"history"+os.path.sep+"playlists/")
        except:
            print("The destination folder already exists")
        file = open("history/playlists/" + list_id + ".csv",'w')
        for item in list:
            file.write(item + "\n") #guardar como json
        file.close()
    
    #This method returns files that have not been downloaded yet
    def getDiferences(self,list_id,list):
        #check if the file already exists
        if(os.path.isfile("history/playlists/" + list_id + ".csv")):
        #"history/playlists/"
            file = open("history/playlists/" + list_id + ".csv","r")
            list_file = []
            list_to_download = []
            for line in file:
                list_file.append(line.rstrip('\n'))
            for item in list:
                if not item in list_file:
                    try:
                        list_to_download.append(item.rstrip('\n'))
                        print(str(item.rstrip('\n')) + " has been added to the download list")
                    except Exception, e:
                        print(str(e))
                else:
                    print(str(item.rstrip('\n')) + " wont be downloaded because this item already exists")
            return list_to_download
        else:
            return list
        return [];
    