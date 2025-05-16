import serial
from serial.tools import miniterm
import keyboard
import threading
import json
import os
import argparse

def load_json_file(filename):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, filename)
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load {filename}: {e}")
        return {}

def parse_args():
    parser = argparse.ArgumentParser(description='Serial Terminal with Hotkeys')
    parser.add_argument('-p', '--port', default='COM3',
                      help='Serial port (default: COM3)')
    parser.add_argument('-b', '--baudrate', type=int, default=115200,
                      help='Baudrate (default: 115200)')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 핫키 설정 로드
    HOTKEYS = load_json_file('hotkeys.json')

    ser = serial.serial_for_url(args.port, baudrate=args.baudrate, timeout=1)
    mt = miniterm.Miniterm(ser)

    # 필수 설정
    mt.set_rx_encoding('UTF-8')
    mt.set_tx_encoding('UTF-8')

    # EOL 설정
    mt.eol = 'lf'

    # 필터 설정
    mt.filters = ['colorize']

    # 종료 문자 설정 (Ctrl+])
    mt.exit_character = chr(0x1d)  # GS/CTRL+]

    # 핫키 설정
    def setup_hotkeys():
        def send_command(command, hotkey_info=None):
            if not ser.is_open:
                return
                
            if hotkey_info:
                print(f"\n[Hotkey] {hotkey_info['key']} : {hotkey_info['description']}")
                
            if isinstance(command, (list, tuple)):
                # 여러 명령어 처리
                for cmd in command:
                    send_single_command(cmd)
            else:
                send_single_command(command)
        
        def send_single_command(command):
            if isinstance(command, str):
                # 문자열 처리
                if command:  # 빈 문자열 제외
                    ser.write(command.encode())
                    ser.write(b'\n')
            else:
                # 바이트 데이터는 그대로 전송하고 개행 추가
                ser.write(command)
                ser.write(b'\n')
        
        def show_hotkeys():
            print("\n\n=== Available Hotkeys ===")
            for key, value in HOTKEYS.items():
                print(f"{key.lower()} : {value['description']}")
            print("ctrl+alt+h : Show this help")
            print("ctrl+]     : Exit program")
            print("ctrl+t     : Miniterm menu")
            print("=======================\n")
        
        keyboard.add_hotkey('ctrl+alt+h', show_hotkeys)
        for key, value in HOTKEYS.items():
            hotkey_info = {'key': key.lower(), 'description': value['description']}
            keyboard.add_hotkey(key, lambda v=value, info=hotkey_info: 
                send_command(v['command'], info))

    # 연결 정보 출력
    print(f"\nConnected to {args.port} at {args.baudrate} baud")
    
    # 연결 후 엔터 전송
    ser.write(b'\n')

    # 핫키 스레드 시작
    threading.Thread(target=setup_hotkeys, daemon=True).start()

    mt.start()

    try:
        mt.join(True)
    except KeyboardInterrupt:
        pass
    finally:
        mt.join(False)
        mt.close()

if __name__ == "__main__":
    main()
