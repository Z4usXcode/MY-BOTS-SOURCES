import requests, re, os, urllib.parse, random, binascii, uuid, time, secrets, string, json
from MedoSigner import Argus, Gorgon, Ladon, md5

def info(username):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6394.70 Mobile Safari/537.36 trill_350402 JsSdk/1.0 NetType/MOBILE Channel/googleplay AppName/trill app_version/35.3.1 ByteLocale/en ByteFullLocale/en Region/IN AppId/1180 Spark/1.5.9.1 AppVersion/35.3.1 BytedanceWebview/d8a21c6",
    }
    try:
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=headers).text
        data = json.loads(re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', tikinfo).group(1))
        user = data['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['user']
        stats = data['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']['stats']
        
        return {
            'id': user['id'],
            'username': user['uniqueId'],
            'name': user['nickname'],
            'verified': user['verified'],
            'private': user['privateAccount'],
            'create_time': time.strftime('%Y-%m-%d', time.localtime(user['createTime'])),
            'videos': stats['videoCount'],
            'followers': stats['followerCount'],
            'following': stats['followingCount'],
            'likes': stats['heartCount']
        }
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

def sign(params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "2.3.1.i18n", sdk_version: int =2, platform: int = 19, unix: int = None):
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
    data=payload
    if not unix: unix = int(time.time())
    return Gorgon(params, unix, payload, cookie).get_value() | { "x-ladon"   : Ladon.encrypt(unix, license_id, aid),"x-argus"   : Argus.get_sign(params, x_ss_stub, unix,platform        = platform,aid             = aid,license_id      = license_id,sec_device_id   = sec_device_id,sdk_version     = sdk_version_str, sdk_version_int = sdk_version)}   

def get_level(username):
    user_info = info(username)
    
    if not user_info:
        print("No get Info")
        return None
    
    url = "https://webcast16-normal-no1a.tiktokv.eu/webcast/user/?request_from=profile_card_v2&request_from_scene=1&target_uid="+str(user_info['id'])+"&iid="+str(random.randint(1, 10**19))+"&device_id="+str(random.randint(1, 10**19))+"&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=300102&version_name=30.1.2&device_platform=android&os=android&ab_version=30.1.2&ssmix=a&device_type=RMX3511&device_brand=realme&language=ar&os_api=33&os_version=13&openudid="+str(binascii.hexlify(os.urandom(8)).decode())+"&manifest_version_code=2023001020&resolution=1080*2236&dpi=360&update_version_code=2023001020&_rticket="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1) + "4632"+"&current_region=IQ&app_type=normal&sys_region=IQ&mcc_mnc=41805&timezone_name=Asia%2FBaghdad&carrier_region_v2=418&residence=IQ&app_language=ar&carrier_region=IQ&ac2=wifi&uoo=0&op_region=IQ&timezone_offset=10800&build_number=30.1.2&host_abi=arm64-v8a&locale=ar&region=IQ&content_language=gu%2C&ts="+str(round(random.uniform(1.2, 1.6) * 100000000) * -1)+"&cdid="+str(uuid.uuid4())+"&webcast_sdk_version=2920&webcast_language=ar&webcast_locale=ar_IQ"	
    
    headers = {'User-Agent': "com.zhiliaoapp.musically/2023001020 (Linux; U; Android 13; ar; RMX3511; Build/TP1A.220624.014; Cronet/TTNetVersion:06d6a583 2023-04-17 QuicVersion:d298137e 2023-02-13)"}
    headers.update(sign(url.split('?')[1], '', "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), None, 1233))    
    try:
        response = requests.get(url, headers=headers)
        level_match = re.search(r'"default_pattern":"(.*?)"', response.text)
        if level_match:
            level_text = level_match.group(1)
            if 'المستوى رقم' in level_text:
                level = level_text.split('المستوى رقم')[1].strip()
            else:
                level = level_text
        else:
            level = "idk"
    except Exception as e:
        print(f"Eroor")
        level = "idk"

    return {
        'id': user_info['id'],
        'username': user_info['username'],
        'name': user_info['name'],
        'verified': user_info['verified'],
        'private': user_info['private'],
        'create_time': user_info['create_time'],
        'videos': user_info['videos'],
        'followers': user_info['followers'],
        'following': user_info['following'],
        'likes': user_info['likes'],
        'level': level
    }

def get_info(username):
    if username is None:
        print("Username bulunamadı!")
        return None
    
    # Level bilgisini al
    level_info = get_level(username)
    
    if not level_info:
        print("No get Info")
        return None

    # Formatlı mesaj oluştur
    result_message = f"""
📌 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 : {level_info['username']}
🧑 𝗡𝗮𝗺𝗲 : {level_info['name']}
🆔 𝗜𝗗 : {level_info['id']}
✅ 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱 : {level_info['verified']}
🔒 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 : {level_info['private']}
📅 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗔𝘁 : {level_info['create_time']}
🎥 𝗩𝗶𝗱𝗲𝗼𝘀 : {level_info['videos']}
👥 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : {level_info['followers']}
➡️ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : {level_info['following']}
❤️ 𝗟𝗶𝗸𝗲𝘀 : {level_info['likes']}
🎮 𝗟𝗲𝘃𝗲𝗹 : {level_info['level']}"""

    print(result_message)
    return result_message
