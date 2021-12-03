import serial
import time
import wiringpi as GPIO
INPUT = 0
OUTPUT = 1
BLED_PIN = 16 # 37
GLED_PIN = 17 # 33
OUTPUT_HIGH = 1
OUTPUT_LOW = 0
ON = 1
OFF = 0
PORT = "/dev/ttyACM4"
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
        ID = b'\x10\x01\x0D\x0A' # ID 설정
        ser.write(ID)
        turnWeakBlue = b'\x20\x02\x0F' # 프로토콜 규칙
        turnWeakBlue += receiveData
        turnWeakBlue += b'\x0D\x0A'
        print('turnWeakBlue',turnWeakBlue)

        cnt = 80 # uart 버퍼가 버티는 빛 보내는 횟수
        while(cnt):
            ser.write(turnWeakBlue)
            time.sleep(0.05) # 한번 보내고 대기하는 시간, 단위 (초)
            cnt -= 1
            print(cnt)
        
        onSendLED()
        receive = True
    except Exception as e:
        print(e)

def receivedData():
    global parsingData
    global receive
    receive = True # 빛을 여러 번 쏘니까 한번만 수신 받기 위함
    
    while(receive):
        if ser.readable(): # 값이 들어왔는지 체크
            Data = ser.readline()
            # print(Data)
            try:
                if Data.startswith(b'Rx >>>'): # UART 개방시 빈 문자열이 들어옴
                # “Rx >>>” 로 시작하는 데이터만 파싱
                # 데이터 파싱
                    onReceivedLED()
                    print("DATA=",Data)
                    parsingData = Data[14:17]
                    parsingData += Data[26:-9]
                    print("parsingData",parsingData)
                    result = parsingData.decode('utf-8') # byte를 str으로 변경하기 위해
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
        GPIO.digitalWrite(BLED_PIN,ON) # LED 켜기
        GPIO.delay(100) # 단위 (ms)
        GPIO.digitalWrite(BLED_PIN,OFF) # LED 끄가
        GPIO.delay(100)
        a -= 1

def onSendLED():
    a=10
    while(a):
        GPIO.digitalWrite(BLED_PIN,ON)
        GPIO.delay(1000)
        GPIO.digitalWrite(BLED_PIN,OFF)
        GPIO.delay(1000)
        a -= 1
        
if __name__=='__main__':
    GPIO.digitalWrite(BLED_PIN,OFF)
    while True:
        try:
            receivedData()
        except Exception as e:
            print(e)
