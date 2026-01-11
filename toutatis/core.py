import argparse
import requests
from urllib.parse import quote_plus
from json import dumps, decoder
import re

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
import pycountry


def getUserId(username, sessionsId):
    headers = {"User-Agent": "iphone_ua", "x-ig-app-id": "936619743392459"}
    api = requests.get(
        f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}',
        headers=headers,
        cookies={'sessionid': sessionsId}
    )
    try:
        if api.status_code == 404:
            return {"id": None, "error": "User not found"}

        id = api.json()["data"]['user']['id']
        return {"id": id, "error": None}

    except decoder.JSONDecodeError:
        return {"id": None, "error": "Rate limit"}


def getInfo(search, sessionId, searchType="username"):
    if searchType == "username":
        data = getUserId(search, sessionId)
        if data["error"]:
            return data
        userId = data["id"]
    else:
        try:
            userId = str(int(search))
        except ValueError:
            return {"user": None, "error": "Invalid ID"}

    try:
        response = requests.get(
            f'https://i.instagram.com/api/v1/users/{userId}/info/',
            headers={'User-Agent': 'Instagram 64.0.0.14.96'},
            cookies={'sessionid': sessionId}
        )
        if response.status_code == 429:
            return {"user": None, "error": "Rate limit"}

        response.raise_for_status()

        info_user = response.json().get("user")
        if not info_user:
            return {"user": None, "error": "Not found"}

        info_user["userID"] = userId
        return {"user": info_user, "error": None}

    except requests.exceptions.RequestException:
        return {"user": None, "error": "Not found"}


def advanced_lookup(username):
    """
        Post to get obfuscated login infos
    """
    data = "signed_body=SIGNATURE." + quote_plus(dumps(
        {"q": username, "skip_recovery": "1"},
        separators=(",", ":")
    ))
    api = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            # "X-FB-HTTP-Engine": "Liger",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )

    try:
        return ({"user": api.json(), "error": None})
    except decoder.JSONDecodeError:
        return ({"user": None, "error": "rate limit"})


def main():
    parser = argparse.ArgumentParser(epilog="Example: toutatis -u vlad_leonov7 -s <sessionid>")
    parser.add_argument('-s', '--sessionid', help="Instagram session ID", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--username', help="One username")
    group.add_argument('-i', '--id', help="User ID")
    args = parser.parse_args()

    sessionsId = args.sessionid
    # Common mistake: using the literal 'username' placeholder; give a helpful hint
    if args.username and args.username.lower() == 'username':
        print("It looks like you used the literal 'username' placeholder. Replace it with the real username.")
        print("Example: toutatis -u vlad_leonov7 -s <your_sessionid_here>")
        return

    # Validate sessionid argument superficially to catch common user errors
    def looks_like_username(s: str) -> bool:
        return bool(re.match(r'^[A-Za-z0-9_.]+$', s)) and len(s) <= 30

    def looks_like_sessionid(s: str) -> bool:
        # sessionid commonly contains digits, colons, or URL-encoded chars; check for those patterns
        return bool(re.search(r'[:%]|[0-9]{6,}', s)) and len(s) >= 8

    if sessionsId.lower() in ('<sessionid>', '<instagramsessionid>'):
        print("It looks like you left the sessionid placeholder. Replace it with your real sessionid cookie value.")
        print("Example: toutatis -u vlad_leonov7 -s <your_sessionid_here>")
        return

    if looks_like_username(sessionsId) and not looks_like_sessionid(sessionsId):
        print("The value passed to -s looks like a username (e.g., 'vlad_leonov'). Did you swap -u and -s?")
        print("Correct usage: toutatis -u vlad_leonov7 -s <your_sessionid_here>")
        return

    search_type = "id" if args.id else "username"
    search = args.id or args.username
    infos = getInfo(search, sessionsId, searchType=search_type)
    if not infos.get("user"):
        exit(infos["error"])

    infos = infos["user"]

    print("Informations about     : " + infos["username"])
    print("userID                 : " + infos["userID"])
    print("Full Name              : " + infos["full_name"])
    print("Verified               : " + str(infos['is_verified']) + " | Is buisness Account : " + str(
        infos["is_business"]))
    print("Is private Account     : " + str(infos["is_private"]))
    print(
        "Follower               : " + str(infos["follower_count"]) + " | Following : " + str(infos["following_count"]))
    print("Number of posts        : " + str(infos["media_count"]))
    # print("Number of tag in posts : "+str(infos["following_tag_count"]))
    if infos.get("external_url"):
        print("External url           : " + infos["external_url"])
    print("IGTV posts             : " + str(infos["total_igtv_videos"]))
    print("Biography              : " + (f"""\n{" " * 25}""").join(infos["biography"].split("\n")))
    print("Linked WhatsApp        : " + str(infos["is_whatsapp_linked"]))
    print("Memorial Account       : " + str(infos["is_memorialized"]))
    print("New Instagram user     : " + str(infos["is_new_to_instagram"]))

    if "public_email" in infos.keys():
        if infos["public_email"]:
            print("Public Email           : " + infos["public_email"])

    if "public_phone_number" in infos.keys():
        if str(infos["public_phone_number"]):
            phonenr = "+" + str(infos["public_phone_country_code"]) + " " + str(infos["public_phone_number"])
            try:
                pn = phonenumbers.parse(phonenr)
                countrycode = region_code_for_country_code(pn.country_code)
                country = pycountry.countries.get(alpha_2=countrycode)
                phonenr = phonenr + " ({}) ".format(country.name)
            except phonenumbers.NumberParseException:
                pass
            print("Public Phone number    : " + phonenr)

    other_infos = advanced_lookup(infos["username"])

    if other_infos["error"] == "rate limit":
        print("Rate limit please wait a few minutes before you try again")

    elif "message" in other_infos["user"].keys():
        if other_infos["user"]["message"] == "No users found":
            print("The lookup did not work on this account")
        else:
            print(other_infos["user"]["message"])

    else:
        if "obfuscated_email" in other_infos["user"].keys():
            if other_infos["user"]["obfuscated_email"]:
                print("Obfuscated email       : " + other_infos["user"]["obfuscated_email"])
            else:
                print("No obfuscated email found")

        if "obfuscated_phone" in other_infos["user"].keys():
            if str(other_infos["user"]["obfuscated_phone"]):
                print("Obfuscated phone       : " + str(other_infos["user"]["obfuscated_phone"]))
            else:
                print("No obfuscated phone found")
    print("-" * 24)
    hd = infos.get("hd_profile_pic_url_info")
    if hd and hd.get("url"):
        print("Profile Picture        : " + hd["url"])

        toutatis -u vlad_leonov7
        

