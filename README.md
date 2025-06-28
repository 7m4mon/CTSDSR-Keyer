# CTSDSR-Keyer

This repository provides two Python-based Morse code (CW) keyer implementations that use RS-232 serial control lines as input paddles. Designed for amateur radio operators, these tools allow simple CW keying using either a straight key or an iambic paddle connected to a PC's serial port.

🔗 GitHub Repository: [7m4mon/CTSDSR-Keyer](https://github.com/7m4mon/CTSDSR-Keyer)

---

## 📁 Files Included

### `CTS-Straight-Keyer.py`

A straight key implementation using the **CTS** line:

- Outputs a sine wave side-tone while the CTS line is held low.
- Designed for traditional "up/down" straight key operation.
- Uses real-time waveform synthesis with phase continuity for clean audio.

### `CTSTSR-Paddle-Keyer.py`

An **Iambic A paddle keyer** using:

- **CTS** for "dit" paddle (·)
- **DSR** for "dah" paddle (–)
- Supports squeeze keying (alternating dit/dah while both pressed).
- Smooth and precise timing of Morse elements.
- No audible clicks thanks to phase-preserving waveform generation.

---

## 🛠 Requirements

Make sure Python 3.x is installed. Then install required packages:

```bash
pip install pyserial sounddevice numpy
```

Tested on both **Windows** and **Linux**.

---

## ⚙ Configuration

Before running, edit each script to match your serial port name:

```python
PORT = 'COM101'      # Windows example
# PORT = '/dev/ttyUSB0'  # Linux example
```

Optional parameters you can modify:

- `TONE_FREQ`: tone frequency in Hz (default: 600 Hz)
- `SAMPLE_RATE`: audio output rate (default: 48000 or 44100)
- `WPM`: words per minute (only in paddle keyer)

---

## 🔌 Hardware Setup

- Use a USB-to-Serial adapter with accessible CTS and DSR lines.
- Connect your straight key or paddle so that pressing closes the line to GND.
- No data is transmitted over the serial line—only control signals are read.

**Pin Usage**:

| Signal | Function         |
|--------|------------------|
| CTS    | Straight key / Dit |
| DSR    | Dah paddle (for iambic) |

---

## 📷 Example Use Cases

- CW practice or training on your PC
- USB paddle interface for SDR
- Side-tone generator for code keying
- CW to SSB modulation gateway (when paired with audio input)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙋 Author

Developed by **7M4MON**

Feel free to fork, modify, or integrate with your own amateur radio tools.  
Pull requests are welcome!