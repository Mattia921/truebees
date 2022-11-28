import os
import json
import requests
from requests_oauthlib import OAuth1
import pathlib
import tweepy
from tweepy import OAuthHandler
import json
import wget
import os
import shutil


class ImageTweet(object):

    def __init__(self, image_name):
        """
        Defines image tweet properties

        Input:
            file_name: str = name of the file to upload
        Output:
            ImageTweet instance
        """
        self.image_filename = image_name
        self.media_id = None
        self.tweet_id = None

        self.MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
        self.POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'
        

        with open("credentials.json") as f:
            self.credentials = json.load(f)
        self.consumer_key = self.credentials["API_key"]
        self.consumer_secret = self.credentials["API_secret_key"]
        self.access_token = self.credentials["Access_token"]
        self.access_secret = self.credentials["Access_token_secret"]

        self.oauth = OAuth1(client_key = self.consumer_key,
                            client_secret=self.consumer_secret,
                            resource_owner_key=self.access_token,
                            resource_owner_secret=self.access_secret)

    def upload(self):

        """
        This method uploads the ImageTweet instance. This is a required step, before the true image upload on a tweet. 
        It performs a POST call to Twitter APIs."""

        data = open(self.image_filename, 'rb').read()
        file = {
            'media':data,
            'media_category':'tweet_image'
        }

        while True:
            response = requests.post(url=self.MEDIA_ENDPOINT_URL, files=file, auth=self.oauth)
            if response.status_code == 200:
                self.media_id = response.json()['media_id']
                break
            else:
                continue
            
        return 

    def tweet(self, image_filename):
        """
        Publishes Tweet with attached image

        Input:
            image_filename: str = name of the image to upload
        Output:
            None
        """

        request_data = {
            'status': 'Upload image: ' + image_filename,
            'media_ids': self.media_id
        }

        while True: 
            response = requests.post(url=self.POST_TWEET_URL, data=request_data, auth=self.oauth)
            if response.status_code == 200:
                self.tweet_id = response.json()['id']
                break
            else:
                continue
        
        return

    def download(self):
        """
        This method returns the link relatives to the tweet where the image has been attached.
        """

        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        api = tweepy.API(auth)
        tweet = api.get_status(self.tweet_id)
        image_url = tweet.extended_entities['media'][0]['media_url']
        return image_url

def wrapper(folder):

    """
    This is just a wrapper function which iterates over all the images in the given folder, and it iteratively calls all the previous functions.
    
    Input: str = the folder name where the images are saved
    Ouput: None
    """

    if not os.path.exists('./DownloadedImages/' + folder):
        os.makedirs('./DownloadedImages/' + folder)

    for image_filename in os.listdir('../' + folder):

        origin_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), folder, image_filename])
        destination_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), "Processed", image_filename])

        while True:
            try:
                print("----------")

                imageTweet = ImageTweet('../' + folder + '/' + image_filename)
                imageTweet.upload()
                imageTweet.tweet(image_filename=image_filename)
                print(f"Uploaded Image: {image_filename}")

                image_url = imageTweet.download()
                original_name = image_filename.split('.')[0]
                download_image = wget.download(image_url, out='./DownloadedImages/' + folder + '/' + original_name + '_TW' + '.jpg')
                print(f"Downloaded Image: {image_filename}")
                break

            except KeyError:
                continue

        shutil.move(origin_path, destination_path)

    print("DONE!!!")
    return
        


    
        