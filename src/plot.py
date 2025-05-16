from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

plt.style.use('fivethirtyeight')

x = []
y = []

def animate(i):
    x.append(random.randint(1, 10))
    y.append(random.randint(1, 10))

    plt.plot(x, y)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()  