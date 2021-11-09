# ESLab_hw4: Mbed BLE programming - Peripheral

以STM32L4 IoT node 作為 BLE Peripheral, Raspberry Pi 3 為 BLE Central進行溝通，實現Read、Write與Notify功能。

#### Step 1
在client.py中將mac address改為欲連接的裝置，先在 STM32L4 執行 main.cpp，再於 RPi3 執行 client.py

#### Step 2
連線後 client.py 會依序進行：

1. Read (student ID):
Peripheral(STM32L4)傳送學號資訊給 Central(Raspberry Pi 3) (可自行修改傳送內容與長度)

2. Notify (Button state):
原本 STM32L4 的 USER_BUTTON 狀態為 0，當按下按鈕時，狀態變為 1，同時傳送 notification 給 Raspberry Pi 3, client.py 會將訊息 read 出來

3. Write (control LED status):
Raspberry Pi 3 會以一秒一次的頻率交替 write 1 或 0，讓 STM32L4 直接根據接收數值改變 led1 的狀態(1 是亮，0 是暗)，總共六次
(可自行調整頻率與次數)

#### Step 3
完成後結束連線，程式結束
