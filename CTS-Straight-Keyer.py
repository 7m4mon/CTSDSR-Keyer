# ------------------------------------------------------------
# CTS-Straight-Keyer.py
#
# RS-232のCTS信号を縦振れキー入力として利用し、
# パドルを押している間だけサイドトーンをPCのスピーカーから出力するCWキーヤーです。
#
# ・CTS端子にスイッチ（縦振れキー）を接続し、GNDに落とすことでトーンが鳴ります。
# ・音はsounddeviceライブラリを使ってリアルタイムに生成され、
#   位相を連続的に保持することで滑らかなCWトーンを実現しています。
# ・サンプリング周波数やトーン周波数はスクリプト内で変更可能です。
#
# 動作環境：
#   - Python 3.x
#   - pip install sounddevice numpy pyserial
#   - Windows/Linux対応（COMポートは適宜変更）
#
# 作成者: 7M4MON

import serial
import time
import numpy as np
import sounddevice as sd

# 設定
TONE_FREQ = 600     # トーン周波数（Hz）
SAMPLE_RATE = 48000  # サンプリングレート
PORT = 'COM101'     # 使用するシリアルポート

# 状態フラグ
is_tone_on = False
phase = 0.0  # 位相保持

# サイドトーン生成（位相継続）
def callback(outdata, frames, time_info, status):
    global is_tone_on, phase
    t = (np.arange(frames) + phase) / SAMPLE_RATE
    wave = 0.5 * np.sin(2 * np.pi * TONE_FREQ * t)
    if is_tone_on:
        outdata[:] = wave.reshape(-1, 1).astype(np.float32)
    else:
        outdata[:] = np.zeros((frames, 1), dtype=np.float32)
    phase += frames

# ストリーム開始
stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=callback,
    blocksize=256,
    latency='low'
)
stream.start()

# シリアルポート設定
ser = serial.Serial(PORT)

print("縦振れキー対応キーヤー起動（CTSを押している間だけトーン）")

try:
    while True:
        is_tone_on = ser.cts
        time.sleep(0.005)

except KeyboardInterrupt:
    print("\n終了")
    stream.stop()
    stream.close()
    ser.close()
