# iqr_ptu2

IQR PTU2 SDK

# Installation

```shell
git clone https://github.com/I-Quotient-Robotics/iqr_ptu2.git
cd iqr_ptu2
sudo python3 setup.py install
```

check: `pip show iqr_ptu2`

## Usage

```python
from iqr_ptu2 import PTU2

pan_tilt = PTU2("/dev/pan_tilt") # or maybe /dev/ttyACM0, \\.\COMx

print("SN: ", pan_tilt.sn)
print("HW_VERSION: ", pan_tilt.hardware_version)
print("SW_VERSION: ", pan_tilt.software_version)
print("FW_VERSION: ", pan_tilt.firmware_version)
print()

print("ID: ", pan_tilt.id)
print()

pan_tilt.move(60, 0, speed=10)
pan_tilt.move(-60, 60, speed=20)
pan_tilt.move(0, -60, speed=30)
pan_tilt.move(0, 0)
```