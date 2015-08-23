from __future__ import division
from datetime import datetime
import time


def timestamp():
    return int((datetime.utcnow() -
                datetime(1970, 1, 1)).total_seconds() * 1000)


class wait:
    last = None
    step = 2000

    def __init__(self, step):
        self.start()
        self.step = step

    def start(self):
        self.last = timestamp()
        return self.last

    def next(self):
        if not self.last:
            self.start()

        waituntil = self.last + self.step
        now = timestamp()
        timetowait = waituntil - now  # milliseconds
        if timetowait > 0:
            time.sleep(timetowait / 1000)  # fractions of seconds

        self.last = timestamp()
        return self.last


if __name__ == '__main__':
    w = wait(201)
    initime = w.start()
    print("started at: ", initime)

    for k in range(3):
        print(w.next())
