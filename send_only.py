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
ser = serial.Serial(PORT, BaudRate,
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
GPIO.pinMode(GLED_PIN, OUTPUT)
GPIO.pinMode(BLED_PIN,OUTPUT)

# def sendData(receiveData):
print(ser.portstr) #연결된 포트 확인.

def sendData():
    global turnStrongBlue
    # ID 설정
    ID = b'\x10\x01\x0D\x0A'
    ser.writelines(ID)
    # if ser.readable(): # 값이 들어왔는지 체크
    ser.timeout = 1 
     #입력방식1
    print(ser.read(ser.inWaiting()))
    # 약한 파란신호
    # print(receiveData)
    # turnWeakBlue = b'\x20\x02\x0F\x1F\xAA\xBB\xCC\xDD\xEE\xFF\x0D\x0A'
    receiveData = b'\x1F\xAA\xBB\xCC\xDD\xEE\xFF'

    # turnWeakBlue = b'\x20\x02 0F 1F AA BB CC DD EE FF 0D 0A'
    # turnWeakBlue = b'\x30\x02\x0F 1F AA BB CC DD EE FF 0D 0A'
    # print(turnWeakBlue)
    # ser.write(turnWeakBlue) 
    # # 쎈 파란신호
    turnWeakBlue = b'\x20\x02\x0F'
    # turnWeakBlue = b'\x30\x02\x0F'
    # # print(turnStrongBlue)
    # # print('bytearray(hex(parsingData)) = ', bytearray(hex(parsingData)))
    # # turnStrongBlue += bytearray(hex(parsingData))
    # # turnStrongBlue += parsingData
    # for i in receiveData:
    #     addData = ''
    #     addData += '0x'+i
    #     print(addData)
    #     turnWeakBlue += addData
    # print("receive",receiveData)
    turnWeakBlue += receiveData
    turnWeakBlue += b'\x0D\x0A'
    print('turnWeakBlue',turnWeakBlue)
    # ser.write(turnStrongBlue)
    # ser.write(bytearray(turnStrongBlue))
    # while
    cnt = 10 # uart 버퍼가 버티는 최대 범위
    while(cnt):
        ser.write(turnWeakBlue)
        time.sleep(0.005) # 최대 속도 
        cnt -= 1
        # print(cnt)
    onSendLED()

def receiveData():
    global parsingData
    receive = True
    realData =''
    while(receive):
        if ser.readable(): # 값이 들어왔는지 체크
            Data = ser.readline()
            # print(Data)
            if Data.startswith(b'Rx >>>'): # UART 개방시 빈 문자열이 계속해서 들어옴
            # 데이터 파싱
                print("DATA=",Data)
                parsingData = Data[14:17]
                parsingData += Data[26:-9]
                print("parsingData",parsingData)
                result = parsingData.decode('utf-8')
                # parsingData = hexData.split()
                print("result",result)
                dataTohex = bytes.fromhex(result)
                print("dataTohex ",dataTohex)
                # byte_array = bytes(parsingData)
                # print(bytearray)
                receive = False
                time.sleep(3) # 수신받은 보내기 전 10초 대기
                sendData(dataTohex)
        # onSendLED() 

def onSendLED():
#     global cnt_switch
    a=10
    while(a):
        GPIO.digitalWrite(BLED_PIN,ON)
        GPIO.delay(500)
        GPIO.digitalWrite(BLED_PIN,OFF)
        GPIO.delay(500)
        a -= 1
        

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

    
# def offLED():
#     GPIO.digitalWrite(LED_PIN,0)

# def switch():
#     if GPIO.digitalRead(SWITCH_PIN):
#         print("스위치 연결")
#         onSendLED()
#     else:
#         print("스위치 닫힘")
#         offLED()
    
# # def offSendLED():
# # def onReceiveLED():
# # def offReceiveLED():
# tOnSendLed = threading.Thread(target = onSendLED)
# tCheckSwitch = threading.Thread(target = checkSwitch)
# tOnSendLed.start()
# tCheckSwitch.start()

# checkSwitch()
# receiveData()

if __name__=='__main__':
    GPIO.digitalWrite(BLED_PIN,OFF)
    # while True:
    #     receiveData()
    sendData()
    # ser.locse()
    # onSendLED()
    ser.close()