#!/usr/bin/python

import sys, os
from subprocess import Popen, PIPE
import serial

from eye import eye

<<<<<<< HEAD
e = eye( 1, show_frame = 1)
=======
e = eye( 0, show_frame = 1)
>>>>>>> b528ba7636462539ddefa2297ef51de047e2480e

pid = os.getpid()

ser = serial.Serial(port='/dev/ttyUSB0')

FN = '/home/artp/Data/%d.dat' % pid
F = open(FN, 'w')

gp = Popen(['gnuplot','-'], bufsize = 0, stdin=PIPE, stdout = PIPE, stderr=PIPE, shell=False)
gp.stdin.write('unset key\n')
gp.stdin.write('lower\n')

i = 0
first = 1
M = 0
while (i<10):
    line = ser.readline()
    mm = e.run()
    if mm :         # may be "None"
        M = mm
    sys.stdout.write("%s Mass: %d\n" % ( line.split('\n')[0], M) )
      
    words = line.split('\n')[0].split(' ')
    if (len(words) == 8):
        F.write('%s %s %s %s %d\n' %(words[1],words[3],words[5],words[7], M))
        F.flush()

        x = int(words[1])
        gp.stdin.write('set xrange [%d:%d]\n' % (x-3000,x))
        if (first):
            first = 0
            gp.stdin.write('set yrange [0:100]\nset y2range[0:5000]\n')
#            gp.stdin.write('unset key\nset format x \"\"\n')
            gp.stdin.write('plot \'%s\' using 1:2 axes x1y1 with lines, \'%s\' usi 1:3 axes x1y1 with lines, \'%s\' usi 1:5 axes x1y2 with lines\n' % (FN,FN,FN))
        else :
            gp.stdin.write('replot\n')
        gp.stdin.flush()

        i = i
F.close()
