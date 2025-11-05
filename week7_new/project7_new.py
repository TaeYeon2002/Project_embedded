import RPi.GPIO as GPIO
import threading
import serial
import time
import re   

# 모터 제어 핀
PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

# 블루투스 시리얼 설정
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성
L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)

# PWM 시작
L_Motor.start(0)
R_Motor.start(0)

# 전역 변수
gData = ""
angle = None    # 각도값 저장 변수
last_cmd = "stop"   # 마지막 명령 저장

# 블루투스 수신 스레드 
def serial_thread():
    global gData
    while True:
        data = bleSerial.readline().decode().strip()
        if data:
            gData = data

# 모터 제어 함수
def forward(): # 전진
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(100)
    R_Motor.ChangeDutyCycle(100)

def backward(): # 후진
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(100)
    R_Motor.ChangeDutyCycle(100)

def turn_left(): # 좌회전
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(100)

def turn_right(): # 우회전
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(100)
    R_Motor.ChangeDutyCycle(0)

def stop(): # 정지
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)

# 메인 루프 
def main():
    global gData, last_cmd, angle
    try:
        while True:
            match = re.search(r"J0:(\d+)", gData) # 각도 가져옴
            if match:
                angle = int(match.group(1)) # "J0:" 제외 숫자만 뽑기
                gData = "" # 전역변수 초기화

                # 각도 기준으로 명령 판별
                if angle == 0:
                    cmd = "stop"
                elif (angle >= 315 or angle <= 45):
                    cmd = "right"
                elif 45 < angle <= 135:
                    cmd = "forward"
                elif 135 < angle <= 225:
                    cmd = "left"
                elif 225 < angle <= 315:
                    cmd = "backward"
                else:
                    cmd = "stop"

            else:
                cmd = last_cmd  # 입력 없으면 이전 상태 유지

            # 상태 변경 시에만 동작
            if cmd != last_cmd:
                last_cmd = cmd
                if cmd == "forward":
                    forward()
                    print("전진")
                elif cmd == "backward":
                    backward()
                    print("후진")
                elif cmd == "left":
                    turn_left()
                    print("좌회전")
                elif cmd == "right":
                    turn_right()
                    print("우회전")
                elif cmd == "stop":
                    stop()
                    print("정지")

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:  # 항상 마지막에 멈추고, 연결 끊음
        L_Motor.stop()
        R_Motor.stop()
        GPIO.cleanup()
        bleSerial.close()
        print("프로그램 종료")

# 실행부
if __name__ == '__main__':
    task1 = threading.Thread(target=serial_thread)
    task1.daemon = True
    task1.start()
    main()