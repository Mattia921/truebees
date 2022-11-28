import json
import requests
import os
import mimetypes
import pathlib
import shutil

from urllib.request import urlopen
from requests_toolbelt import MultipartEncoder


base_url = "https://graph.facebook.com/v15.0"

def upload_image(folder: str, imagename: str, access_token: str, phone_number_id: str):
    """
    Uploads a media to the cloud api and returns the id of the media

    Input:
        folder: str =  the source folder where the image is saved
        imagename: str = the name of the image to process
        access_token: str = the access token obtained after the creation-verification of a Facebook(WhatsAPP) Developer account
        phone_number_id: str = the ID of the Phone Number relatives to the WhatsApp Developer account

    Ouput:
        Image ID: str

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.upload_media("/path/to/media")

    REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#
    """
    media = "../" + folder + "/" + imagename
    url = f"{base_url}/{phone_number_id}/media"
    
    form_data = {
        "file": (
            media,
            open(media, "rb"),
            mimetypes.guess_type(media)[0],
            ),
            "messaging_product": "whatsapp",
            "type": mimetypes.guess_type(media)[0],
            }
            
    m = MultipartEncoder(fields=form_data)

    headers = {
        "Content-Type": m.content_type,
        "Authorization": "Bearer {}".format(access_token),
        }

    r = requests.post(
        url,
        headers=headers,
        data=m,
    )

    if r.status_code == 200:
        print(f"Upload WhatsApp Image = {imagename}")
        return r.json().get('id')

    print(f"Facebook upload error: {r.text}")
    return None


def query_media_url(media_id: str, access_token: str):

    """
    This function gets the link relatives to the image that has been already downloaded.
    It performs a GET call.

    Input:
        media_id: str = the Image ID
        access_token: str = the access token obtained after the creation-verification of a Facebook(WhatsAPP) Developer account

    Ouput:
        Image URL
    """

    url = f"{base_url}/{media_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token),
        }


    r = requests.get(url, headers = headers)
    if r.status_code == 200:
        return r.json()["url"]

    return None

def download_and_save_img(img_url: str, img_name_complete: str, access_token:str):

    """
    This function downlods the given image. It performs a GET call to Facebook APIs.
    Input:
        img_url: str = the link pointing to the image
        img_name_complete: str = the original image name
        access_token: str = the access token obtained after the creation-verification of a Facebook(WhatsAPP) Developer account
    Output:
        None
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token),
        }

    img_response = requests.get(img_url, headers = headers)

    img_name_list = img_name_complete.split(".")
    img_name = img_name_list[0]

    cwd = os.getcwd()
    targetPath = cwd + "\WhatApp_Download"
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

    targetFile = targetPath + "\\" + img_name
    image = open(targetFile+ '_WA' + '.jpeg', "wb")
    image.write(img_response.content)
    image.close()

    print(f"Download WhatsApp Image = {img_name_complete}")
    print("---------------")

def wrapper(folder:str):

    """
    This is just a wrapper function which iterates over all the images in the given folder, and it iteratively calls all the previous functions.
    
    Input: str = the folder name where the images are saved
    Ouput: None
    """

    with open('credentials.json') as f:
        credentials = json.load(f)
    access_token = credentials['access_token']
    phone_id = credentials['phone_number_ID']

    for imagename in os.listdir('../' + folder):

        origin_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), folder, imagename])
        destination_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), "Processed", imagename])

        print(origin_path)
        print(destination_path)


        image_id = upload_image(folder, imagename, access_token, phone_id)
        image_url = query_media_url(image_id, access_token)
        download_and_save_img(image_url, imagename, access_token)

        shutil.move(origin_path, destination_path)
    

    print(f"FINISHED! {folder}")
    return


