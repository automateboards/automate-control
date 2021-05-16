#!/usr/bin/python3

from smbus import SMBus
import serial

I2C_ADDRESS         = 0x08
I2C_BUS             = 0x01
UART_PORT           = "/dev/ttyACM0"
UART_BAUDRATE       = 9600
UART_TIMEOUT_MS     = 3000
COMM_DEBUG          = True


class DeviceConnection(object):

    def __init__(self, mode='uart_usb', address=I2C_ADDRESS, port=UART_PORT, bus=I2C_BUS):
        """Initialize UART or I2C connection to slave microcontroller"""

        self._mode = mode
        self.address = address
        self.port = port

        if mode == 'uart_usb':
            self._con = serial.Serial(
                port=self.port,
                baudrate=UART_BAUDRATE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                rtscts=False,
                dsrdtr=False,
                timeout=UART_TIMEOUT_MS / 1000,
                write_timeout=5,
            )
        else:
            self._con = SMBus(bus)

    def disconnect(self):
        """Disconnect UART or I2C connection"""

        self._con.close()

    def get_register(self, register_address, format_bytes=False):
        """Get single register from slave microcontroller"""

        if format_bytes:
            return self.get_registers(register_address, register_len=1, format_bytes=format_bytes)
        else:
            return self.get_registers(register_address, register_len=1, format_bytes=format_bytes)[0]
        
    def get_registers(self, register_address, register_len=1, format_bytes=False):
        """Get multiple registers from slave microcontroller"""

        if COMM_DEBUG:
            print("request register '%02x' len '%i'" % (register_address, register_len * 2))

        if self._mode == 'uart_usb':

            self._con.write(b'R%02x%02x\n' % (register_address, register_len * 2))
            response = self._con.read_until(terminator=serial.LF).decode('ascii').strip()

            if COMM_DEBUG:
                print("raw response '%s'" % response)

            if not response.startswith('ACK'):
                raise Exception("response error")

            response = response.split('ACK')[1]

            registers = []
            if not format_bytes:
                registers = [int(response[i:i + 4], 16) for i in range(0, len(response), 4)]
            else:
                registers = [int(response[i:i + 2], 16) for i in range(0, len(response), 2)]

            if COMM_DEBUG:
                print("decoded response '%s'" % registers)

            return registers

        else:
            response = self._con.read_i2c_block_data(self.address, register_address, register_len * 2)

            if COMM_DEBUG:
                print("raw response '%s'" % response)

            registers = []
            for i in range(0, register_len * 2, 2):
                registers.append((response[i] << 8) + response[i+1])

            if COMM_DEBUG:
                print("decoded response '%s'" % registers)

            return registers
        
    def set_register(self, register_address, register_value):
        """Set single register on slave microcontroller"""

        return self.set_registers(register_address, [register_value])

    def set_registers(self, register_address, register_values, format_bytes=False):
        """Set multiple registers on slave microcontroller"""

        if self._mode == 'uart_usb':

            out_str = ""
            if format_bytes:
                for register_value in register_values:
                    out_str += str("%02x" % register_value)
            else:
                for register_value in register_values:
                    out_str += str("%04x" % register_value)

            if COMM_DEBUG:
                print("set registers raw '%02x - %s'" % (register_address, out_str))

            self._con.write(b'W%02x%s\n' % (register_address, out_str.encode('ascii')))
            response = self._con.read_until(terminator=serial.LF).decode('ascii').strip()

            if COMM_DEBUG:
                print("raw response '%s'" % response)

            if not response.startswith('ACK'):
                raise Exception("response error")

            return response

        else:
            out_bytes = []
            if format_bytes:
                out_bytes = register_values
            else:
                for register_value in register_values:
                    out_bytes.extend([(register_value & 0xFF00) >> 8, (register_value & 0x00FF)])

            if COMM_DEBUG:
                print("set registers raw '%02x - %s'" % (register_address, out_bytes))

            self._con.write_i2c_block_data(self.address, register_address, out_bytes)
