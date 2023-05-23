# VolunteerProject #

This project is a part of a larger project providing volunteer assistance to Ukrainian refugees on the territory of the Russian Federation.

The goal of this project is to automate the verification of data for specific individuals in the Volunteer website's lists. 

Volunteer.su is a website where a Russian patriotic initiative group collects and publishes data about military personnel, activists, etc., supporting Ukraine.

Through trial and error, it has been discovered that being listed on the Volunteer website is likely to cause problems for individuals at the border.

If a person or his father is listed on the website, he’d better to be be helped separately from other refugees due to his security and security of others.

Volunteers sometime does not have resourses to check Volunteer.su and this project has been  designed in support.
The automatic verification mode is activated only in strictly defined cases and operates from a local server outside the territory of the Russian Federation.

For security purposes, all data and a chat used for demonstrating the project's functionality is fictional or specially designed and some details are reduced
or changed.


# Motivation

Volunteer.su is a website where a Russian patriotic initiative group collects and publishes data about military personnel, activists, etc., supporting Ukraine.

Through trial and error, it has been discovered that being listed on the Volunteer website is likely to cause problems for individuals at the border.

If a person or his father is listed on the website, he’d better to be be helped separately from other refugees due to his security and security of others.

For security purposes, all data and a chat used for demonstrating the project's functionality is fictional or specially designed and some details are reduced.

# **Guideline**

1. Clone the repository in your folder: git clone https://github.com/Olga-Beliaeva/VolunteerProject.git

2. Install libraries:  pip3 install -r requirements.txt

3. Download Webdriver (see Volunteer_project_Downloading Webdriver.txt for details)

4. Sign in Telegram and manage your App (see Volunteer_project_Signing_In_Telegram.docx for details) 

5. Fill in env.example with api_id and api_hash and rename file to env. 

6. Find https://t.me/voluneer_project and join it

7. Run Volunteer_project_main.py

8. Take a look at https://t.me/voluneer_project


# **Detailed description**

***Volunteer_project_Main.py***

- connects to a specified Telegram chat
- goes through a given range of message ids
- filters relevant messages only
- checks names from filtered messages with Volunteer.su
- messages a result back to a message of origin

***Volunteer_project_Volunteer.py***

Module checks presence of a person and his father on Volunteer.su and
returns a list with found references or an empty list.

***Volunteer_project_Parser.py***

Module filters data by provided fields, clears data by templates and returns data in expected format.

***Volunteer_project_Father_name.py***

Module returns a father's name provided from a person's middle name.

***Volunteer_project_Google_translate_ru_ua.py***

Module returns whether a translated name to Ukrainian or an exception phrase.
Normally we use DeepL API but for demonstration purpose we have replaced DeepL API by Google.

***Volunteer_project_russian_names_men_downloader.py***

Module downloads Russian man names and supports Volunteer_project_Father_name.py

***.env.example***

Provides example of api_id and api_hash


# FYI

for Python < 3.10 “Unexpected exception in the receive loop” may happen during Volunteer_project_main.py run but it does not affect the process

