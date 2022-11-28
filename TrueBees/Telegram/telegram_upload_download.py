import telegram
import json
import os
import pathlib
import shutil



def wrapper(folder):

    """
    This is a wrapper which iterates over all the images inside the given folder, and automatically performs the UPLOAD-DOWNLOAD steps.
    It performs a POST and a GET calls to the Telegram Bot.as_view

    Input: folder: str = the folder name which contains the images to process
    Output: None
    """

    with open('credentials.json') as f:
        credentials = json.load(f)
    token = credentials['token']
    chat_id = credentials['chat_id']  # id of the sender (myself)
    bot = telegram.Bot(token)

    if not os.path.exists('./DownloadedImages/' + folder):
        os.makedirs('./DownloadedImages/' + folder)

    for imagename in os.listdir('../' + folder):

        origin_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), folder, imagename])
        destination_path = "\\".join(["\\".join(str(pathlib.Path(__file__).parent.resolve()).split('\\')[:-1]), "Processed", imagename])

        while True:
            try:
                print("----------")

                #UPLOAD step
                image = bot.send_photo(chat_id, photo=open('../' + folder + '/' + imagename, 'rb'), filename=imagename.split('.')[0])
                print(f"Upload Telegram Image = {imagename}")

                #DOWNLOAD step
                file = bot.get_file(image['photo'][2]['file_id'])
                file.download('./DownloadedImages/' + folder + '/' + imagename.split('.')[0] + '_TL' + '.jpeg')
                print(f"Download Telegram Image = {imagename}")
                break

            except telegram.error.TimedOut:
                continue

        shutil.move(origin_path, destination_path)

    print(f"FINISHED! {folder}")
    return
    

