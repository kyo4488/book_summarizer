DEBUG = False
LENGTH_LIMIT = True

import time
if not DEBUG:
  import sensor
import re
import json

push_count = 0

def extract_last_number(s):
    # 正規表現で文字列の最後にある数字を探す
    match = re.search(r'\d+$', s)
    if match:
        return int(match.group())  # 見つかった場合は整数として返す
    return None  # 見つからなかった場合はNoneを返す

# push__countの読み書き
def update_push_count(new_value):
    with open("push_count.json", "w") as f:
        json.dump({"push_count": new_value}, f)

def get_push_count():
    try:
        with open("push_count.json", "r") as f:
            data = json.load(f)
            return data["push_count"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

#一定時間押されなかったら0に戻す
no_push_count=0

while True:
  if DEBUG:
     response = input()
  else:
    response = sensor.send_command("r A0")
  
  if response.startswith("Analog pin A0 is") and extract_last_number(response) > 100:
    print("plus")
    push_count += 1
    update_push_count(push_count)
    no_push_count=0
  else:
    no_push_count+=1
    if no_push_count>50:
      push_count=0
      update_push_count(push_count)
      no_push_count=0
  
  update_push_count(push_count)
  print("push_count:", push_count)

  time.sleep(0.2)