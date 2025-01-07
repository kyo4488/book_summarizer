import time
import sensor
import summarize
import re

def extract_last_number(s):
    # 正規表現で文字列の最後にある数字を探す
    match = re.search(r'\d+$', s)
    if match:
        return int(match.group())  # 見つかった場合は整数として返す
    return None  # 見つからなかった場合はNoneを返す

while True:
  response = sensor.send_command("r A0")
  if response.startswith("Analog pin A0 is") and extract_last_number(response) > 100:
      summarize.summarize()
      time.sleep(10)

  time.sleep(1)