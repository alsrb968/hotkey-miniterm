# 시리얼 터미널 프로그램

이 프로그램은 시리얼 통신을 위한 터미널 프로그램으로, 핫키 기능을 지원합니다.

## 기능

- 시리얼 포트 통신
- 커스텀 핫키 지원
- 기본 색상 표시 기능
- 자동 연결 후 콘솔 메시지 표시

## 사용법

### 기본 실행
```bash
python main.py
```
기본 설정으로 실행됩니다 (COM3, 115200 baudrate)

### 옵션 지정
```bash
python main.py -p COM3 -b 115200
```
- `-p, --port`: 시리얼 포트 지정 (기본값: COM3)
- `-b, --baudrate`: 통신 속도 지정 (기본값: 115200)

### 핫키 사용법

1. `ctrl+alt+h`: 사용 가능한 핫키 목록 표시
2. `ctrl+]`: 프로그램 종료 (miniterm 기본)
3. `ctrl+t`: Miniterm 메뉴 (miniterm 기본)

### 설정된 핫키

- `ctrl+alt+1`: adb mode
- `ctrl+alt+2`: host mode
- `ctrl+alt+3`: adb mode always
- `ctrl+alt+4`: host mode always
- `ctrl+alt+5`: master clear
- `ctrl+alt+6`: start Settings
- `ctrl+alt+7`: start All Apps

### 핫키 설정

`hotkeys.json` 파일에서 핫키를 설정할 수 있습니다.

- 예시:
```json
{
    "f1": { // hotkey
        "description": "도움말", // 제목 or 설명
        "command": "help" // 명령어
    },
    "f2": {
        "description": "상태 확인",
        "command": "status"
    }
}
```

## 요구사항

- Python 3.x
- 필요한 패키지:
  - pyserial
  - keyboard

## 설치

필요한 패키지 설치:
```bash
pip install pyserial keyboard
```
