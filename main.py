"""
1. Start session – User activates the collar and begins work.
2. Monitor PC activity – System continuously tracks active window, mouse/keyboard input, and app usage.
3. Check if working in approved apps – If YES, continue monitoring. If NO, proceed to step 4.
4. Detect tab-switching or idle behavior – If user tabs out or goes idle, start warning timer. If still working, loop back to monitoring.
5. Warning timer countdown – Grace period (e.g., 10–30 seconds) before action.
6. Timer expires – If user returns to work before timer ends, pause timer and resume monitoring.
7. Check if user returned to work – After shock, if YES, reset and resume monitoring. If NO, continue to step 8.
8. Extended inattention check – If distraction persists beyond threshold (e.g., 2+ minutes), deliver strong corrective shock.
9. Log activity data – Record all events (shocks, durations, app switches) for reporting.
10. Loop back to monitoring – System returns to step 2 and continues until session ends.
11. Generate report – At session end, compile productivity stats and shock log.
12. End session – User deactivates collar.
"""
import serial
import time

serial_port = 'COM3'
baud_rate = 115200

arduino = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=.1)

def send_command(c: str):
    arduino.write(bytes(c,   'utf-8'))
    arduino.flush()
    print(f'Sent: {c}')

def shock(command: str):
    send_command(command)

# ---- Main ----
is_running = True

while is_running:
    shock_strength: str = input("Enter intensity (L, M, H): ").upper()
    if not shock_strength in ["L", "M", "H"]:
        continue

    do_shock = input("shock (y/n): ")
    if  do_shock == 'y':
        shock(shock_strength)
        do_shock = ''
    else:
        print("closing software...")
        break
