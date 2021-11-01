#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse
import logging
from google.auth.transport import Request

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from telegram.ext.inlinequeryhandler import InlineQueryHandler
import constants as keys
from telegram import Update, InlineQueryResultVideo
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = keys.GOOGLE_DEV_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                         search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                          search_result['id']['playlistId']))

    print('Videos:\n', '\n'.join(videos), '\n')
    print('Channels:\n', '\n'.join(channels), '\n')
    print('Playlists:\n', '\n'.join(playlists), '\n')

    return videos[0]


def command_video(update: Update, context: CallbackContext):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_term = ' '.join(context.args)
    print("Context is: " + search_term)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=search_term,
        part='id,snippet',
        maxResults=5
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))

    print('Videos:\n', '\n'.join(videos), '\n')
    default_youtube_url = 'https://www.youtube.com/watch?v='
    videoid = search_result['id']['videoId']
    print("Full URL is: " + default_youtube_url + videoid)

    InlineQueryResultVideo(
        id='',
        video_url='',
        mime_type='',
        thumb_url='',
        title='',
        input_message_content=default_youtube_url + videoid
    )
    return videos[0]


def retrieve_video(videos):
    # Used to retrieve youtube video
    default_youtube_url = 'https://www.youtube.com/watch?v='
    videoid = videos['id']['videoId']
    print("Full URL is: " + default_youtube_url + videoid)

    InlineQueryResultVideo(
        id='',
        video_url='',
        mime_type='',
        thumb_url='',
        title='',
        input_message_content=default_youtube_url + videoid
    )


def inline_video_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_term = query
    search_respone = youtube.search().list(
        q=search_term,
        part='id,snippet',
        maxResults=5
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_respone.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))

    print('Videos:\n', '\n'.join(videos), '\n')

    default_youtube_url = 'https://www.youtube.com/watch?v='
    videoid = search_result['id']['videoId']
    first_video_id = search_result['items'][0]['id']['videoId']
    print("Full URL is: " + default_youtube_url + videoid)
    print("First video id is: " + first_video_id)
    results = [
        InlineQueryResultVideo(
            id='',
            video_url='default_youtube_url + videoid',
            mime_type='',
            thumb_url='',
            title='',
            input_message_content=default_youtube_url + videoid
        )
    ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=5)
    args = parser.parse_args()

    # Create the Update and pass it my bot's token
    updater = Updater(keys.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands
    dispatcher.add_handler(CommandHandler("youtube", command_video))
    dispatcher.add_handler(InlineQueryHandler(inline_video_query))
    # Start the bot
    updater.start_polling()

    updater.idle()

    # try:
    # youtube_search(args)

    # except HttpError as e:
    # print("An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)")
