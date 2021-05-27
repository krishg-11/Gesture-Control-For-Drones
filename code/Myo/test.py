import myo


class Listener(myo.DeviceListener):
  
  def __init__(self):
    self.orientation = None
    self.pose = myo.Pose.rest
    self.flight_direction = "R"
    self.locked = False
    self.battery_level = None
    self.gyro = None

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.request_battery_level()

  def on_battery_level(self, event):
    print("Your battery level is:", event.battery_level)
    
  def on_orientation(self, event):
    self.orientation = event.orientation
    self.gyro = event.gyroscope

  def on_pose(self, event):
    self.pose = event.pose
    if self.pose == myo.Pose.double_tap:
      if(self.locked): 
        event.device.unlock()
        print("Device Unlocked")
      else: 
        event.device.lock()
        print("Device Locked")
      event.device.vibrate(myo.VibrationType.long)
      self.locked = not self.locked
    if(not self.locked):
      if self.pose == myo.Pose.fingers_spread and self.flight_direction == "R":
        event.device.vibrate(myo.VibrationType.short)
        self.flight_direction = "L"
      elif self.pose == myo.Pose.fist and self.flight_direction == "L":
          event.device.vibrate(myo.VibrationType.short)
          self.flight_direction = "R"


if __name__ == '__main__':
  myo.init(sdk_path = "C:/Users/krish/OneDrive/Documents/Syslab/Myo/myo-sdk-win-0.9.0")
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 1000):
    print(listener.gyro)
    print(listener.locked)