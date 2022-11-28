# TrueBees project (Data Entry)
Python scripts to Upload-Download images on Social Media (Facebook, WhatsApp, Twitter, Telegram)
To process the images, it is first necessary to copy the folder containing them inside the **Code** directory of this repository.

## Facebook
The APIs used for this social are those officially supported from Facebook, called Facebook GraphAPI.
* Download: download is possible through the “fb-down” library that downloads images using their URLs. To automate the operation, a Python script was made that implements GraphAPI calls to get the URLs of the uploaded videos.
* Upload: as for the upload there are no libraries that implement working Graph APIs, consequently it was necessary to write independently the code to make the requests to endpoints. To this end, it is necessary to have: 
  * Authentication token (only available after creating a developer account and consequent verification by phone number) 
  * Id of a public Facebook page, with permissions enabled (“pages show list”, “pages read engagement”, “pages manage posts”, which can be activated through the Facebook developer dashboard).

Here I provide the required fields to copy inside the **credentials.json** file. These are available after that a Facebook Developer account has been created.

```
"access_token" : "EAA****cZD"
"page_id": "11**84"
"app_id": "50**11"
"app_secret": "e41**90f"
```
We recommend generating an Access Token with a longer duration than the default one. To do so, it is necessary to execute the createLongLivedToken.py script. After that, a new token will be produced, which you will have to copy inside the "access_token" field of the **credentials.json** file.

## WhatsApp
Please refer to this Medium article on how to use [WhatsApp Cloud API](https://medium.com/@today.rafi/whatsapp-cloud-api-how-to-send-whatsapp-messages-from-python-9baa03c93b5d)

**credentials.json** required files:
```
"phone_number_ID": "10**50"
"access_token": "EA**nE"
```
The Access Token expires after 24 hours after it was generated. So you will have to produce a new one after that period. This can easily be done inside the Facebook (WhatsApp) Developer dashboard.

## Twitter
* Download: The “Tweepy” library allows you to download images. The necessary tools are:
  * Developer account with verified phone number
   * Access Token, Access Token Secret, API secret key (automatically generated and present in the developer dashboard)
* Upload: the same “Tweepy” library was used to upload the images.

**credentials.json** required files:
```
"API_key": "3F**5v",
"API_secret_key": "82**tf",
"Bearer Token": "AA**Ya",
"Access_token": "15**BH",
"Access_token_secret": "99**2c",
"App ID": "2**3",
"Account Name": "@AccountName",
"Client ID": "eF**aQ",
"Client Secret": "Ge**DB"
```


## Telegram
* Download: The library used is “python-telegram-bot”. This is a wrapper of the Telegram bot API. To automate the loading it was necessary to:
  * create a bot, and get the access endpoint for the bot
  * get a “chat-id”, which is an id that identifies an active telegram user
* Upload: The upload takes place with the same library. When uploading a file, a “file-id” is generated, that is a unique identifier of the image just uploaded. Through this id, downloading is then possible.

**credentials.json** required files:
```
"token": "53**4A",
"chat_id": "9**5",
"access_point": "https://web.telegram.org/z/#53**64"
```




