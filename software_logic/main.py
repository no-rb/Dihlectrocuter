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
import pygetwindow as gw
import serial
import time

# NOTE: Initialize Arduino code and functionality
serial_port = 'COM3'
baud_rate = 115200

try:
    arduino = serial.Serial(port=serial_port, baudrate=baud_rate, timeout=0.1)
    print(f"Connected to {serial_port}")
except serial.SerialException as e:
    print(f"Couldn't connect to Arduino: {e}")
    arduino = None

def send_command(c: str):
    if arduino:
        arduino.write(bytes(c,   'utf-8'))
        arduino.flush()
        print(f'Sent: {c}')

def shock(command: str):
    send_command(command)

# NOTE: Initialize window check code and functionality
banned_tabs = [
    "youtube",
    "github",
    "tiktok" #victor...
    "discord",
    "twitch",
    "e621"
    "sendou"
]

def check_active_tab(activeWindow: gw.Win32Window | None, tabList: list[str]) -> bool:
    if activeWindow == None:
        return False

    window_title_lower = activeWindow.title.lower()

    for tab in tabList:
        if activeWindow and tab in window_title_lower:
            print(f'{tab} is open!')
            return True

    return False

# ---- Main ----
def Main():
    # NOTE: Timer system implemantation:
    #       When the program is ran:
    #       - Setup (~DONE)
    #           - Init timer at X seconds (DONE)
    #           - Shock strength selection (DONE)
    #           - (maybe) Select which tabs are bad (not needed)
    #       - Loop (DONE)
    #           - Detect bad tabs from monitoring
    #               - Decrease timer by 1 seconds
    #           - Timer reaches
    #               - SHOCK THAT MF'er (strength determined in settings)
    #           - Reset timer

    is_running = True

    # End if no arduino is connected
    if arduino == None:
        return

    # Get settings input from user
    timer_start_value = int(input("Set the timer (in seconds): "))

    shock_timer = timer_start_value
    shock_strength: str = input("Enter intensity (L, M, H): ").upper()
    while not shock_strength in ["L", "M", "H"]:
        shock_strength: str = input("Enter intensity (L, M, H): ").upper()

    while is_running:
        # Active window (from pygetwindow)
        active_window = gw.getActiveWindow()

        if check_active_tab(activeWindow=active_window, tabList=banned_tabs):
            shock_timer -= 1

        time.sleep(1)
        print(f'Time left: {shock_timer} seconds')

        if shock_timer <= 0:
            shock(shock_strength)
            shock_timer = timer_start_value

            # NOTE: Removed shock confirmation

            # # Get confirmation to administer the shock
            # do_shock = input("shock (y/n): ")
            # if  do_shock == 'y':
            #     shock(shock_strength)
            #     do_shock = ''
            # else:
            #     print("closing software...")
            #     break

if __name__ == "__main__":
    Main()
