import RPi.GPIO as GPIO   
import time               

# 각 스위치 핀 번호 설정
SW = [5, 6, 13, 19]
# 부저가 연결된 핀 번호 설정
BUZZER = 12

# 도레미파솔라시도 한 번만 재생하도록 할 변수
OneDo = True

# 스위치의 이전 상태 저장 (0: 안 눌림, 1: 눌림)
lastState = [0, 0, 0, 0]

# GPIO 경고 메시지 비활성화
GPIO.setwarnings(False)
# GPIO 핀 번호 모드를 BCM 방식으로 설정
GPIO.setmode(GPIO.BCM)

# BUZZER 핀을 출력 모드로 설정
GPIO.setup(BUZZER, GPIO.OUT)
# 각 스위치 핀을 입력 모드로 설정하고 풀다운 저항 사용
for pin in SW:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 객체 생성 (BUZZER 핀에 주파수 262Hz)
p = GPIO.PWM(BUZZER, 262)

# 도레미파솔라시도 주파수 배열
DoDo = [262, 294, 330, 349, 392, 440, 494, 523]
# 도레미파 주파수 배열
DoPa = [262, 294, 330, 349]
# 미레미레 주파수 배열
MiRe = [330, 294, 330, 294]
# 도미라솔 주파수 배열
DoSol = [262, 330, 440, 392]
# 파미레도 주파수 배열
PaDo = [349, 330, 294, 262]

# 각 스위치에 대응하는 멜로디를 리스트로 묶기
Melodies = [DoPa, MiRe, DoSol, PaDo]

try:
    while True:  # 무한 반복
        # 각 스위치의 현재 입력 상태 읽기 (1: 눌림, 0: 안 눌림)
        currentState = [GPIO.input(pin) for pin in SW]

        # 프로그램 시작할 때 도레미파솔라시도 재생
        if OneDo:
            for i in DoDo:              # DoDo 리스트의 각 주파수에 대해
                p.ChangeFrequency(i)    # 주파수 변경
                p.start(50)             # duty cycle 50%로 PWM 시작
                time.sleep(0.1)         # 0.1초 동안 유지
            OneDo = False               # 이후 다시 재생되지 않도록 False로 설정
        p.stop()                        # 재생 종료

        # SW1~SW4 검사
        for i in range(4):
            # 이전 상태가 0이고 현재 상태가 1이면
            if (lastState[i] == 0 and currentState[i] == 1):
                for freq in Melodies[i]:  # 해당 스위치의 멜로디 재생
                    p.ChangeFrequency(freq)
                    p.start(50)
                    time.sleep(0.1)
                p.stop()

            # 다음 루프를 위해 현재 상태를 이전 상태 변수에 저장
            lastState[i] = currentState[i]

        # 0.1초 대기
        time.sleep(0.1)

except KeyboardInterrupt:   # Ctrl+C 입력 시 예외 발생
    pass                    # 프로그램 종료 시 아무 동작 없이 넘어감

# 프로그램 종료 시 PWM 정지 GPIO 설정 초기화
p.stop()
GPIO.cleanup()