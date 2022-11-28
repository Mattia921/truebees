import argparse
import os

from Facebook import facebook_upload_download
from Telegram import telegram_upload_download
from Twitter import twitter_upload_download
from Whatsapp import whatsapp_upload_download


if __name__ == '__main__':

    ap = argparse.ArgumentParser()

    ap.add_argument("-f", "--folder", required=True, help='Folder where to search for image to upload-download')
    ap.add_argument("-s", "--social", choices=['facebook', 'whatsapp', 'telegram', 'twitter'], required=True, 
                    help='The name of the social on which to process the image: eg')
    args = vars(ap.parse_args())
    folder = args["folder"]
    social = args["social"]


    if social == 'facebook':
        os.chdir(os.getcwd() + '\\' + 'Facebook')
        facebook_upload_download.wrapper(folder)
    elif social == 'whatsapp':
        os.chdir(os.getcwd() + '\\' + 'Whatsapp')
        whatsapp_upload_download.wrapper(folder)
    elif social == 'telegram':
        os.chdir(os.getcwd() + '\\' + 'Telegram')
        telegram_upload_download.wrapper(folder)
    else:
        os.chdir(os.getcwd() + '\\' + 'Twitter')
        twitter_upload_download.wrapper(folder)

