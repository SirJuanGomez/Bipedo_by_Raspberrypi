#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __MODE1              = 0x00
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD

  def __init__(self, address=0x40, bus_num=1, debug=False):
    """Initialize PCA9685 with I2C address and bus number"""
    try:
      self.bus = smbus.SMBus(bus_num)
      self.address = address
      self.debug = debug
      self.write(self.__MODE1, 0x00)
      if self.debug:
        print(f"PCA9685 initialized at address 0x{address:02X} on I2C bus {bus_num}")
    except Exception as e:
      raise RuntimeError(f"Error initializing PCA9685: {e}")
    
  def write(self, reg, value):
    """Writes an 8-bit value to the specified register/address"""
    try:
      self.bus.write_byte_data(self.address, reg, value)
    except Exception as e:
      raise RuntimeError(f"Error writing to register 0x{reg:02X}: {e}")
      
  def read(self, reg):
    """Read an unsigned byte from the I2C device"""
    try:
      result = self.bus.read_byte_data(self.address, reg)
      return result
    except Exception as e:
      raise RuntimeError(f"Error reading from register 0x{reg:02X}: {e}")
    
  def setPWMFreq(self, freq):
    """Sets the PWM frequency"""
    if not (40 <= freq <= 1000):
      raise ValueError("Frequency must be between 40 and 1000 Hz")
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    prescale = math.floor(prescaleval + 0.5)

    oldmode = self.read(self.__MODE1)
    newmode = (oldmode & 0x7F) | 0x10        # sleep
    self.write(self.__MODE1, newmode)        # go to sleep
    self.write(self.__PRESCALE, int(math.floor(prescale)))
    self.write(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.write(self.__MODE1, oldmode | 0x80)
    if self.debug:
      print(f"PWM frequency set to {freq} Hz")

  def setPWM(self, channel, on, off):
    """Sets a single PWM channel"""
    if not (0 <= channel <= 15):
      raise ValueError(f"Canal {channel} fuera de rango (0-15)")
    self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
    self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
    self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
    self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)
    if self.debug:
      print(f"Channel {channel} set: ON={on}, OFF={off}")
  
  def setMotorPwm(self, channel, duty):
    """Set motor speed with PWM duty cycle"""
    self.setPWM(channel, 0, duty)
    if self.debug:
      print(f"Motor PWM set on channel {channel} with duty cycle {duty}")
  
  def setServoPulse(self, channel, pulse):
    """Sets the Servo Pulse, The PWM frequency must be 50HZ"""
    if not (0 <= channel <= 15):
      raise ValueError(f"Canal {channel} fuera de rango (0-15)")
    pulse = pulse * 4096 / 20000        # PWM frequency is 50HZ, the period is 20000us
    self.setPWM(channel, 0, int(pulse))
    if self.debug:
      print(f"Servo pulse set on channel {channel} with pulse {pulse}")

if __name__=='__main__':
    print("PCA9685 module ready.")
