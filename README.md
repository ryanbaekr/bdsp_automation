# BDSP Automation

This repository contains a few scripts for automating common tasks in Pokemon Brilliant Diamond and Shining Pearl.

This file will contain general information pertaining to the setup while info related to each automation can be found in its corresponding folder.

## Hardware Required

* PC running Windows with access to Python (code may work on other platforms but is untested)
* Nintendo Switch (tested on OLED, should work on all models)
* Raspberry Pi Pico (or clone, hardware diagrams will be based on the [Frood](https://42keebs.eu/shop/parts/controllers/frood-rp2040-pro-micro-controller/))
* USB to UART adapter (hardware diagrams will be based on the Arduino Uno R3 in USB bridge mode)

## Hardware Setup

Flash the Raspberry Pi Pico with the included `SwiCC_RP2040.uf2` file. This file is from knflrpn's SwiCC_RP2040 [repository](https://github.com/knflrpn/SwiCC_RP2040), specifically version 2.2. Then, connect everything following the diagram below.

```
+--------------------+       +--------------------+       +--------------------+       +--------------------+
|                    |       |              Reset |<-+    |                    |       |                    |
|                    |       |                    |  |    |                    |       |                    |
|                    |       |                    |  |    |                    |       |                    |
|                    |       |       Arduino  GND |<-+    |                    |       |                    |
|         PC     USB |<----->| USB     Uno    GND |<----->| GND    Frood   USB |<----->| USB   Switch       |
|                    |       |         R3         |       |                    |       |                    |
|                    |       |                    |       |                    |       |                    |
|                    |       |              1<-TX |<----->| D0                 |       |                    |
|                    |       |              0<-RX |<----->| D1                 |       |                    |
+--------------------+       +--------------------+       +--------------------+       +--------------------+
```

## Software Setup

Install the required Python libraries with the included `requirements.txt` file.

``` bash
pip install -r requirements.txt
```
