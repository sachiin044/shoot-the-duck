import serial
import time
from pynput.mouse import Controller, Button
import pyautogui

PORT = 'COM6'
BAUD = 115200
SENSITIVITY = 1
DEADZONE = 4

mouse = Controller()
last_btn = 0
press_time = 0
CENTER_INTERVAL = 7 # Interval for automatic recentering In seconds
CENTER_LOCK_DURATION = 2 # Delay after centering before movement is allowed
last_center_time = time.time() # Initialize timestamp for auto-recenter
lock_start_time = 0 # Timestamp when center lock started
is_locked = False

# ── Kalman filter state for each axis ───────────────
class KalmanFilter:
    def __init__(self):
        self.x = 0.0       # estimated true value
        self.bias = 0.0    # estimated bias
        self.P00 = 1.0     # uncertainty in value
        self.P01 = 0.0
        self.P10 = 0.0
        self.P11 = 1.0     # uncertainty in bias

        self.Q_angle = 0.001   # process noise — how fast true value changes
        self.Q_bias  = 0.003   # process noise — how fast bias drifts
        self.R       = 0.03    # measurement noise

    def update(self, measurement, dt=0.015):
        # Predict
        self.P00 += dt * (dt*self.P11 - self.P01 - self.P10 + self.Q_angle)
        self.P01 -= dt * self.P11
        self.P10 -= dt * self.P11
        self.P11 += self.Q_bias * dt

        # Update
        S = self.P00 + self.R
        K0 = self.P00 / S
        K1 = self.P10 / S

        y = measurement - (self.x - self.bias)
        self.x    += K0 * y
        self.bias += K1 * y

        P00_temp = self.P00
        self.P00 -= K0 * self.P00
        self.P01 -= K0 * self.P01
        self.P10 -= K1 * P00_temp
        self.P11 -= K1 * self.P01

        return self.x - self.bias  # return corrected value

kf_gx = KalmanFilter()
kf_gy = KalmanFilter()

print("Connecting...")
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.flushInput()
time.sleep(3)
ser.flushInput()
print("Ready! Hold button to re-center.\n")

screen_w, screen_h = pyautogui.size()
cx, cy = screen_w // 2, screen_h // 2

while True:
    try:
        # 1. Check for automatic recenter every 5 seconds (TOP OF LOOP to avoid blocking)
        now = time.time()
        if now - last_center_time >= CENTER_INTERVAL:
            print(f"DEBUG: Triggering Auto-Center at {now}")
            pyautogui.moveTo(cx, cy)
            last_center_time = now
            is_locked = True
            lock_start_time = now
            print("RE-CENTERED (AUTO) - LOCKED FOR 2s")
            # Clear any pending serial data to avoid jump after lock
            ser.reset_input_buffer()
            continue

        # 2. Check if we are currently in a lock period
        if is_locked:
            if now - lock_start_time >= CENTER_LOCK_DURATION:
                is_locked = False
                print("MOVEMENT UNLOCKED")
                ser.reset_input_buffer() # Clear old data
            else:
                # Still locked, sleep briefly to avoid high CPU and check again
                time.sleep(0.01)
                continue

        # 3. Read serial data (with timeout)
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line or ',' not in line: 
            continue
            
        parts = line.split(',')
        if len(parts) != 5: continue

        gx_raw = float(parts[2])
        gy_raw = float(parts[3])
        btn    = int(float(parts[4]))

        # Kalman filter corrects bias automatically every frame
        gx = kf_gx.update(gx_raw)
        gy = kf_gy.update(gy_raw)

        dx = -gy * SENSITIVITY if abs(gy) > DEADZONE else 0
        dy = -gx * SENSITIVITY if abs(gx) > DEADZONE else 0

        if dx != 0 or dy != 0:
            mouse.move(int(dx), int(dy))

        if btn == 1 and last_btn == 0:
            press_time = time.time()
        if btn == 0 and last_btn == 1:
            if time.time() - press_time > 0.5:
                pyautogui.moveTo(cx, cy)
                print("RE-CENTERED (MANUAL)!")
                ser.reset_input_buffer()
            else:
                mouse.click(Button.left)
                print("CLICK")

        last_btn = btn
        print(f"Gx:{gx:+5.2f} Gy:{gy:+5.2f} | dx:{dx:+4.0f} dy:{dy:+4.0f} | BTN:{btn}")

    except (ValueError, UnicodeDecodeError):
        pass
    except KeyboardInterrupt:
        print("Stopped.")
        ser.close()
        break

