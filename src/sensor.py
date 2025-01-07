import serial
import time

# Arduinoのシリアルポートとボーレートを設定
arduino_port = "/dev/cu.usbmodem101"  # 使用しているポートを指定
baud_rate = 9600       # Arduinoスケッチと一致するボーレート

# シリアル通信を初期化
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Arduinoがリセットされるため、接続の安定を待つ

# コマンドを送信して応答を取得する関数
def send_command(command):
    ser.write((command + "\n").encode())  # コマンドを送信
    print(f"Sent: {command.strip()}")

    # Arduinoからの応答を受信
    response = ser.readline().decode().strip()
    print(f"Arduino responded: {response}")
    return response

# 実行例
if __name__ == "__main__":
    try:
        # アナログピンA0の値を読み取る
        send_command("r A0")

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        ser.close()