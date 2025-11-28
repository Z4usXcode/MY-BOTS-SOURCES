import requests, re, os, urllib.parse, random, binascii, uuid, time, secrets, string, json
from MedoSigner import Argus, Gorgon, Ladon, md5

def info(username):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/125.0.6394.70 Mobile Safari/537.36 trill_350402 JsSdk/1.0 NetType/MOBILE Channel/googleplay AppName/trill app_version/35.3.1 ByteLocale/en ByteFullLocale/en Region/IN AppId/1180 Spark/1.5.9.1 AppVersion/35.3.1 BytedanceWebview/d8a21c6",
    }
    try:
        tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=headers).text
        data = json.loads(re.search(
            r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>',
            tikinfo
        ).group(1))

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

def get_info(username):
    if username is None:
        print("Username bulunamadı!")
        return
    
    user_info = info(username)
    
    if not user_info:
        print("No get Info")
        return    

    print(f"""
📌 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 : {user_info['username']}
🧑 𝗡𝗮𝗺𝗲 : {user_info['name']}
🆔 𝗜𝗗 : {user_info['id']}
✅ 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱 : {user_info['verified']}
🔒 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 : {user_info['private']}
📅 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗔𝘁 : {user_info['create_time']}
🎥 𝗩𝗶𝗱𝗲𝗼𝘀 : {user_info['videos']}
👥 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : {user_info['followers']}
➡️ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : {user_info['following']}
❤️ 𝗟𝗶𝗸𝗲𝘀 : {user_info['likes']}
""")
  
    return username
