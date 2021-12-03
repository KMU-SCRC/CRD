from os import readlink
import serial
import time
import threading
import wiringpi as GPIO
INPUT = 0
OUTPUT = 1
BLED_PIN = 16 # 37
GLED_PIN = 17 # 33
# SWITCH_PIN = 5# 39
OUTPUT_HIGH = 1
OUTPUT_LOW = 0
ON = 1
OFF = 0
PORT = "/dev/ttyACM11"
BaudRate = 115200
cnt_switch = 0
parsingData = ""
GPIO.wiringPiSetup() # wpi 기준으로 pin qjsghrk 매겨짐
ser = serial.Serial(PORT, BaudRate, timeout=3)
# GPIO.pinMode(SWITCH_PIN, INPUT)
GPIO.pinMode(GLED_PIN, OUTPUT)
GPIO.pinMode(BLED_PIN,OUTPUT)

def sendData(receiveData):
    try:
        global receive
        # ID 설정
        ID = b'\x10\x01\x0D\x0A'
        ser.write(ID)
        # 약한 파란신호
        # print(receiveData)
        # turnWeakBlue = b'\x20\x02\x0F\x1F\xAA\xBB\xCC\xDD\xEE\xFF\x0D\x0A'

        # turnWeakBlue = b'\x20\x02 0F 1F AA BB CC DD EE FF 0D 0A'
        # turnWeakBlue = b'\x30\x02\x0F 1F AA BB CC DD EE FF 0D 0A'
        # print(turnWeakBlue)
        # ser.write(turnWeakBlue) 
        # # 쎈 파란신호
        turnWeakBlue = b'\x20\x02\x0F'
        print("receive",receiveData)
        turnWeakBlue += receiveData
        turnWeakBlue += b'\x0D\x0A'
        print('turnWeakBlue',turnWeakBlue)
        # ser.write(turnStrongBlue)
        # ser.write(bytearray(turnStrongBlue))
        # while
        cnt = 80 # uart 버퍼가 버티는 최대 범위
        while(cnt):
            ser.write(turnWeakBlue)
            time.sleep(0.05) # 최대 속도 
            cnt -= 1
            print(cnt)
        
        onSendLED()
        receive = True
    except Exception as e:
        print(e)

def receiveData():
    global parsingData
    global receive
    receive = True
    realData =''
    while(receive):
        if ser.readable(): # 값이 들어왔는지 체크
            Data = ser.readline()
            # print(Data)
            try:
                if Data.startswith(b'Rx >>>'): # UART 개방시 빈 문자열이 계속해서 들어옴
                # 데이터 파싱
                    onReceivedLED()
                    print("DATA=",Data)
                    parsingData = Data[14:17]
                    parsingData += Data[26:-9]
                    print("parsingData",parsingData)
                    result = parsingData.decode('utf-8')
                    print("result",result)
                    dataTohex = bytes.fromhex(result)
                    print("dataTohex ",dataTohex)
                    receive = False
                    time.sleep(10) # 수신받은 보내기 전 10초 대기
                    sendData(dataTohex)
            except Exception as e:
                print(e)

def onReceivedLED():
    a=10
    while(a):
        GPIO.digitalWrite(BLED_PIN,ON)
        GPIO.delay(100)
        GPIO.digitalWrite(BLED_PIN,OFF)
        GPIO.delay(100)
        a -= 1
        
def onSendLED():
    GPIO.digitalWrite(BLED_PIN,ON)
    GPIO.delay(10000)
    GPIO.digitalWrite(BLED_PIN,OFF)
    # GPIO.delay(500)
        

# def checkSwitch():
#     # global cnt_switch
#     # print(cnt_switch)
#     while(True):
#         print(GPIO.digitalRead(SWITCH_PIN))
#         if GPIO.digitalRead(SWITCH_PIN):
#         #      # 눌렸을 때 1
#         #     # cnt_switch += 1
#         #     # print("눌림",cnt_switch)
#             GPIO.digitalWrite(LED_PIN,ON)
#         else:
#         #     # print("안눌림",cnt_switch)
#             GPIO.digitalWrite(LED_PIN,OFF)
#             # pass

    

if __name__=='__main__':
    GPIO.digitalWrite(BLED_PIN,OFF)
    while True:
        receiveData()