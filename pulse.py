import numpy

from gpiozero import MCP3008
from time import sleep, time
from matplotlib import pyplot as plt
from numpy import linspace

from scipy.fft import fft, ifft, fftfreq

pulse = MCP3008(channel=2)
previouspulse = 0.0
beatlist = []
#timelist = []
time_count = 0
count = 0
heartbeat = 0
increasing = True

SAMPLE_RATE = 200.0
DURATION = 8.0

#t = time()
#time_differences = []
#time_diff = 0
timing = 0
START_TIME = time()

for i in range(800):
#while len(beatlist) < DURATION:
 #   count += 1
    #t = time()
    #print(t)
    beatlist.append(pulse.value)
    #timelist.append(timing)
    #if ((increasing and previouspulse > pulse.value) or (not(increasing) and previouspulse < pulse.value)):
    #    count += 1
    #    if (count % 4 == 0):
    #        heartbeat += 1
    #    increasing = not(increasing)
    previouspulse = pulse.value
    time_count += 1/SAMPLE_RATE
    # time_diff =  time() - t
    # time_differences.append(time_diff)
    #timing = t - START_TIME
    sleep(1/SAMPLE_RATE)

timing = time() - START_TIME
SAMPLE_RATE = len(beatlist) / timing
# SAMPLE_RATE = sum(time_differences) / len(time_differences)
print(SAMPLE_RATE)
print(timing)

#print(count)
#print(heartbeat)
print(beatlist)
#print(timelist)
#x = timelist
y = beatlist
#print(len(x))
print(len(y))

# plt.plot(x,y)
# plt.hlines(y=0.3, xmin=0,xmax=8,color="r", linestyle="-")
# plt.show()

print(1/SAMPLE_RATE)
print(1.0/SAMPLE_RATE)
N = 800 # num sample points
print(N)
yf = fft(y)
xf = fftfreq(N, 1.0 / SAMPLE_RATE)
print(xf.shape)
print(yf.shape)
yf = numpy.abs(yf)



# xf = fftfreq(N, T)[:N//2]

plt.plot(xf, yf)
plt.xlim(0.8, 2)
plt.ylim(0,20)
#plt.plot(xf, numpy.abs(yf))
plt.show()