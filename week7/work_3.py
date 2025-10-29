import RPi.GPIO as GPIO  
import time               

# 모터 제어 핀 정의
PWMA = 18     # 왼쪽 모터 속도 제어
PWMB = 23     # 오른쪽 모터 속도 제어
AIN1 = 22     # 왼쪽 모터 방향 제어 1
AIN2 = 27     # 왼쪽 모터 방향 제어 2
BIN1 = 25     # 오른쪽 모터 방향 제어 1
BIN2 = 24     # 오른쪽 모터 방향 제어 2

# 각 스위치 핀 번호 설정
SW = [5, 6, 13, 19]

# 스위치의 이전 상태 저장 (0: 안 눌림, 1: 눌림)
lastState = [0, 0, 0, 0]

# GPIO 경고 메시지 비활성화
GPIO.setwarnings(False)
# GPIO 핀 번호 모드를 BCM 방식으로 설정
GPIO.setmode(GPIO.BCM)

# 각 스위치 핀을 입력 모드로 설정하고 풀다운 저항 사용
for pin in SW:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 모터 제어 핀을 출력으로 설정
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 객체 생성 (주파수 500Hz)
L_Motor = GPIO.PWM(PWMA, 500)  # 왼쪽 모터 제어 PWM
R_Motor = GPIO.PWM(PWMB, 500)  # 오른쪽 모터 제어 PWM

# PWM 초기화 (출력 0%)
L_Motor.start(0)
R_Motor.start(0)

try:
    while True:  # 무한 반복
        # 각 스위치의 현재 입력 상태 읽기 (1: 눌림, 0: 안 눌림)
        currentState = [GPIO.input(pin) for pin in SW]

        # SW1 0(안 눌림) -> 1(눌림) 상태로 바뀌면
        if (lastState[0] == 0 and currentState[0] == 1):
            print(f"SW1 클릭: 전진")
            # 두 모터를 정방향 회전
            GPIO.output(AIN1, 0)
            GPIO.output(AIN2, 1)
            GPIO.output(BIN1, 0)
            GPIO.output(BIN2, 1)
            # 양쪽 모터 속도 100%로 동작
            L_Motor.ChangeDutyCycle(100)
            R_Motor.ChangeDutyCycle(100)
            time.sleep(1.0)  # 1초간 전진

            # 모터 정지
            L_Motor.ChangeDutyCycle(0)
            R_Motor.ChangeDutyCycle(0)
            time.sleep(1.0)

        # SW2 0(안 눌림) -> 1(눌림) 상태로 바뀌면
        if (lastState[1] == 0 and currentState[1] == 1):
            print(f"SW2 클릭: 우회전")
            # 왼쪽 모터만 정방향으로 회전 (오른쪽은 정지)
            GPIO.output(AIN1, 0)
            GPIO.output(AIN2, 1)
            L_Motor.ChangeDutyCycle(100)
            time.sleep(1.0)

            # 왼쪽 모터 정지
            L_Motor.ChangeDutyCycle(0)
            time.sleep(1.0)

        # SW3 0(안 눌림) -> 1(눌림) 상태로 바뀌면
        if (lastState[2] == 0 and currentState[2] == 1):
            print(f"SW3 클릭: 좌회전")
            # 오른쪽 모터만 정방향 회전 (왼쪽은 정지)
            GPIO.output(BIN1, 0)
            GPIO.output(BIN2, 1)
            R_Motor.ChangeDutyCycle(100)
            time.sleep(1.0)

            # 오른쪽 모터 정지
            R_Motor.ChangeDutyCycle(0)
            time.sleep(1.0)

        # SW4 0(안 눌림) -> 1(눌림) 상태로 바뀌면
        if (lastState[3] == 0 and currentState[3] == 1):
            print(f"SW4 클릭: 후진")
            # 두 모터를 역방향 회전
            GPIO.output(AIN1, 1)
            GPIO.output(AIN2, 0)
            GPIO.output(BIN1, 1)
            GPIO.output(BIN2, 0)
            L_Motor.ChangeDutyCycle(100)
            R_Motor.ChangeDutyCycle(100)
            time.sleep(1.0)

            # 모터 정지
            L_Motor.ChangeDutyCycle(0)
            R_Motor.ChangeDutyCycle(0)
            time.sleep(1.0)

        # 다음 루프를 위해 현재 상태를 이전 상태 변수에 저장
        for i in range(4):
            lastState[i] = currentState[i]

        # 0.1초 대기
        time.sleep(0.1)

except KeyboardInterrupt:   # Ctrl+C 입력 시 예외 발생
    pass                    # 프로그램 종료 시 아무 동작 없이 넘어감

# 프로그램 종료 시 GPIO 설정 초기화
GPIO.cleanup()