import requests
import os
import time

USERNAME = os.environ.get("YEMOT_USERNAME")
PASSWORD = os.environ.get("YEMOT_PASSWORD")
SOURCE_FOLDER = "ivr2:/Trash/Messages" 
DESTINATION_FOLDER = "ivr2:/4"

def check_and_move():
    try:
        login_url = "https://www.call2all.co.il/ym/api/Login"
        login_response = requests.get(login_url, params={"username": USERNAME, "password": PASSWORD}).json()
        
        if login_response.get("responseStatus") == "OK":
            token = login_response.get("token")
            
            dir_url = "https://www.call2all.co.il/ym/api/GetIVR2Dir"
            dir_response = requests.get(dir_url, params={"token": token, "path": SOURCE_FOLDER}).json()
            
            if dir_response.get("responseStatus") == "OK":
                files = dir_response.get("files", [])
                wav_files = [f["name"] for f in files if f["name"].endswith(".wav")]
                
                if wav_files:
                    for file_name in wav_files:
                        action_url = "https://www.call2all.co.il/ym/api/FileAction"
                        action_params = {
                            "token": token,
                            "action": "move",
                            "what": f"{SOURCE_FOLDER}/{file_name}",
                            "target": DESTINATION_FOLDER
                        }
                        requests.get(action_url, params=action_params)
    except Exception:
        pass

# הרובוט מתעורר ומבצע 9 בדיקות (כל 30 שניות) לאורך 4.5 דקות סה"כ
for i in range(9):
    check_and_move()
    if i < 8: # בפעם האחרונה אין צורך לישון, כי הרובוט מסיים
        time.sleep(30)
