import time

DT = 0.01
SIM_TIME = 100
BOUNCINESS = 1
position, velocity = 1, 0

lastVel = velocity
peaks = [100*position]
timestepCount = int(SIM_TIME / DT)

def a(t): return -9.81

for step in range(timestepCount):
    acceleration = a(step * DT)
    velocity += acceleration * DT
    position += velocity * DT

    if position < 0:
        velocity = -velocity * BOUNCINESS
        position += velocity * DT

    if lastVel > 0 and velocity < 0:
        peaks.append(100*position)

    print(f"{100*position:.2f}         v: {100*velocity:.2f}, a: {100*acceleration:5.2f}")
    lastVel = velocity
    time.sleep(DT)

print(peaks)
