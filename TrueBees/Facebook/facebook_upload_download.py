import json
import requests
import os
import argparse
import pathlib
import shutil

from urllib.request import urlopen
from requests_toolbelt import MultipartEncoder


def upload_img(folder: str, imagename: str, access_token: str, page_id: str):

    """
    This functions takes an image and uploads it to the given Facebook Page. 
    It performs a POST call to Facebook APis.

    Input:
        folder: str =  the source folder where the image is saved
        imagename: str = the name of the image to process
        access_token: str = the access token obtained after the creation-verification of a Facebook Developer account
        page_id: str = the Id of the Facebook Page, where the image will be uploaded

    Output:
        Image ID: str = the ID of the image, posted on the Facebook Page. This will be useful for tracing the image to be downloaded

    """

    m = MultipartEncoder(
        fields={"access_token": access_token,
                "source": ("../" + folder + "/" + imagename,
                            open("../" + folder + "/" + imagename, 'rb')),
                "title": imagename,
                "description": "Uploading image with API"})


    url = "https://graph-video.facebook.com/v13.0/" + page_id + "/photos"
    response = requests.post(url, headers={'Content-Type': m.content_type}, data=m)
    if response.status_code == 200:
        j_res = response.json()
        facebook_image_id = j_res.get('id')
        print(f"Upload Facebook Image = {imagename}")
        return facebook_image_id
    else:
        print(f"Facebook upload error: {response.text}")


def get_img_link_from_fb_postID(image_id: str, page_id: str, access_token: str):

    """
    This function is fundamental to get the link relatives to the image already published.
    It performs a GET call to Facebook APIs.

    Input:
        image_id: str = the ID of the image to download
        page_id: str = the Facebook Page ID where the image has been published
        access_token: str = the access token obtained after the creation-verification of a Facebook Developer account

    Output:
        Image URL: str = the link pointing to the image

    """

    url = 'https://graph.facebook.com/v13.0/' + page_id + '_' + image_id + '/attachments?access_token=' + access_token

    response = requests.get(url)
    response_json = json.loads(response.content)

    img_url = response_json['data'][0]['media']['image']['src']
    return img_url


def download_and_save_img(img_url: str, img_name_complete: str):

    """
    This function takes the url of the image as input and downloads it, inside a scecif folder.
    It performs a GET call.

    Input:
        image_url: str = the link pointing to the image
        image_name_complete: str = the original image name

    Output:
        None
    """

    img_response = requests.get(img_url)

    img_name_list = img_name_complete.split(".")
    img_name = img_name_list[0]

    cwd = os.getcwd()
    targetPath = cwd + "\Facebook_Download"
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

    targetFile = targetPath + "\\" + img_name
    image = open(targetFile+ '_FB' + '.jpg', "wb")
    image.write(img_response.content)
    image.close()

    print(f"Download Facebook Image = {img_name_complete}")


def delete_img(img_name:str, image_id: str, access_token:str):

    """
    This function deletes the given Facebook image.
    It performs a DELETE call to Facebook APIs.

    Input:
        image_name: str = the original image name
        image_id: str = the ID of the image to delete
    Output:
        True: if the delete call was successful
    """
    url = "https://graph-video.facebook.com/v13.0/" + image_id + "?access_token=" + access_token
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Deleted Facebook Image = {img_name}")
        print("-----------")
        return True


def wrapper(folder:str):

    """
    This is just a wrapper function which iterates over all the images in the given folder, and it iteratively calls all the previous functions.
    
    Input: str = the folder name where the images are saved
    Ouput: None
    """

    with open('credentials.json') as f:
        credentials = json.load(f)
    access_token = credentials['access_token']
    page_id = credentials['page_id']


    for imagename in os.listdir('../' + folder):
        origin_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), folder, imagename])
        destination_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), "Processed", imagename])

        image_id = upload_img(folder, imagename, access_token, page_id)
        image_url = get_img_link_from_fb_postID(image_id, page_id, access_token)
        download_and_save_img(image_url, imagename)

        shutil.move(origin_path, destination_path)
    

    print(f"FINISHED! {folder}")
    return



