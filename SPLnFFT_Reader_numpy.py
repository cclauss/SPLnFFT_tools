#!/usr/bin/env python
# coding: utf-8

# See: https://forum.omz-software.com/topic/1964/binary-files-read-and-write
# This code is available at: https://github.com/cclauss/SPLnFFT_tools

# SPLnFFT app makes two sound pressure level readings every 1/8th of a second.
# It stores the results into a daily binary data file that this script reads.
#
# Read 1,382,400 float32 values into a numpy.ndarray.
# Reshape that ndarray into two columns of 691,200 floats each.
# 691,200 == 8 readings per sec * 60 secs per min * 60 mins per hour * 24 hours.
# The columns represent Fast Sound Pressure Level and Slow Sound Pressure Level.

# 24 hours of data is too much to view at once so work should be
# done to allow users to zoom into interesting portions of the day.

import datetime, numpy

#filename = 'SPLnFFT_2015_07_21.bin'
#filename = 'SPLnFFT_2015_08_17.bin'
filename = 'SPLnFFT_2015_08_17_00h_to_08h.bin'
try:
    pieces = filename.split('_')
    start_hour = int(pieces[4].rstrip('h'))
    end_hour = int(pieces[6].rstrip('h.bin'))
except IndexError:
    start_hour, end_hour = 0, 24
hours_of_data = end_hour - start_hour
fmt = '{} hours of data from {:02}h to {:02}h'
print(fmt.format(hours_of_data, start_hour, end_hour))

def elapsed_time(msg='total'):
    return 'Elapsed time ({}): {}'.format(msg, datetime.datetime.now() - start)

start = datetime.datetime.now()
data = numpy.fromfile(filename, dtype=numpy.float32).reshape(-1, 2)
print(elapsed_time('4 Read and reshape'))
print(type(data), len(data))  # numpy.ndarray, 691200 for a 24 hour file
t = numpy.linspace(start_hour, end_hour, len(data))

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig.subplots_adjust(left=0.09, bottom=0.1, right=0.97, top=0.93)
fast = data[:,0]
slow = data[:,1]
ax.plot(t[fast>0], fast[fast>0], 'g+-')
ax.plot(t[slow>0], slow[slow>0], 'ms-')
t_bad = t[(fast <= 0) | (slow <= 0)]
print(elapsed_time('3 Starting scatter...'))  # approx. 0.5 seconds
ax.scatter(t_bad, max(fast.max(), slow.max()) + numpy.ones_like(t_bad), marker='o')
print(elapsed_time('2 Scatter'))  # approx. 22 seconds for a 24 hour file
plt.legend(('Fast Lp','Slow Lp','Readings <= 0'), loc='lower right')
plt.title('Sound Pressure Level data from ' + filename)
hours_of_data = end_hour - start_hour
if hours_of_data == 24:
    plt.xlabel('Eight samples per second across a 24 hour day')
else:
    plt.xlabel('Eight samples per second across {} hours'.format(hours_of_data))
plt.ylabel('Sound Pressure Level (Lp) in dB(A)')
plt.xlim(start_hour, end_hour)
plt.xticks(numpy.arange(start_hour, end_hour))
print(elapsed_time('1 Adornments'))
plt.show()
print(elapsed_time('0 plt.show() Done.'))  # approx. 2 minutes 20 seconds for a 24 hour file
