import requests
import random
import user_agent
import secrets
import json
import time

class Gm:
    def __init__(self, email):
        self.email = email
        if "@" in self.email:
            self.email = self.email.split("@")[0]
        self.TL = None
        self.__Host_GAPS = None
        self.base_url = 'https://accounts.google.com/_/signup'
        self.headers = {
            'user-agent': user_agent.generate_user_agent(),
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'x-same-domain': '1',
            'google-accounts-xsrf': '1',
            'accept': '*/*',
            'origin': 'https://accounts.google.com',
            'referer': 'https://accounts.google.com/signup',
        }

    def check(self):
        try:
            # İlk istek - token almak için
            url = self.base_url + '/validatepersonaldetails'
            params = {
                'hl': "en",
                '_reqid': str(random.randint(100000, 999999)),
                'rt': "j"
            }
            
            # Düzeltilmiş payload
            payload = {
                'f.req': json.dumps(["AEThLlymT9V_0eW9Zw42mUXBqA3s9U9ljzwK7Jia8M4qy_5H3vwDL4GhSJXkUXTnPL_roS69KYSkaVJLdkmOC6bPDO0jy5qaBZR0nGnsWOb1bhxEY_YOrhedYnF3CldZzhireOeUd-vT8WbFd7SXxfhuWiGNtuPBrMKSLuMomStQkZieaIHlfdka8G45OmseoCfbsvWmoc7U", "L7N", "", "L7N", "", 0, 0, None, None, None, 0, None, 1, [], 1]),
                'deviceinfo': json.dumps([None, None, None, None, None, "US", None, None, None, "GlifWebSignIn", None, [], None, None, None, None, 1, None, 0, 1, "", None, None, 1, 1, 2])
            }

            # Cookie oluştur
            __Host_GAPS = '1:' + ''.join(secrets.choice("qwertyuiopasdfghjklzxcvbnm0123456789") for _ in range(30))
            cookies = {
                '__Host-GAPS': __Host_GAPS,
                'SOCS': 'CAISHAgCEhJnd3NfMjAyNDA0MDgtMF9SQzIaAmRlIAEaBgiA_LyuBg'
            }

            response = requests.post(
                url, 
                cookies=cookies, 
                params=params, 
                data=payload, 
                headers=self.headers, 
                timeout=10
            )
            
            if response.status_code != 200:
                return {"available": False, "error": "HTTP Error"}

            # Token'ı ayıkla
            try:
                response_data = response.text
                if '",null,"' in response_data:
                    self.TL = response_data.split('",null,"')[1].split('"')[0]
                else:
                    # Alternatif token alma yöntemi
                    import re
                    tl_match = re.search(r'"TL":"([^"]+)"', response_data)
                    if tl_match:
                        self.TL = tl_match.group(1)
                    else:
                        return {"available": False, "error": "Token not found"}
            except:
                return {"available": False, "error": "Token extraction failed"}

            # Kullanıcı adı kontrolü
            url = self.base_url + '/usernameavailability'
            cookies = {'__Host-GAPS': self.__Host_GAPS or __Host_GAPS}
            params = {'TL': self.TL}
            
            data = {
                'f.req': json.dumps([f"TL:{self.TL}", self.email, 0, 0, 1, None, 0, 5167]),
                'deviceinfo': json.dumps([None, None, None, None, None, "US", None, None, None, "GlifWebSignIn", None, [], None, None, None, None, 2, None, 0, 1, "", None, None, 2, 2])
            }

            response = requests.post(
                url, 
                params=params, 
                cookies=cookies, 
                headers=self.headers, 
                data=data, 
                timeout=10
            )

            if response.status_code == 200:
                response_text = response.text
                # Farklı yanıt formatlarını kontrol et
                if '"gf.uar",1' in response_text or '["gf.uar",1' in response_text:
                    return {"available": True}
                elif '"gf.uar",0' in response_text or '["gf.uar",0' in response_text:
                    return {"available": False}
                else:
                    # JSON parsing denemesi
                    try:
                        json_response = json.loads(response_text.replace("'", '"'))
                        if isinstance(json_response, list) and len(json_response) > 0:
                            if json_response[0] == "gf.uar" and json_response[1] == 1:
                                return {"available": True}
                            elif json_response[0] == "gf.uar" and json_response[1] == 0:
                                return {"available": False}
                    except:
                        pass
                    
                    return {"available": False, "error": "Unknown response format"}
            else:
                return {"available": False, "error": f"HTTP {response.status_code}"}

        except requests.exceptions.RequestException as e:
            return {"available": False, "error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"available": False, "error": f"Unexpected error: {str(e)}"}

def gmail_check(email):
    # Basit e-posta formatı kontrolü
    if not email or "@" not in email:
        return {"available": False, "error": "Invalid email format"}
    
    try:
        result = Gm(email=email).check()
        return result
    except Exception as e:
        return {"available": False, "error": f"Check failed: {str(e)}"}

# Test kodu
if __name__ == "__main__":
    test_email = "testusername@gmail.com"
    result = gmail_check(test_email)
    print(f"Result for {test_email}: {result}")
