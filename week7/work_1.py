import RPi.GPIO as GPIO    
import time                 

# 각 스위치 핀 번호 설정
SW = [5, 6, 13, 19]

# 각 스위치의 클릭 횟수를 저장할 리스트 초기화
count = [0, 0, 0, 0]

# 스위치의 이전 상태 저장 (0: 안 눌림, 1: 눌림)
lastState = [0, 0, 0, 0]

# GPIO 경고 메시지 비활성화
GPIO.setwarnings(False)

# GPIO 핀 번호 모드를 BCM 방식으로 설정
GPIO.setmode(GPIO.BCM)

# 각 스위치 핀을 입력 핀으로 설정하고, 풀다운 저항 사용
for pin in SW:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:  # 무한 반복
        # 각 스위치의 현재 입력 상태 읽기 (1: 눌림, 0: 안 눌림)
        currentState = [GPIO.input(pin) for pin in SW]

        # SW1~SW4 검사
        for i in range(4):
            # 이전 상태가 0이고 현재 상태가 1이면
            if (lastState[i] == 0 and currentState[i] == 1):
                count[i] += 1                           # 클릭 횟수 증가
                print(f"('SW{i+1} click', {count[i]})") # 클릭 횟수 출력
            
            # 다음 루프를 위해 현재 상태를 이전 상태로 저장
            lastState[i] = currentState[i]

        # 0.1초 대기
        time.sleep(0.1)

except KeyboardInterrupt:   # Ctrl+C 입력 시 예외 발생
    pass                    # 프로그램 종료 시 아무 동작 없이 넘어감

# 프로그램 종료 시 GPIO 설정 초기화
GPIO.cleanup()