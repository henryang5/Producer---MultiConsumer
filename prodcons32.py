#!/usr/bin/env python
# Chun Example 4-12, changes by mht
# Henry Ang
# 3/1/17
# CSC 4800
# Threading program with a single producer and multiple consumers. Changes by Henry Ang

from time import sleep
from queue import *
from myThread3 import MyThread
from threading import Lock

NITEMS = 10
NREADERS = 3
WRITERDELAY = 1
WRITERFINISHED = False

def writeQ(queue, item):                 # producer, writer
    """
    Producer, puts items in queue.
    :param queue:
    :param item:
    """
    print('Writer producing object %d for Q...' % item, end='')
    queue.put(item, True)
    print("size now", queue.qsize())

def readQ(queue, nReader):               # consumer, reader
    """
    Consumer, gets value from queue. Returns consumed object from queue or ends.
    :param queue:
    :param nReader:
    :return: None, val
    """
    try:
        global WRITERFINISHED;
        if WRITERFINISHED == True and queue.qsize() == 0: # end of prod-con processing, exit thread
           return None
        else:
            val = queue.get(False)                  # non blocking. returns value or goes to empty exception
            print('     Reader-' + str(nReader) + ' consumed object %d from Q... size now' % val, queue.qsize())
            return val
    except Empty:
        print("     Reader-%d polling empty queue" % nReader)

def writer(queue, loops):
    """
    Producer thread. Calls writeQ and sleeps. When producer is done WriterFinished is set to true.
    :param queue:
    :param loops:
    """
    global WRITERFINISHED;
    for i in range(loops):
        writeQ(queue, i)
        sleep(WRITERDELAY)
    WRITERFINISHED = True;

def reader(queue, loops, nReader):
    """
    Reader thread. Calls readQ and sleeps.
    :param queue:
    :param loops:
    :param nReader:
    """
    for i in range(loops):
        item = readQ(queue, nReader)
        sleep(3)

def main():
    """
    Main function of program. Creates a writer and multiple readers.
    """
    nloops = NITEMS
    numReaders = NREADERS

    funcs = [writer]
    for i in range(0, numReaders):  # multiple readers
        funcs.append(reader)

    nfuncs = range(len(funcs))
    q = Queue(32)
    threads = []

    for i in nfuncs:
        if i == 0:     # write
            t  = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
        else:          # read
            t = MyThread(funcs[i], (q, nloops, (i -1)), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print('all DONE')

if __name__ == '__main__':
    main()