# ------------------------------------------------------------
# CTSTSR-Paddle-Keyer.py
#
# RS-232のCTS（短点）とDSR（長点）信号を2パドルとして利用する、
# Iambic A方式対応のソフトウェアCWキーヤーです。
#
# ・CTSに短点パドル、DSRに長点パドルを接続することで、
#   手動パドルによるCW打鍵が可能になります。
# ・Iambic A方式により、両パドルを同時に押下すると「トー・ツー・トー…」と交互に送信されます。
# ・音声はsounddeviceライブラリでリアルタイムに生成され、位相継続によりクリック音を抑えています。
#
# 動作環境：
#   - Python 3.x
#   - pip install sounddevice numpy pyserial
#   - COMポートは環境に合わせてPORT変数を変更してください。
#
# 備考：
#   - スクイーズ解除はどちらかのパドルを離すことで即座に停止します。
#
# 作成者: 7M4MON
# ------------------------------------------------------------

import serial
import time
import numpy as np
import sounddevice as sd


import serial
import time
import numpy as np
import sounddevice as sd

WPM = 20
DIT = 1.2 / WPM
TONE_FREQ = 600
SAMPLE_RATE = 44100

# 状態フラグ
is_tone_on = False

# グローバル変数
phase = 0.0

def callback(outdata, frames, time_info, status):
    global is_tone_on, phase
    t = (np.arange(frames) + phase) / SAMPLE_RATE
    wave = 0.5 * np.sin(2 * np.pi * TONE_FREQ * t)

    if is_tone_on:
        outdata[:] = wave.reshape(-1, 1).astype(np.float32)
    else:
        outdata[:] = np.zeros((frames, 1), dtype=np.float32)

    # 次の位相用に更新（累積）
    phase += frames


stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=callback
)
stream.start()

# シリアルポート設定
PORT = 'COM101'  # 適宜変更
ser = serial.Serial(PORT)

def paddle_state():
    return ser.cts, ser.dsr  # 短点, 長点

def send_element(duration, symbol):
    global is_tone_on
    print(symbol, end='', flush=True)
    is_tone_on = True
    time.sleep(duration)
    is_tone_on = False
    time.sleep(DIT)  # inter-element space

print("スクイーズ対応キーヤー起動 (Iambic A)")

try:
    while True:
        dit, dah = paddle_state()

        if dit and not dah:
            send_element(DIT, '·')

        elif dah and not dit:
            send_element(DIT * 3, '–')

        elif dit and dah:
            # スクイーズ動作：交互に出す（iambic A）
            while True:
                dit, dah = paddle_state()
                if not (dit and dah):
                    break  # どちらか離したら終了

                send_element(DIT, '·')
                dit, dah = paddle_state()
                if not (dit and dah):
                    break
                send_element(DIT * 3, '–')

        else:
            time.sleep(0.005)

except KeyboardInterrupt:
    print("\n終了")
    stream.stop()
    stream.close()
    ser.close()
