from st3215 import ST3215

servo = ST3215('/dev/ttyACM1')
print("Connected to servo")
ids = servo.ListServos()
print(ids)