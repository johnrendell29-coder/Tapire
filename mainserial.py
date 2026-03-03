import serial
import time

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)  # Wait for Arduino reset
    print("Connected to Arduino on COM3")
except:
    print("Failed to connect to Arduino.")
    exit()

while True:
    command = input("Enter 1 to turn ON LED, 0 to turn OFF LED, q to quit: ")

    if command == '1':
        arduino.write(b'1')
    elif command == '0':
        arduino.write(b'0')
    elif command == 'q':
        break
    else:
        print("Invalid command")
        continue

    time.sleep(0.1)
    if arduino.in_waiting:
        response = arduino.readline().decode().strip()
        print("Arduino says:", response)

arduino.close()
print("Connection closed.")