from pymodbus.client import ModbusSerialClient
from struct import pack, unpack
from time import sleep


class PTU2:

    def __init__(self, serial_port:str, baudrate:int=115200, id:int=1) -> None:
        self.__client = ModbusSerialClient(serial_port, baudrate=baudrate)
        self.__id = id
    
    def __del__(self) -> None:
        self.__client.close()

    def __set_cmd(self, address:int, value:int) -> None:
        rsp = self.__client.write_registers(address=address, values=[value], slave=self.__id)
        if rsp.isError(): raise IOError(f"write_registers(address={address}, values={[value]}, slave={self.__id})")
    
    def __get_cmd(self, address:int):
        rsp = self.__client.read_holding_registers(address=address, count=1, slave=self.__id)
        if rsp.isError(): raise IOError(f"write_registers(address={address}, count=1, slave={self.__id})")
        else: return rsp.registers[0]
    
    @property
    def id(self):
        return self.__get_cmd(0)
    @id.setter
    def id(self, id:int):
        self.__set_cmd(0, id)
        self.__id = id

    @property
    def sn(self):
        sn_low, sn_high = unpack('BB', pack('H', self.__get_cmd(1)))
        sn_0 = ''.join(['0']*(4-len(str(sn_low))))
        str_sn = f'{sn_0}{sn_low}'
        hw_ver = self.hardware_version
        sw_ver = self.software_version
        return f'PTU2{hw_ver[0]}{hw_ver[1]}{sw_ver[0]}{sw_ver[1]}{(sn_high&0b11110000)>>4}{str_sn}'

    @property
    def hardware_version(self):
        return tuple(reversed(list(unpack('BB', pack('H', self.__get_cmd(2))))))

    @property
    def software_version(self):
        return tuple(reversed(list(unpack('BB', pack('H', self.__get_cmd(3))))))

    @property
    def firmware_version(self):
        first, second_third = unpack('BB', pack('H', self.__get_cmd(4)))
        return tuple(reversed([first, (second_third&0b11110000)>>4, second_third&0b00001111]))

    @property
    def speed(self):
        return self.__get_cmd(6)
    @speed.setter
    def speed(self, speed:int):
        assert speed >= 0 and speed <= 30
        self.__set_cmd(6, speed)

    @property
    def yaw(self):
        return unpack('h', pack('H', self.__get_cmd(12)))[0]/100
    @yaw.setter
    def yaw(self, degrees:float):
        assert degrees >= -60.0 and degrees <= 60.0
        self.__set_cmd(7, unpack('H', pack('h', int(degrees*100)))[0])
    
    @property
    def pitch(self):
        return unpack('h', pack('H', self.__get_cmd(13)))[0]/100
    @pitch.setter
    def pitch(self, degrees:float):
        assert degrees >= -60.0 and degrees <= 60.0
        self.__set_cmd(8, unpack('H', pack('h', int(degrees*100)))[0])

    @property
    def yaw_temp(self):
        return self.__get_cmd(14)/10
    
    @property
    def pitch_temp(self):
        return self.__get_cmd(15)/10
    
    @property
    def loop_time(self):
        return self.__get_cmd(19)
    
    def set_zero(self) -> None:
        self.__set_cmd(5, 1)

    def move(self, yaw:float, pitch:float, speed:int=None):
        speed_backup = self.speed
        if speed: self.speed = speed
        self.yaw = yaw
        self.pitch = pitch
        sleep(max(abs(yaw-self.yaw), abs(pitch-self.pitch))/self.speed)
        self.speed = speed_backup

    @property
    def joint_0(self): return 0.023
    @property
    def joint_1(self): return 0.062
    @property
    def joint_2(self): return 0.032

if __name__ == '__main__': # for testing

    pan_tilt = PTU2("/dev/pan_tilt")

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