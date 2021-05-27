# The MIT License (MIT)
#
# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
This example displays the orientation, pose and RSSI as well as EMG data
if it is enabled and whether the device is locked or unlocked in the
terminal.
Enable EMG streaming with double tap and disable it with finger spread.
"""

from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys
import time

global counter
counter = 0
class Listener(myo.DeviceListener):

  def __init__(self):
    self.interval = TimeInterval(None, 0.05)
    self.orientation = None
    self.pose = myo.Pose.rest
    self.emg_enabled = False
    self.locked = False
    self.rssi = None
    self.emg = None
    self.battery_level = None
    self.gyro = None
  
  def getGyro(self):
    return self.gyro

  def output(self):
    if not self.interval.check_and_reset():
      return

    parts = []
    if self.gyro:
      for comp in self.gyro:
        parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
    parts.append(str(self.pose).ljust(10))
    parts.append('E' if self.emg_enabled else ' ')
    parts.append('L' if self.locked else ' ')
    parts.append(self.rssi or 'NORSSI')
    parts.append(self.battery_level or "%")
    if self.emg:
      for comp in self.emg:
        parts.append(str(comp).ljust(5))
    print('\r' + ''.join('[{}]'.format(p) for p in parts), end='')
    sys.stdout.flush()

  def on_connected(self, event):
    event.device.request_battery_level
    event.device.request_rssi()
    event.device.vibrate(myo.VibrationType.medium)
    
  def on_battery_level(self, event):
    self.battery_level = event.battery_level
    # self.output()

  def on_rssi(self, event):
    self.rssi = event.rssi
    # self.output()

  def on_pose(self, event):
    self.pose = event.pose
    if self.pose == myo.Pose.double_tap:
      event.device.stream_emg(True)
      self.emg_enabled = True
    elif self.pose == myo.Pose.fingers_spread:
      event.device.stream_emg(False)
      self.emg_enabled = False
      self.emg = None
      event.device.vibrate(myo.VibrationType.short)
    elif self.pose == myo.Pose.fist:
        event.device.vibrate(myo.VibrationType.short)
    # self.output()

  def on_orientation(self, event):
    global counter
    counter += 1
    self.orientation = event.orientation
    self.gyro = event.gyroscope
    # self.output()
    

  def on_emg(self, event):
    self.emg = event.emg
    # self.output()

  def on_unlocked(self, event):
    self.locked = False
    # self.output()

  def on_locked(self, event):
    self.locked = True
    # self.output()


if __name__ == '__main__':
  myo.init(sdk_path = "C:/Users/krish/OneDrive/Documents/Syslab/Myo/myo-sdk-win-0.9.0")
  hub = myo.Hub()
  listener = Listener()
  start = time.time()
  while hub.run(listener.on_event, 1):
    print(listener.getGyro())
  
