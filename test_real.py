from omron_d6t import OmronD6T
import time
import numpy
import matplotlib.pyplot as plt
import numpy as np

omron = OmronD6T(bus=1, address=0x0a)

old_bar = None
def draw_sensor():
    global old_bar
    res = omron.read()


    if res is None:
        return

    room, temps = res

    normalized = []

    for temp in temps:
        normalized.append(temp - room)

    temperature = np.reshape(normalized, (-1, 4))
    plt.pcolor(temperature, vmin=-10, vmax=10)

    if old_bar is not None:
        old_bar.remove()

    old_bar = plt.colorbar()

    plt.pause(0.1)

    # print("Room Temperature: " + str(room) + "\nTemp: " + str(temps))

    print(numpy.mean(normalized))




try:
    while(True):
        draw_sensor()
except KeyboardInterrupt:
    print('\nExiting script.')
    omron.close_connection()

