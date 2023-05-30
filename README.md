# VolunteerProject

This project is a part of a larger project providing volunteer assistance to Ukrainian refugees on the territory of the Russian Federation.

The goal of this project is to automate the verification of data for specific individuals in the Volunteer website's lists.

Volunteer.su is a website where a Russian patriotic initiative group collects and publishes data about military personnel, activists, etc., supporting Ukraine.

Through trial and error, it has been discovered that being listed on the Volunteer website is likely to cause problems for individuals at the border.

If a person or his father is listed on the website, he’d better to be be helped separately from other refugees due to his security and security of others.

The checking chat has been launched for this purpose. The checking prosidure is following:

- a messege with a hash tag #check is automaticaly sent to the checking chat

- a message goes through a checking process at the set time:

  - a person's full name + his father first name and surname (specially modeled) are checking with Volunteer.su

- a result is returning to a sender by a hash tag #verdict

For security purposes, all data and a chat used for demonstrating the project's functionality is fictional or specially designed and some details are reduced
or changed.

# Motivation

Volunteer.su is a website where a Russian patriotic initiative group collects and publishes data about military personnel, activists, etc., supporting Ukraine.

Through trial and error, it has been discovered that being listed on the Volunteer website is likely to cause problems for individuals at the border.

If a person or his father is listed on the website, he’d better to be be helped separately from other refugees due to his security and security of others.

For security purposes, all data and a chat used for demonstrating the project's functionality is fictional or specially designed and some details are reduced.

# **Guideline**

1. Clone the repository in a project folder: git clone https://github.com/Olga-Beliaeva/VolunteerProject.git

2. Download Python 3.11 (*FYI #1)

3. Install libraries into the project environment:  pip3 install -r requirements.txt

4. Download Webdriver (see Volunteer_project_Downloading Webdriver.txt for details)

5. Sign in Telegram and manage your App (see Volunteer_project_Signing_In_Telegram.docx for details)

6. Fill in env.example with api_id and api_hash and rename env.example to env.

7. Join to https://t.me/voluneer_project by link https://t.me/+mcHh1q39NCo4Yjhh

8. Run Volunteer_project_Main.py

9. Enter your phone number (the one registred in 4.)  and a code you received

10. Take a look at https://t.me/voluneer_project


# **Detailed description**

***Volunteer_project_Main.py***

- connects to a specified Telegram chat
- goes through a given range of message ids
- filters relevant messages only
- checks names from filtered messages with Volunteer.su
- messages a result back to a message of origin

***Volunteer_project_Volunteer.py (v1) | Volunteer_project_Volunteer_with_requests.py (v2)***

Module checks presence of a person and his father (v1 only) on Volunteer.su and
returns a message with found references.

v2 set by default

***Volunteer_project_Parser.py***

Module filters data by provided fields, clears data by templates and returns data in expected format.

***Volunteer_project_Father_name.py***

/valid for v1 only/

Module returns a father's name provided from a person's middle name.

***Volunteer_project_Google_translate_ru_ua.py***

/valid for v1 only/

Module returns whether a translated name to Ukrainian or an exception phrase.
Normally we use DeepL API but for demonstration purpose we have replaced DeepL API by Google.

***Volunteer_project_russian_names_men_downloader.py***

Module downloads Russian man names and supports Volunteer_project_Father_name.py

***.env.example***

Provides example of api_id and api_hash


# FYI

1. for Python < 3.10 “Unexpected exception in the receive loop” may happen during Volunteer_project_Main.py run but it should not affect the process

2. while running v1, you may incounter with
ERROR: Couldn't read tbsCertificate as SEQUENCE
ERROR: Failed parsing Certificate
here you may find a solution:
https://stackoverflow.com/questions/75771237/error-parsing-cert-retrieved-from-aia-as-der-error-couldnt-read-tbscertifi/75772763#75772763

3. If you are experiensing a kind of you-do-not-have-rights-sending-message-to-this-group problem while message back to https://t.me/voluneer_project, try following:

- run Volunteer_project_Find_id.py

- find id of https://t.me/voluneer_project

- replace all https://t.me/voluneer_project by its id in Volunteer_project_Main.py