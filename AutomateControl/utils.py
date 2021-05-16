#!/usr/bin/python3

from enum import IntEnum


class REG():
    R_SW_INFO               = 0x00
    R_HW_INFO               = 0x01
    R_3V3_VAL               = 0x02
    R_5V0_VAL               = 0x03
    R_TEMP_VAL              = 0x04
    R_SWITCH_VAL            = 0x05
    R_GEN_ERROR1            = 0x06
    R_GEN_ERROR2            = 0x07

    RW_INT_CONF             = 0x10
    RW_EMU_CONF             = 0x11
    RW_I2C_CONF             = 0x12
    RW_LED_CONF             = 0x13
    RW_WDG_CONF             = 0x14
    RW_RTC_CONF             = 0x15
    RW_SWITCH_CONF          = 0x16

    RW_RTC_SEC_VAL          = 0x20
    RW_RTC_MIN_VAL          = 0x21
    RW_RTC_HOUR_VAL         = 0x22
    RW_RTC_DAY_VAL          = 0x23
    RW_RTC_MONTH_VAL        = 0x24
    RW_RTC_YEAR_VAL         = 0x25
    RW_RTC_WDAY_VAL         = 0x26

    RW_GPIO_INT_CONF1       = 0x30
    RW_GPIO_INT_CONF2       = 0x31
    RW_GPIO_INT_CONF3       = 0x32
    RW_GPIO_INT_CONF4       = 0x33
    RW_GPIO1_CONF1          = 0x37
    RW_GPIO2_CONF1          = 0x38
    RW_GPIO3_CONF1          = 0x39
    RW_GPIO4_CONF1          = 0x3A
    RW_GPIO_M1_AN_CONF1     = 0x3B
    RW_GPIO_M2_AN_CONF1     = 0x3C
    RW_GPIO1_CONF2          = 0x40
    RW_GPIO2_CONF2          = 0x41
    RW_GPIO3_CONF2          = 0x42
    RW_GPIO4_CONF2          = 0x43
    RW_GPAB_IODIR           = 0x44
    RW_GPAB_IPOL            = 0x45
    RW_GPAB_INTEN           = 0x46
    RW_GPAB_GPPU            = 0x47
    RW_GPAB_GPPD            = 0x48

    R_GPIO1_ADC_VAL         = 0x50
    R_GPIO2_ADC_VAL         = 0x51
    R_GPIO3_ADC_VAL         = 0x52
    R_GPIO4_ADC_VAL         = 0x53
    R_GPIO_M1_AN_ADC_VAL    = 0x54
    R_GPIO_M2_AN_ADC_VAL    = 0x55
    RW_GPIO1_DAC_VAL        = 0x56
    RW_GPIO2_DAC_VAL        = 0x57
    RW_GPIO3_DAC_VAL        = 0x58
    RW_GPIO4_DAC_VAL        = 0x59
    RW_GPIO1_DIG_VAL1       = 0x5A
    RW_GPIO2_DIG_VAL1       = 0x5B
    RW_GPIO3_DIG_VAL1       = 0x5C
    RW_GPIO4_DIG_VAL1       = 0x5D
    RW_GPIO_M1_AN_DIG_VAL1  = 0x5E
    RW_GPIO_M2_AN_DIG_VAL1  = 0x5F
    RW_GPIO1_DIG_VAL2       = 0x68
    RW_GPIO2_DIG_VAL2       = 0x69
    RW_GPIO3_DIG_VAL2       = 0x6A
    RW_GPIO4_DIG_VAL2       = 0x6B
    RW_GPAB_DIG_VAL1        = 0x6C
    RW_GPIO_INT_VAL1        = 0x70

    RW_UART_RS485_CONF1     = 0x80
    RW_UART_RS485_CONF2     = 0x81
    RW_UART_MIKRO2_CONF1    = 0x82
    RW_UART_MIKRO2_CONF2    = 0x83

    W_UART_RS485_TX_PTR     = 0x90
    W_UART_RS485_TX_LEN     = 0x91
    W_UART_RS485_TX_VAL	    = 0x92
    W_UART_RS485_TX_SEND	= 0x93

    W_UART_RS485_RX_LEN     = 0xA0
    R_UART_RS485_RX_VAL	    = 0xA2
    R_UART_RS485_RX_PTR     = 0xA3
    R_UART_RS485_RX_PEND    = 0xA4
    R_UART_RS485_RX_STATUS  = 0xA5

    W_LED_SAVE              = 0xF0
    W_GPIO_SAVE             = 0xF1
    W_UART_SAVE             = 0xF2
    R_DEBUG1                = 0xF5
    R_DEBUG2                = 0xF6
    R_PERF_CNT1             = 0xF7
    R_PERF_CNT2             = 0xF8
    R_PERF_CNT3             = 0xF9
    W_BOOTLOADER            = 0xFA
    RW_ESP32_DELAY          = 0xFB
    R_GPIO1_CUR             = 0xFC
    R_GPIO2_CUR             = 0xFD
    R_GPIO3_CUR             = 0xFE
    R_GPIO4_CUR             = 0xFF


class EnumBase(IntEnum):
    
    @classmethod
    def get_list(cls):
        return [e.name for e in cls]
        
    @classmethod
    def get_by_name(cls, name):
        for e in cls:
            if e.name == name:
                return e.value


class GPIO_FUNC(EnumBase):
    DEFAULT = 0x00
    PWM = 0x01
    PWMLED = 0x02
    CNT = 0x03
    CNT_RST = 0x04
    CNT_S0 = 0x05
    RC_SERVO = 0x06
    STEPPER = 0x07
    AO_0_5V_OUT = 0x08
    AO_0_10V_OUT = 0x09
    AO_0_24V_OUT = 0x0A
    AI_RATIO_3V3 = 0x0B
    AI_RATIO_5V0 = 0x0C
    AI_0_7V5 = 0x0D
    AI_0_15V = 0x0E


class GPIO_MODE(EnumBase):
    MODE_NONE = 0x00
    MODE_AN_IN = 0x01
    MODE_AN_OUT = 0x02
    MODE_DIG_IN = 0x03
    MODE_DIG_OUT = 0x04
    MODE_DIG_OUT_OD = 0x05


class GPIO_MODE_GPAB(EnumBase):
    MODE_NONE = 0x00
    MODE_DIG_IN = 0x03
    MODE_DIG_OUT = 0x04


class GPIO_MODE_BCM(EnumBase):
    MODE_NONE = 0x00
    MODE_DIG_IN = 0x03
    MODE_DIG_OUT = 0x04
    MODE_DIG_OUT_OD = 0x05


class GPIO_PULL(EnumBase):
    NO_PULL = 0x00
    PULL_DOWN = 0x01
    PULL_UP = 0x02


class GPIO_PULL_GPAB(EnumBase):
    NO_PULL = 0x00
    PULL_UP = 0x02


class GPIO_HYST(EnumBase):
    HYST_0MV = 0x00
    HYST_25MV = 0x01
    HYST_50MV = 0x02
    HYST_100MV = 0x03
    HYST_200MV = 0x04
    HYST_400MV = 0x05
    HYST_800MV = 0x06
    HYST_1600MV = 0x07


class GPIO_THR(EnumBase):
    THR_1V5 = 0x00
    THR_3V0 = 0x01
    THR_6V0 = 0x02
    THR_9V0 = 0x03
    THR_12V = 0x04
    THR_15V = 0x05
    THR_18V = 0x06
    THR_21V = 0x07


class GPIO_POL(EnumBase):
    POL_ACTIVE_HIGH = 0x00
    POL_ACTIVE_LOW = 0x01


class UART_MODE(EnumBase):
    MODE_NONE = 0x00
    MODE_RAW = 0x01
    MODE_DMX512 = 0x02
    MODE_DMX512_RAW = 0x03
    MODE_MODBUS_RTU = 0x04


class UART_STATE(EnumBase):
    STATE_OK = 0x00
    STATE_BUSY = 0x01
    STATE_ERROR = 0x02
    STATE_ERROR_CRC = 0x03
    STATE_ERROR_TIMEOUT = 0x04
    STATE_PENDING = 0x05


class UART_STOPBITS(EnumBase):
    STOPBITS_0_5 = 0x00
    STOPBITS_1 = 0x01
    STOPBITS_2 = 0x02
    STOPBITS_1_5 = 0x03


class UART_PARITY(EnumBase):
    PARITY_NONE = 0x00
    PARITY_ODD = 0x01
    PARITY_EVEN = 0x02


class UART_485_EEPROM(EnumBase):
    RS485_NOSAVE = 0x00
    RS485_SAVE = 0x01


class UART_MIKROBUS1_EEPROM(EnumBase):
    MIKROBUS1_NOSAVE = 0x00
    MIKROBUS1_SAVE = 0x02


class UART_MIKROBUS2_EEPROM(EnumBase):
    MIKROBUS2_NOSAVE = 0x00
    MIKROBUS2_SAVE = 0x04


class GPIO_IO1_EEPROM(EnumBase):
    IO1_NOSAVE = 0x00
    IO1_SAVE = 0x01


class GPIO_IO2_EEPROM(EnumBase):
    IO2_NOSAVE = 0x00
    IO2_SAVE = 0x02


class GPIO_IO3_EEPROM(EnumBase):
    IO3_NOSAVE = 0x00
    IO3_SAVE = 0x04


class BOARD_TYPE(EnumBase):
    NONE = 0x00
    AUTOMATE_MINI = 0x01
    AUTOMATE_MAXI = 0x02


class BOARD_VARIANT(EnumBase):
    NONE = 0x00
    LIGHT = 0x01
    BASIC = 0x02
    FULL = 0x03


class LED_MODE(EnumBase):
    MODE_DEFAULT = 0x00
    MODE_0_5HZ = 0x01
    MODE_1_0HZ = 0x02
    MODE_2_0HZ = 0x03
    MODE_4_0HZ = 0x04
    MODE_8_0HZ = 0x05
    MODE_ON = 0x0E
    MODE_OFF = 0x0F


class I2C_START_ADDR(EnumBase):
    ADDR_START_0x08 = 0x00
    ADDR_START_0x10 = 0x01
    ADDR_START_0x18 = 0x02
    ADDR_START_0x20 = 0x03
    ADDR_START_0x28 = 0x04
    ADDR_START_0x30 = 0x05
    ADDR_START_0x38 = 0x06
    ADDR_START_0x40 = 0x07

    @staticmethod
    def to_address_value(enum_name):
        return int(enum_name.split("ADDR_START_")[1], 16)


class I2C_ADDR_CNT(EnumBase):
    ADDR_CNT_1 = 0x00
    ADDR_CNT_2 = 0x01
    ADDR_CNT_4 = 0x02


class SAVE_LED_CONF(EnumBase):
    NO_SAVE = 0x00
    SAVE_LED0 = 0x01


class SAVE_UART_CONF(EnumBase):
    SAVE_NONE = 0x00
    SAVE_UART_RS485 = 0x01
    SAVE_UART_MIKROBUS2 = 0x02
    SAVE_UART_BOTH = 0x03
    SAVE_UART_SWITCH = 0x04


class SAVE_IO_CONF(EnumBase):
    SAVE_NONE = 0x00
    SAVE_IO1 = 0x01
    SAVE_IO2 = 0x02
    SAVE_IO3 = 0x04
    SAVE_IO4 = 0x08
    SAVE_ALL = 0x0F


class EMU_IOEXP(EnumBase):
    IOEXP_DISABLED = 0x00
    IOEXP_ENABLED = 0x01


class EMU_RTC(EnumBase):
    RTC_DISABLED = 0x00
    RTC_ENABLED = 0x01


class BOOTLOADER_RESET(EnumBase):
    BOOT_STM32 = 0x31BE
    BOOT_ESP32 = 0x4383
    RESET_STM32 = 0x1AB2
    RESET_ESP32 = 0x62B2
    RESET_STM32_FACTORY = 0x82A1


class SWITCH_UART(EnumBase):
    UART_MIKROBUS1 = 0x01
    UART_RS485 = 0x02
    UART_STM32 = 0x03


class SWITCH_USB(EnumBase):
    USB_STM32 = 0x01
    USB_ESP32 = 0x02
    USB_DEBUG = 0x03


class REGMAP():
    IO_HEADER = {'header': '   External IO registers (IO1-IO3):', 'data': [
        ['   Config', 'Set IO mode (required)'],
        ['   Function', 'Set IO function (optional)'],
        ['   ADC Value', 'Input voltage in mV or ratio (for ratio functions)'],
        ['   DAC Value', 'Set output voltage in mV (not available for some functions)'],
        ['   DIG1 Value', 'Duty cycle (0..1000) for PWM functions, 0/1 for the default function or counter value (not available for some functions)'],
        ['   DIG2 Value', 'Frequency (0..5000) for PWM functions or counter value (not available for some functions)']],
         'col_width': [25, 100],
    }

    MAP_IO_1 = {
        REG.RW_GPIO1_CONF1: {'nicename': 'IO1 Config', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.RW_GPIO1_CONF2: {'nicename': 'IO1 Function', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.R_GPIO1_ADC_VAL: {'nicename': 'IO1 ADC Value (mV/ratio)', 'rw': 'r', 'format': 'dec'},
        REG.RW_GPIO1_DAC_VAL: {'nicename': 'IO1 DAC Value (mV)', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO1_DIG_VAL1: {'nicename': 'IO1 DIG1 Value', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO1_DIG_VAL2: {'nicename': 'IO1 DIG2 Value', 'rw': 'rw', 'format': 'dec'},
        -1: IO_HEADER,
    }

    MAP_IO_2 = {
        REG.RW_GPIO2_CONF1: {'nicename': 'IO2 Config', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.RW_GPIO2_CONF2: {'nicename': 'IO2 Function', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.R_GPIO2_ADC_VAL: {'nicename': 'IO2 ADC Value (mV/ratio)', 'rw': 'r', 'format': 'dec'},
        REG.RW_GPIO2_DAC_VAL: {'nicename': 'IO2 DAC Value (mV)', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO2_DIG_VAL1: {'nicename': 'IO2 DIG1 Value', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO2_DIG_VAL2: {'nicename': 'IO2 DIG2 Value', 'rw': 'rw', 'format': 'dec'},
        -1: IO_HEADER,
    }

    MAP_IO_3 = {
        REG.RW_GPIO3_CONF1: {'nicename': 'IO3 Config', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.RW_GPIO3_CONF2: {'nicename': 'IO3 Function', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.R_GPIO3_ADC_VAL: {'nicename': 'IO3 ADC Value (mV/ratio)', 'rw': 'r', 'format': 'dec'},
        REG.RW_GPIO3_DAC_VAL: {'nicename': 'IO3 DAC Value (mV)', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO3_DIG_VAL1: {'nicename': 'IO3 DIG1 Value', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO3_DIG_VAL2: {'nicename': 'IO3 DIG2 Value', 'rw': 'rw', 'format': 'dec'},
        -1: IO_HEADER,
    }

    MAP_IO_4 = {
        REG.RW_GPIO4_CONF1: {'nicename': 'IO4 Config', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.RW_GPIO4_CONF2: {'nicename': 'IO4 Function', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.R_GPIO4_ADC_VAL: {'nicename': 'IO4 ADC Value (mV/ratio)', 'rw': 'r', 'format': 'dec'},
        REG.RW_GPIO4_DAC_VAL: {'nicename': 'IO4 DAC Value (mV)', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO4_DIG_VAL1: {'nicename': 'IO4 DIG1 Value', 'rw': 'rw', 'format': 'dec'},
        REG.RW_GPIO4_DIG_VAL2: {'nicename': 'IO4 DIG2 Value', 'rw': 'rw', 'format': 'dec'},
        -1: IO_HEADER,
    }

    MAP_IO_EXP = {
        REG.RW_GPAB_IODIR: {'nicename': 'IO Exp. Direction', 'rw': 'rw', 'format': 'bin'},
        REG.RW_GPAB_IPOL: {'nicename': 'IO Exp. Polarity', 'rw': 'rw', 'format': 'bin'},
        REG.RW_GPAB_INTEN: {'nicename': 'IO Exp. Int. Enable', 'rw': 'rw', 'format': 'bin'},
        REG.RW_GPAB_GPPU: {'nicename': 'IO Exp. Pull-Up Enable', 'rw': 'rw', 'format': 'bin'},
        REG.RW_GPAB_GPPD: {'nicename': 'IO Exp. Pull-Down Enable', 'rw': 'rw', 'format': 'bin'},
        REG.RW_GPAB_DIG_VAL1: {'nicename': 'IO Exp. Value', 'rw': 'rw', 'format': 'bin'},
        -1: {'header': '   GPIO Expander registers:', 'data': [
            ['   Direction', '1=input, 0=output'],
            ['   Polarity', '1=Active low, 0=Active high'],
            ['   Interrupt', '1=Enable, 0=Disable'],
            ['   Pull-Up Enable', '1=Enable pull-up, 0=Disable pull-up'],
            ['   Pull-Down Enable', '1=Enable pull-down, 0=Disable pull-down'],
            ['   Value', 'Input value (direction = input) or output value (direction = output)']],
             'col_width': [25, 75],
             },
        -2: {'header': '  Bit position from left (15) to right (0):', 'data': [
            ['  (15) GPA7/PA0/BCM26', '(14) GPA6/PA3/BCM27', '(13) GPA5/PA9/BCM13', '(12) GPA4/PB4/BCM12'],
            ['  (11) UNUSED', '(10) GPA2/PB7/BCM6', '(9) GPA1/PB6/BCM5', '(8) GPA0/PB2/BCM4'],
            ['  (7) GPB7/PA15/BCM15', '(6) GPB6/PC2/BCM16 (M1)', '(5) GPB5/PC3/BCM20 (M2)', '(4) UNUSED'],
            ['  (3) GPB3/PC10/BCM22', '(2) GPB2/PC11/BCM23', '(1)  GPB1/PC12/BCM24', '(0) GPB0/PD2/BCM25'],
            [''],
            ['  GPAx/GPBx = GPIO reference for integrated MCP23017 I2C IO expander'],
            ['  PAx/PBx/PCx/PDx = GPIO reference for the STM32 MCU'],
            ['  BCMx = GPIO reference for the HAT socket (Pi Broadcom numbering)'],
            [
                '  Setting GPB6/GPB5 as output will disable the ADC functionality (Mikrobus AN), digital input mode is not supported'],
        ],
             'col_width': [25, 25, 25, 25],
             },
    }

    MAP_RTC = {
        REG.RW_RTC_WDAY_VAL: {'nicename': 'Weekday', 'rw': 'rw', 'format': 'dec'},
        REG.RW_RTC_SEC_VAL: {'nicename': 'Seconds', 'rw': 'rw', 'format': 'dec'},
        REG.RW_RTC_MIN_VAL: {'nicename': 'Minutes', 'rw': 'rw', 'format': 'dec'},
        REG.RW_RTC_HOUR_VAL: {'nicename': 'Hours', 'rw': 'rw', 'format': 'dec'},
        REG.RW_RTC_DAY_VAL: {'nicename': 'Day of month', 'rw': 'rw', 'format': 'dec'},
        REG.RW_RTC_MONTH_VAL: {'nicename': 'Month of year', 'rw': 'rw', 'format': 'dec'},
        REG.RW_RTC_YEAR_VAL: {'nicename': 'Year', 'rw': 'rw', 'format': 'dec'}
    }

    MAP_GEN_INFO = {
        REG.R_SW_INFO: {'nicename': 'SW version', 'rw': 'r', 'format': 'hex'},
        REG.R_HW_INFO: {'nicename': 'HW version', 'rw': 'r', 'format': 'hex'},
        REG.R_3V3_VAL: {'nicename': '3V3 rail voltage (mV)', 'rw': 'r', 'format': 'dec'},
        REG.R_5V0_VAL: {'nicename': '5V0 rail voltage (mV)', 'rw': 'r', 'format': 'dec'},
        REG.R_TEMP_VAL: {'nicename': 'Board temperature (°C)', 'rw': 'r', 'format': 'dec'},
        REG.R_SWITCH_VAL: {'nicename': 'Switch value', 'rw': 'r', 'format': 'dec'},
        REG.RW_LED_CONF: {'nicename': 'LED Config', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.R_GPIO_M1_AN_ADC_VAL: {'nicename': 'Mikrobus1 AN (mV)', 'rw': 'r', 'format': 'dec'},
        REG.R_GPIO_M2_AN_ADC_VAL: {'nicename': 'Mikrobus2 AN (mV)', 'rw': 'r', 'format': 'dec'},
        REG.R_GEN_ERROR1: {'nicename': 'General error register 1', 'rw': 'r', 'format': 'bin'},
        REG.R_GEN_ERROR2: {'nicename': 'General error register 2', 'rw': 'r', 'format': 'bin'},
    }

    REG_MAP_UART = {
        REG.RW_UART_RS485_CONF1: {'nicename': 'RS485 UART Config', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.RW_UART_RS485_CONF2: {'nicename': 'RS485 UART Baudrate', 'rw': 'rw', 'format': 'dec'},
    }

    REG_MAP_ADVANCED = {
        REG.RW_I2C_CONF: {'nicename': 'I2C Slave Config (MCU restart)', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.RW_EMU_CONF: {'nicename': 'Emulator Config (MCU restart)', 'rw': 'rw', 'format': 'hex', 'conf': True},
        REG.R_GPIO1_CUR: {'nicename': 'Estimated output current (IO1)', 'rw': 'r', 'format': 'dec'},
        REG.R_GPIO2_CUR: {'nicename': 'Estimated output current (IO2)', 'rw': 'r', 'format': 'dec'},
        REG.R_GPIO3_CUR: {'nicename': 'Estimated output current (IO3)', 'rw': 'r', 'format': 'dec'},
        REG.RW_SWITCH_CONF: {'nicename': 'ESP32 UART0 routing', 'rw': 'rw', 'format': 'hex', 'conf': True},
    }

    REG_MAP_EXPERT_ZONE = {
        REG.W_LED_SAVE: {'nicename': 'Write LED config to EEPROM', 'rw': 'w', 'format': 'bin', 'conf': True},
        REG.W_UART_SAVE: {'nicename': 'Write UART config to EEPROM', 'rw': 'w', 'format': 'bin', 'conf': True},
        REG.W_GPIO_SAVE: {'nicename': 'Write GPIO config to EEPROM', 'rw': 'w', 'format': 'bin', 'conf': True},
        REG.W_BOOTLOADER: {'nicename': 'ESP32/STM32 reset and boot', 'rw': 'w', 'format': 'bin', 'conf': True},
        REG.RW_ESP32_DELAY: {'nicename': 'ESP32 startup delay (ms)', 'rw': 'rw', 'format': 'dec'},
        REG.R_PERF_CNT1: {'nicename': 'Loops per second', 'rw': 'r', 'format': 'dec'},
        REG.R_PERF_CNT2: {'nicename': 'Max loop time (ms)', 'rw': 'r', 'format': 'dec'},
        REG.R_PERF_CNT3: {'nicename': 'Min loop time (ms)', 'rw': 'r', 'format': 'dec'},
        REG.R_DEBUG1: {'nicename': 'Debug register 1', 'rw': 'r', 'format': 'dec'},
        REG.R_DEBUG2: {'nicename': 'Debug register 2', 'rw': 'r', 'format': 'dec'},
    }


class Convert(object):

    @staticmethod
    def str_to_int(input_str):
        """Helper method to convert string based integers to python integers"""

        if input_str.startswith("0x"):
            int_value = int(input_str, 16)
        elif input_str.startswith("0b"):
            int_value = int(input_str, 2)
        else:
            int_value = int(input_str, 10)

        return int_value


class Modbus(object):

    _last_function_code = 0
    _last_slave_address = 0
    _last_register_address = 0
    _last_byte_count = 0
    _last_resp_message_len = 0

    @classmethod
    def build_rtu_frame(cls, slave_address, function_code, register_address, register_count=1, values=[]):
        """Helper method to build a modbus RTU frame"""

        message_len = 6

        if type(values) is not list:
            values = [values]

        # Correct for modbus register offset
        if 40001 <= register_address <= 49999:
            register_address -= 40001
        elif 30001 <= register_address <= 39999:
            register_address -= 30001

        if function_code == 16:
            register_count = len(values)
            message_len += ((register_count * 2) + 1)

        message = [
            REG.W_UART_RS485_TX_PTR,                # Message start address
            [
                0, 0,                               # (W_UART_RS485_TX_PTR) Set TX buffer pointer to 0
                0, message_len,                     # (W_UART_RS485_TX_LEN) Set Modbus message length (without CRC) correct (in bytes!)
                slave_address,                      # (W_UART_RS485_TX_VAL) Write Modbus slave address in TX buffer
                function_code,                      # (W_UART_RS485_TX_VAL) Write Modbus function code in TX buffer
                (register_address & 0xFF00) >> 8,   # (W_UART_RS485_TX_VAL) Write Modbus register address in TX buffer
                (register_address & 0x00FF) >> 0,   # (W_UART_RS485_TX_VAL) Write Modbus register address in TX buffer
                (register_count & 0xFF00) >> 8,     # (W_UART_RS485_TX_VAL) write Modbus register count in TX buffer
                (register_count & 0x00FF) >> 0,     # (W_UART_RS485_TX_VAL) write Modbus register count in TX buffer
            ]
        ]

        if values and function_code == 16:
            message[1].append(len(values) * 2)      # (W_UART_RS485_TX_VAL) Write Modbus byte count in TX buffer
            for value in values:                    # (W_UART_RS485_TX_VAL) Write Modbus register values in TX buffer
                message[1].append((value & 0xFF00) >> 8)
                message[1].append((value & 0x00FF) >> 0)

        message[1].extend([0, 0])                   # (W_UART_RS485_TX_SEND) Send TX buffer to end device
        return message

    @classmethod
    def decode_rtu_frame(cls, response_frame):
        """Helper method to decode a modbus RTU frame"""

        function_code = response_frame[1]
        error_code = 'ERROR'

        response_decoded = []

        if function_code == 3 or function_code == 4:
            byte_count = response_frame[2]

            for i in range(0, byte_count, 2):
                response_decoded.append((response_frame[3 + i] << 8) | response_frame[4 + i])
            error_code = None

        elif function_code == 16:

            register_start_address = (response_frame[2] << 8) | response_frame[3]
            register_count = (response_frame[4] << 8) | response_frame[5]

            if register_start_address == cls._last_register_address:
                error_code = None

        return [error_code, response_decoded]


class Dmx512(object):

    @classmethod
    def build_dmx512_frame(cls, slot, values=[]):
        """Helper method to build a DMX512 frame"""

        if slot < 0 or slot > 512:
            raise Exception("Slot out of range (1-512)")

        response_len = 0

        if type(values) is not list:
            values = [values]

        message = [
            REG.W_UART_RS485_TX_PTR,                # Message start address
            [
                (slot & 0xFF00) >> 8,               # (W_UART_RS485_TX_PTR) Set TX buffer pointer to DMX512 slot
                (slot & 0x00FF) >> 0,               # (W_UART_RS485_TX_PTR) Set TX buffer pointer to DMX512 slot
                (len(values) & 0xFF00) >> 8,        # (W_UART_RS485_TX_LEN) Set message length (in bytes!)
                (len(values) & 0x00FF) >> 0,        # (W_UART_RS485_TX_LEN) Set message length (in bytes!)
            ]
        ]

        for value in values:
            if value < 0 or value > 255:
                raise Exception("Value out of range (0-255)")
            message[1].append(value)                # (W_UART_RS485_TX_VAL) Write DMX512 value in TX buffer

        message[1].extend([0, 0])                   # (W_UART_RS485_TX_SEND) Send TX buffer to end device

        return [response_len, message]



