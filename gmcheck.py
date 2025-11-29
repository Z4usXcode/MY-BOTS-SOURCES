import requests, sys, json
def check_email(email: str) -> bool:
    url = "https://api.fraudemail.com/email";payload = {"email": email};headers = {"User-Agent": "Python","Content-Type":"application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10);data = r.json()
    except Exception as e:
        print("\033[91mAPI ERROR:", e, "\033[0m")
        return False
    print("\n📄 API CEVABI:")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    flags = [
        data.get("exists"),data.get("valid"),data.get("available"),
  data.get("status")]
    
