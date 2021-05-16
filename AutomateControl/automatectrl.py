#!/usr/bin/python3

import time
import platform
import os
import sys
import PySimpleGUI as sg

from utils import *
from connection import DeviceConnection
from screeninfo import get_monitors

DEFAULT_UART_PORT           = ""
DEFAULT_I2C_ADDRESS         = 0x2A
DEFAULT_I2C_BUS             = 0x01

CONF_REG_VALUE_WIDTH        = 64
CONF_REG_DESCR_WIDTH        = 32
CONF_REG_MODBUS_DESC_WIDTH  = CONF_REG_DESCR_WIDTH + 9

SCREEN_POS_X                = 0
SCREEN_POS_Y                = 0

GUI_TABKEY_IO1              = "_TAB_KEY_IO1_"
GUI_TABKEY_IO2              = "_TAB_KEY_IO2_"
GUI_TABKEY_IO3              = "_TAB_KEY_IO3_"
GUI_TABKEY_IO_EXP           = "_TAB_KEY_IO_EXP_"
GUI_TABKEY_IO_GPB           = "_TAB_KEY_IO_GPB_"
GUI_TABKEY_IO_BCM           = "_TAB_KEY_IO_BCM_"
GUI_TABKEY_RTC              = "_TAB_KEY_RTC_"
GUI_TABKEY_GEN_INFO         = "_TAB_KEY_GEN_INFO_"
GUI_TABKEY_NETWORK          = "_TAB_KEY_NETWORK_"
GUI_TABKEY_UART             = "_TAB_KEY_UART_"
GUI_TABKEY_ADVANCED         = "_TAB_KEY_ADVANCED_"
GUI_TABKEY_EXPERT           = "_TAB_KEY_EXPERT_"

GUI_KEY_MODBUS_REG          = "_KEY_TEXT_MODBUS_REG_"
GUI_KEY_MODBUS_REG_LEN      = "_KEY_TEXT_MODBUS_REG_LEN_"
GUI_KEY_MODBUS_CODE         = "_KEY_TEXT_MODBUS_CODE_"
GUI_KEY_MODBUS_SLAVE        = "_KEY_TEXT_MODBUS_SLAVE_"
GUI_KEY_MODBUS_TXBUT        = "_KEY_TEXT_MODBUS_TXBUT_"
GUI_KEY_MODBUS_RESP         = "_KEY_TEXT_MODBUS_RESP_"
GUI_KEY_MODBUS_REG_VAL      = "_KEY_TEXT_MODBUS_REG_VAL_"
GUI_KEY_DMX512_SLOT         = "_KEY_TEXT_DMX512_SLOT_"
GUI_KEY_DMX512_TXVAL        = "_KEY_TEXT_DMX512_VAL_"
GUI_KEY_DMX512_TXBUT        = "_KEY_TEXT_DMX512_TXBUT_"

GUI_OK                      = "Ok"
GUI_CANCEL                  = "Cancel"


def get_window_location(sizex, sizey):
    """Helper to get center coordinates of window"""

    return int(SCREEN_POS_X - sizex / 2), int(SCREEN_POS_Y - sizey / 2)


def register_decoder(register_address, register_value):
    """Decode register value to descriptive text"""

    try:
        # Decode IO1-IO4 configuration registers
        if REG.RW_GPIO1_CONF1 <= register_address <= REG.RW_GPIO4_CONF1:
            response = str(GPIO_MODE((register_value & 0xE000) >> 13).name)
            response += ", " + str(GPIO_PULL((register_value & 0x1800) >> 11).name)
            response += ", " + str(GPIO_THR((register_value & 0x00F0) >> 4).name)
            response += ", " + str(GPIO_HYST((register_value & 0x000F) >> 0).name)
            return response

        # Decode SW version info
        elif register_address == REG.R_SW_INFO:
            return str("%i.%i.%i" %
                       ((register_value & 0xF000) >> 12, (register_value & 0x0F00) >> 8, (register_value & 0x00FF)))

        # Decode HW version info
        elif register_address == REG.R_HW_INFO:
            return str("%s %s Rev. %i" %
                       (BOARD_TYPE((register_value & 0xF000) >> 12).name,
                        BOARD_VARIANT((register_value & 0x0F00) >> 8).name, (register_value & 0x00FF)))

        # Decode LED Config
        elif register_address == REG.RW_LED_CONF:
            return str("LED0 %s" % (LED_MODE(register_value & 0x000F).name))

        # Decode IO1-IO4 function registers
        elif REG.RW_GPIO1_CONF2 <= register_address <= REG.RW_GPIO4_CONF2:
            return str(GPIO_FUNC(register_value).name)

        # Decode UART configuration register
        elif (register_address == REG.RW_UART_RS485_CONF1 or
              register_address == REG.RW_UART_MIKRO2_CONF1):
            response = str(UART_MODE((register_value & 0xFF00) >> 8).name)
            response += ", " + str(UART_STOPBITS((register_value & 0x00C0) >> 6).name)
            response += ", " + str(UART_PARITY((register_value & 0x0030) >> 4).name)
            return response

        # Decode UART baudrate setting
        elif (register_address == REG.RW_UART_RS485_CONF2 or
              register_address == REG.RW_UART_MIKRO2_CONF2):
            return str(register_value * 100)

        # Decode I2C configuration register
        elif register_address == REG.RW_I2C_CONF:
            return str("%s, %s" % (I2C_ADDR_CNT((register_value & 0x0300) >> 8).name,
                                  I2C_START_ADDR(register_value & 0x000F).name))

        # Decode emulator configuration register
        elif register_address == REG.RW_EMU_CONF:
            return str("%s, %s" % (EMU_RTC((register_value & 0x0002) >> 1).name,
                                   EMU_IOEXP(register_value & 0x0001).name))

        # Decode USB and UART switch state
        elif register_address == REG.RW_SWITCH_CONF:
            return str("%s" % (SWITCH_UART(register_value).name))

    except Exception:
        return "ERROR"
        
    return ""


def format_response(register_address, value, window_values, decode=True):
    """Format response as binary, hex or decimal string"""

    response = ""
    int_value = value

    # Display as hexadecimal value
    if window_values[str('_KEY_FORMAT_HEX_%s' % register_address)]:
        response = str('0x%04X' % value)

    # Display as decimal value
    elif window_values[str('_KEY_FORMAT_DEC_%s' % register_address)]:
        response = str(value)

    # Display network settings as x.x.x.x
    elif (str('_KEY_FORMAT_IP_%s' % register_address) in window_values and 
            window_values[str('_KEY_FORMAT_IP_%s' % register_address)]):
        response = str("%i.%i" % ((int_value & 0xFF00) >> 8, int_value & 0x00FF))

    # Display as binary
    else:
        response = '0b' + format(int_value, '016b')

    # Add more information
    if decode:
        reg_decoded = register_decoder(register_address, int_value)
        if reg_decoded:
            response += (" [" + reg_decoded + "]")
        
    return response


def gui_format_tab(reg_map_dict):
    response = []

    for key in reg_map_dict.keys():
        if key >= 0:
            response.append([
                sg.Text(str('[0x%02x] %s' % (key, reg_map_dict[key].get('nicename'))), size=(CONF_REG_DESCR_WIDTH, 1)),
                sg.CBox('Edit', disabled=reg_map_dict[key].get('rw') == 'r', enable_events=True,
                        key=str('_KEY_EDIT_%s' % key)),
                sg.In(disabled=True, key=str('_KEY_TEXT_%s' % key), size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)
            ])

            # Add configuration button if required
            if reg_map_dict[key].get('conf', False):
                response[-1].extend([sg.B('Configure', key=str('_KEY_CONF_%s' % key), enable_events=True, disabled=True, size=(10, 1))])
            else:
                response[-1].extend([sg.B('', disabled=True, size=(10, 1))])

            response[-1].extend([
                sg.B('Write', key=str('_KEY_WRITE_%s' % key), enable_events=True, disabled=True),
                sg.Radio('Hex', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_HEX_%s' % key),
                         default=reg_map_dict[key].get('format') == 'hex'),
                sg.Radio('Dec', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_DEC_%s' % key),
                         default=reg_map_dict[key].get('format') == 'dec'),
                sg.Radio('Bin', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_BIN_%s' % key),
                         default=reg_map_dict[key].get('format') == 'bin'),
            ])

            # Add IP format for network config registers
            if reg_map_dict[key].get('format') == 'ip':
                response[-1].extend([sg.Radio('Ip', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_IP_%s' % key),
                                              default=reg_map_dict[key].get('format') == 'ip')])
        else:
            descr_table = reg_map_dict[key].get('data')
            table_width = reg_map_dict[key].get('col_width')
            header = reg_map_dict[key].get('header')

            # Add white space
            response.append([sg.Text('', font=("Helvetica", 5))])

            # Add header
            if header:
                response.append([sg.Text(header, border_width=None, background_color=None, font=("Helvetica", 12),
                                         pad=(0, 0), size=(sum(table_width), 1))])

            # Add description / table data
            for desc_line in descr_table:
                if type(desc_line) is list:
                    response.append([sg.Text(desc_col, border_width=None, background_color=None,
                                         pad=(0, 0), size=(table_width[i] if len(desc_line) > 1 else sum(table_width), 1)) for i, desc_col in enumerate(desc_line)])
    return response


def gui_format_tab_uart(reg_map_dict):

    response = gui_format_tab(reg_map_dict)

    for key in reg_map_dict.keys():

        response.append([
            sg.Text(str('[0x%02x] %s' % (key, reg_map_dict[key].get('nicename'))), size=(CONF_REG_DESCR_WIDTH, 1)),
            sg.CBox('Edit', disabled=reg_map_dict[key].get('rw') == 'r', enable_events=True,
                    key=str('_KEY_EDIT_%s' % key)),
            sg.In(disabled=True, key=str('_KEY_TEXT_%s' % key), size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)
        ])

        # Add configuration button if required
        if reg_map_dict[key].get('conf', False):
            response[-1].extend([sg.B('Configure', key=str('_KEY_CONF_%s' % key), enable_events=True, disabled=True, size=(10, 1))])
        else:
            response[-1].extend([sg.B('', disabled=True, size=(10, 1))])

        response[-1].extend([
            sg.B('Write', key=str('_KEY_WRITE_%s' % key), enable_events=True, disabled=True),
            sg.Radio('Hex', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_HEX_%s' % key),
                     default=reg_map_dict[key].get('format') == 'hex'),
            sg.Radio('Dec', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_DEC_%s' % key),
                     default=reg_map_dict[key].get('format') == 'dec'),
            sg.Radio('Bin', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_BIN_%s' % key),
                     default=reg_map_dict[key].get('format') == 'bin'),
        ])

        # Add IP format for network config registers
        if reg_map_dict[key].get('format') == 'ip':
            response[-1].extend([sg.Radio('Ip', str('_KEY_FORMAT_%s' % key), key=str('_KEY_FORMAT_IP_%s' % key),
                                          default=reg_map_dict[key].get('format') == 'ip')])

    return response


def gui_config_popup(settings):
    layout_popup = [[sg.Text('Configuration')]]

    for idx, setting in enumerate(settings):
        values = setting.get_list()
        size_y = min(max(len(values), 5), 8)
        layout_popup.append(
            [sg.Listbox(values, size=(32, size_y), default_values=[values[0]], key=str(idx))])

    layout_popup.append([sg.Button(GUI_OK), sg.Button(GUI_CANCEL)])
    window_popup = sg.Window('CONFIG', layout_popup, location=get_window_location(0, 0))

    event, values = window_popup.read()
    window_popup.close()

    if event == GUI_OK:
        response = []
        for idx, setting in enumerate(settings):
            response.append(setting.get_by_name(values[str(idx)][0]))
        return response

    return None


def gui_connection_popup():
    """Request connection parameters from user"""

    OPT1_TXT_KEY    = '_OPT1_TXT_'
    OPT2_TXT_KEY    = '_OPT2_TXT_'
    OPT1_KEY        = '_OPT1_'
    OPT2_KEY        = '_OPT2_'
    USB_EN_KEY      = '_CON_TYPE_UART_'
    I2C_EN_KEY      = '_CON_TYPE_I2C_'

    layout_popup = [[sg.Text('Connection settings')],
                    [sg.Radio('I2C', 'CON_TYPE', key=I2C_EN_KEY, enable_events=True, default=False)],
                    [sg.Radio('USB/UART', 'CON_TYPE', key=USB_EN_KEY, enable_events=True, default=True)],
                    [sg.Text('', key=OPT1_TXT_KEY, size=(20, 1)), sg.In('', key=OPT1_KEY)],
                    [sg.Text('', key=OPT2_TXT_KEY, size=(20, 1)), sg.In('', key=OPT2_KEY)],
                    [sg.Button(GUI_OK), sg.Button(GUI_CANCEL)]]

    window_popup = sg.Window('CONFIG', layout_popup, size=(500, 210), location=get_window_location(500, 210))
    window_setup = True

    while True:
        event, values = window_popup.read(timeout=10 if window_setup else 250)
        if event in (sg.WIN_CLOSED, 'Quit', GUI_CANCEL):
            window_popup.close()
            return None

        if event == GUI_OK:
            break

        if event == I2C_EN_KEY or event == USB_EN_KEY or window_setup:
            window_setup = False
            if values[USB_EN_KEY]:
                window_popup[OPT1_TXT_KEY].update(value='USB/UART port')
                window_popup[OPT1_KEY].update(value=DEFAULT_UART_PORT)
                window_popup[OPT2_TXT_KEY].update(value='')
                window_popup[OPT2_KEY].update(value=str(DEFAULT_I2C_BUS), visible=False)
            else:
                window_popup[OPT1_TXT_KEY].update(value='I2C slave address')
                window_popup[OPT1_KEY].update(value=str(DEFAULT_I2C_ADDRESS))
                window_popup[OPT2_TXT_KEY].update(value='I2C bus')
                window_popup[OPT2_KEY].update(value=str(DEFAULT_I2C_BUS), visible=True)

    window_popup.close()

    return ['uart' if values[USB_EN_KEY] else 'i2c', values[OPT1_KEY], values[OPT2_KEY]]


modbus_request = False


def main():
    """Application entry point"""

    if os.geteuid() == 0:
        sys.exit("This software is not supposed to be run as root!")

    io1_io2_layout = []
    io3_io4_layout = []
    ioexp_layout = []
    modbus_rx_len = 0

    global modbus_request
    global DEFAULT_UART_PORT
    global SCREEN_POS_X
    global SCREEN_POS_Y

    # Get center position coordinates of monitor
    for monitor in get_monitors():
        SCREEN_POS_X = int(monitor.width / 2)
        SCREEN_POS_Y = int(monitor.height / 2)
        break

    # Check platform support
    if "linux" in platform.system().lower():
        DEFAULT_UART_PORT = "/dev/ttyACM0"
    elif "windows" in platform.system().lower():
        DEFAULT_UART_PORT = "COM1"
    else:
        sg.Popup('OS not supported!', location=(SCREEN_POS_X, SCREEN_POS_Y))
        sys.exit(1)

    # Open connection to slave microcontroller
    while True:
        connection_settings = gui_connection_popup()
        if not connection_settings:
            sys.exit(0)

        [_type, opt1, opt2] = connection_settings
        try:
            if _type == 'uart':
                dev_con = DeviceConnection(mode='uart_usb', port=opt1)
            else:
                dev_con = DeviceConnection(mode='i2c', port=opt1, bus=opt2)
            break
        except Exception:
            sg.Popup('Connection failed!', location=(SCREEN_POS_X, SCREEN_POS_Y))

    # Get board hardware info
    hwinfo_reg = dev_con.get_register(REG.R_HW_INFO)
    board_type = ((hwinfo_reg & 0xF000) >> 12)
    board_variant = ((hwinfo_reg & 0x0F00) >> 8)

    # Set options depending on variant
    rtc_supported = (board_type == BOARD_TYPE.AUTOMATE_MINI and board_variant == BOARD_VARIANT.FULL)
    rs485_supported = (board_type == BOARD_TYPE.AUTOMATE_MINI and board_variant == BOARD_VARIANT.FULL)
    can_supported = (board_type == BOARD_TYPE.AUTOMATE_MINI and board_variant == BOARD_VARIANT.FULL)

    if board_type != BOARD_TYPE.AUTOMATE_MINI:
        sys.exit("Board not supported by this tool!")

    def gui_update_tab(reg_address_start, reg_address_stop):
        """Get / update all registers for range"""

        reg_values = dev_con.get_registers(reg_address_start, reg_address_stop - reg_address_start + 1)
        for i in range(reg_address_start, reg_address_stop + 1):
            if str('_KEY_TEXT_%i' % i) in gui_window.AllKeysDict:
                if not values[str('_KEY_EDIT_%i' % i)]:
                    gui_window[str('_KEY_TEXT_%i' % i)].update(value=format_response(i, reg_values[i - reg_address_start], values))

    def gui_update_tab_modbus_dmx512():
        """Get / update all modbus and DMX512 registers"""

        global modbus_request

        # txval_str = str("%02x%02x %04x %04x" % (Convert.str_to_int(values[GUI_KEY_MODBUS_SLAVE]),
        #                                         Convert.str_to_int(values[GUI_KEY_MODBUS_CODE]),
        #                                         Convert.str_to_int(values[GUI_KEY_MODBUS_REG]),
        #                                         Convert.str_to_int(values[GUI_KEY_MODBUS_REG_LEN])))

        modbus_enabled = 'modbus' in values[str('_KEY_TEXT_%s' % REG.RW_UART_RS485_CONF1)].lower()
        dmx512_enabled = 'dmx512' in values[str('_KEY_TEXT_%s' % REG.RW_UART_RS485_CONF1)].lower()
        gui_window[GUI_KEY_MODBUS_TXBUT].update(disabled=not modbus_enabled)
        gui_window[GUI_KEY_DMX512_TXBUT].update(disabled=not dmx512_enabled)

        if modbus_enabled and modbus_request:
            modbus_request_mode = (values[GUI_KEY_MODBUS_CODE] == str(4) or
                                   values[GUI_KEY_MODBUS_CODE] == str(3))  # TODO support for function 1 and 2?
            gui_window[GUI_KEY_MODBUS_REG_VAL].update(disabled=modbus_request_mode)
            gui_window[GUI_KEY_MODBUS_REG_LEN].update(disabled=not modbus_request_mode)
            rx_state = dev_con.get_register(REG.R_UART_RS485_RX_STATUS)

            if UART_STATE(rx_state) == UART_STATE.STATE_OK:
                rx_len = dev_con.get_register(REG.R_UART_RS485_RX_PEND)
                dev_con.set_register(REG.W_UART_RS485_RX_LEN, rx_len)
                gui_window[GUI_KEY_MODBUS_RESP].update(value=str(dev_con.get_registers(REG.R_UART_RS485_RX_VAL, register_len=int(rx_len/2))))
                modbus_request = False
            else:
                gui_window[GUI_KEY_MODBUS_RESP].update(value=str(UART_STATE(rx_state).name))

    # Build GUI tab layout
    gui_layout_tabs = []
    uart_layout = gui_format_tab(REGMAP.REG_MAP_UART)
    uart_layout.append([sg.Text('')])
    uart_layout.append([sg.Text('RS485 Modbus RTU Master/Client (Requires UART in modbus mode)')])
    uart_layout.append([sg.Text('Slave address (1-255)', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('1', disabled=False, key=GUI_KEY_MODBUS_SLAVE, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('Function code (3, 4 or 16)', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('4', disabled=False, key=GUI_KEY_MODBUS_CODE, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('Register address', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('1', disabled=False, key=GUI_KEY_MODBUS_REG, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('Register count', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('1', disabled=False, key=GUI_KEY_MODBUS_REG_LEN, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('Register value(s) (comma separated)', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('1', disabled=False, key=GUI_KEY_MODBUS_REG_VAL, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.B('Send/Request', key=GUI_KEY_MODBUS_TXBUT, enable_events=True, disabled=False)])
    uart_layout.append([sg.Text('Response', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In(disabled=True, key=GUI_KEY_MODBUS_RESP, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('')])
    uart_layout.append([sg.Text('RS485 DMX512 (Requires UART in DMX512 mode)')])
    uart_layout.append([sg.Text('Start channel/slot (1-512)', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('1', key=GUI_KEY_DMX512_SLOT, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append([sg.Text('Value(s) (comma separated, 0-255)', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)),
                        sg.In('0', key=GUI_KEY_DMX512_TXVAL, size=(CONF_REG_VALUE_WIDTH, 1), enable_events=True)])
    uart_layout.append(
        [sg.Text('', size=(CONF_REG_MODBUS_DESC_WIDTH, 1)), sg.B('Send', key=GUI_KEY_DMX512_TXBUT, enable_events=True)])

    gui_layout_tabs.append(
        sg.Tab('General', gui_format_tab(REGMAP.MAP_GEN_INFO), tooltip='Generic device info', key=GUI_TABKEY_GEN_INFO))

    gui_layout_tabs.append(sg.Tab('IO1', gui_format_tab(REGMAP.MAP_IO_1), key=GUI_TABKEY_IO1))
    gui_layout_tabs.append(sg.Tab('IO2', gui_format_tab(REGMAP.MAP_IO_2), key=GUI_TABKEY_IO2))
    gui_layout_tabs.append(sg.Tab('IO3', gui_format_tab(REGMAP.MAP_IO_3), key=GUI_TABKEY_IO3))
    gui_layout_tabs.append(sg.Tab('IO Expander', gui_format_tab(REGMAP.MAP_IO_EXP), key=GUI_TABKEY_IO_EXP))

    # Add RS485, RTC and CAN bus tabs only if supported by board
    if rs485_supported:
        gui_layout_tabs.append(sg.Tab('RS485', uart_layout, tooltip='UART and RS485 settings', key=GUI_TABKEY_UART))
    if rtc_supported:
        gui_layout_tabs.append(
            sg.Tab('RTC', gui_format_tab(REGMAP.MAP_RTC), tooltip='Real time clock', key=GUI_TABKEY_RTC))

    gui_layout_tabs.append(
        sg.Tab('Advanced settings', gui_format_tab(REGMAP.REG_MAP_ADVANCED), tooltip='Advanced settings', key=GUI_TABKEY_ADVANCED))
    gui_layout_tabs.append(
        sg.Tab('Expert settings', gui_format_tab(REGMAP.REG_MAP_EXPERT_ZONE), tooltip='Expert settings', key=GUI_TABKEY_EXPERT))

    gui_layout = [[sg.TabGroup([gui_layout_tabs], tooltip='', key='_TABGROUP_')]]

    # Show the layout on screen
    gui_window = sg.Window('AutoMATE Slave Control', gui_layout, size=(1170, 800), location=get_window_location(1170, 900))

    # Poll registers continuously for updates
    while True:
        event, values = gui_window.read(timeout=250)
        if event in (sg.WIN_CLOSED, 'Quit'):
            break

        # Enable/disable register edit mode
        if event.startswith('_KEY_EDIT_'):
            index = event.split('_KEY_EDIT_')[1]
            if str('_KEY_CONF_%s' % index) in gui_window.AllKeysDict:
                gui_window[str('_KEY_CONF_%s' % index)].update(disabled=(not values[event]))
                if not values[event]:
                    gui_window[str('_KEY_WRITE_%s' % index)].update(disabled=True)
            else:
                gui_window[str('_KEY_TEXT_%s' % index)].update(disabled=(not values[event]))
                gui_window[str('_KEY_WRITE_%s' % index)].update(disabled=(not values[event]))

        # Open register configuration popup window
        elif event.startswith('_KEY_CONF_'):

            index = int(event.split('_KEY_CONF_')[1])
            register_value = 0

            # Enable write button
            gui_window[str('_KEY_WRITE_%s' % index)].update(disabled=False)

            # Write local IO1-IO4 GPIO configuration registers
            if REG.RW_GPIO1_CONF1 <= index <= REG.RW_GPIO4_CONF1:

                response = gui_config_popup([GPIO_MODE, GPIO_PULL, GPIO_THR, GPIO_HYST, GPIO_POL])

                if response:
                    register_value |= (response[0] << 13)
                    register_value |= (response[1] << 11)
                    register_value |= (response[2] << 4)
                    register_value |= (response[3] << 0)
                    register_value |= (response[4] << 10)

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write local IO1-IO4 function configuration registers
            elif REG.RW_GPIO1_CONF2 <= index <= REG.RW_GPIO4_CONF2:

                response = gui_config_popup([GPIO_FUNC])

                if response:
                    register_value = response[0]

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write LED configuration register
            elif index == REG.RW_LED_CONF:

                response = gui_config_popup([LED_MODE])

                if response:
                    register_value |= (response[0] << 0)

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write local UART configuration registers
            elif index == REG.RW_UART_RS485_CONF1 or \
                    index == REG.RW_UART_MIKRO2_CONF1:

                response = gui_config_popup([UART_MODE, UART_STOPBITS, UART_PARITY])

                if response:

                    register_value |= (response[0] << 8)
                    register_value |= (response[1] << 6)
                    register_value |= (response[2] << 4)

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write I2C configuration register
            elif index == REG.RW_I2C_CONF:

                response = gui_config_popup([I2C_ADDR_CNT, I2C_START_ADDR])

                if response:
                    register_value |= (response[0] << 8)
                    register_value |= (response[1] << 0)

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write emulator configuration register
            elif index == REG.RW_EMU_CONF:

                response = gui_config_popup([EMU_RTC, EMU_IOEXP])

                if response:
                    register_value |= (response[0] << 1)
                    register_value |= (response[1] << 0)

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write LED EEPROM register
            elif index == REG.W_LED_SAVE:

                response = gui_config_popup([SAVE_LED_CONF])

                if response:
                    register_value = response[0]

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write UART EEPROM register
            elif index == REG.W_UART_SAVE:

                response = gui_config_popup([SAVE_UART_CONF])

                if response:
                    register_value = response[0]

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

            # Write GPIO EEPROM register
            elif index == REG.W_GPIO_SAVE:

                    response = gui_config_popup([SAVE_IO_CONF])

                    if response:
                        register_value = response[0]

                        gui_window[str('_KEY_TEXT_%i' % index)].update(
                            value=format_response(index, register_value, values, False))

            # Write bootloader register
            elif index == REG.W_BOOTLOADER:

                    response = gui_config_popup([BOOTLOADER_RESET])

                    if response:
                        register_value = response[0]

                        gui_window[str('_KEY_TEXT_%i' % index)].update(
                            value=format_response(index, register_value, values, False))

            # Write UART and USB switch state
            elif index == REG.RW_SWITCH_CONF:

                response = gui_config_popup([SWITCH_UART])

                if response:
                    register_value = response[0]

                    gui_window[str('_KEY_TEXT_%i' % index)].update(
                        value=format_response(index, register_value, values, False))

        elif event.startswith(GUI_KEY_MODBUS_TXBUT):
            gui_window[GUI_KEY_MODBUS_RESP].update(value='pending...')

            tx_values = values[GUI_KEY_MODBUS_REG_VAL]
            if ',' in tx_values:
                tx_values = tx_values.split(',')
            else:
                tx_values = [tx_values]

            tx_values = [Convert.str_to_int(tx_val) for tx_val in tx_values]

            modbus_message = Modbus.build_rtu_frame(
                function_code=Convert.str_to_int(values[GUI_KEY_MODBUS_CODE]),
                slave_address=Convert.str_to_int(values[GUI_KEY_MODBUS_SLAVE]),
                register_address=Convert.str_to_int(values[GUI_KEY_MODBUS_REG]),
                register_count=Convert.str_to_int(values[GUI_KEY_MODBUS_REG_LEN]),
                values=tx_values
            )

            print(modbus_message)
            dev_con.set_registers(modbus_message[0], modbus_message[1], format_bytes=True)

            modbus_request = True

        elif event.startswith(GUI_KEY_DMX512_TXBUT):

            tx_values = values[GUI_KEY_DMX512_TXVAL]
            if ',' in tx_values:
                tx_values = tx_values.split(',')
            else:
                tx_values = [tx_values]

            tx_values = [Convert.str_to_int(tx_val) for tx_val in tx_values]

            [response_len, dmx512_message] = Dmx512.build_dmx512_frame(
                slot=Convert.str_to_int(values[GUI_KEY_DMX512_SLOT]),
                values=tx_values
            )

            print(dmx512_message)
            print(modbus_rx_len)
            dev_con.set_registers(dmx512_message[0], dmx512_message[1], format_bytes=True)

        # Write modified register to device
        elif event.startswith('_KEY_WRITE_'):
            index = event.split('_KEY_WRITE_')[1]

            # Send to hardware device
            try:
                dev_con.set_register(int(index), Convert.str_to_int(values[str('_KEY_TEXT_%s' % index)].strip()))
            except ValueError:
                sg.Popup('Oops!', 'Only numbers are accepted!', location=(SCREEN_POS_X, SCREEN_POS_Y))

            # I2C slave needs some time to re-initialize
            if int(index) == REG.RW_I2C_CONF:
                time.sleep(1)
                new_addr = Convert.str_to_int(values[str('_KEY_TEXT_%s' % index)]) & 0x000F
                dev_con.address = I2C_START_ADDR.to_address_value(I2C_START_ADDR(new_addr).name)

            # Disable edit mode again after transmit
            gui_window[str('_KEY_EDIT_%s' % index)].update(value=False)
            gui_window[str('_KEY_TEXT_%s' % index)].update(disabled=True)
            gui_window[str('_KEY_WRITE_%s' % index)].update(disabled=True)
            if str('_KEY_CONF_%s' % index) in gui_window.AllKeysDict:
                gui_window[str('_KEY_CONF_%s' % index)].update(disabled=True)

        if values['_TABGROUP_'] == GUI_TABKEY_IO1 or \
                values['_TABGROUP_'] == GUI_TABKEY_IO2 or \
                values['_TABGROUP_'] == GUI_TABKEY_IO3:
            gui_update_tab(REG.R_GPIO1_ADC_VAL, REG.R_GPIO4_ADC_VAL)
            gui_update_tab(REG.RW_GPIO1_DAC_VAL, REG.RW_GPIO4_DAC_VAL)
            gui_update_tab(REG.RW_GPIO1_DIG_VAL1, REG.RW_GPIO4_DIG_VAL1)
            gui_update_tab(REG.RW_GPIO1_DIG_VAL2, REG.RW_GPIO4_DIG_VAL2)
            gui_update_tab(REG.RW_GPIO1_CONF1, REG.RW_GPIO4_CONF2)

        elif values['_TABGROUP_'] == GUI_TABKEY_IO_EXP:
            gui_update_tab(REG.RW_GPAB_IODIR, REG.RW_GPAB_GPPD)
            gui_update_tab(REG.RW_GPAB_DIG_VAL1, REG.RW_GPAB_DIG_VAL1)

        elif values['_TABGROUP_'] == GUI_TABKEY_RTC:
            gui_update_tab(REG.RW_RTC_SEC_VAL, REG.RW_RTC_WDAY_VAL)

        elif values['_TABGROUP_'] == GUI_TABKEY_GEN_INFO:
            gui_update_tab(REG.R_SW_INFO, REG.R_SWITCH_VAL)
            gui_update_tab(REG.R_GPIO_M1_AN_ADC_VAL, REG.R_GPIO_M2_AN_ADC_VAL)
            gui_update_tab(REG.RW_LED_CONF, REG.RW_LED_CONF)
            gui_update_tab(REG.R_GEN_ERROR1, REG.R_GEN_ERROR2)

        elif values['_TABGROUP_'] == GUI_TABKEY_NETWORK:
            gui_update_tab(REG.RW_NET_CONF_IP1, REG.RW_NET_CONF_DHCP)

        elif values['_TABGROUP_'] == GUI_TABKEY_UART:
            gui_update_tab(REG.RW_UART_RS485_CONF1, REG.RW_UART_MIKRO2_CONF2)
            gui_update_tab_modbus_dmx512()

        elif values['_TABGROUP_'] == GUI_TABKEY_ADVANCED:
            gui_update_tab(REG.RW_EMU_CONF, REG.RW_SWITCH_CONF)
            gui_update_tab(REG.R_GPIO1_CUR, REG.R_GPIO4_CUR)

        elif values['_TABGROUP_'] == GUI_TABKEY_EXPERT:
            gui_update_tab(REG.R_DEBUG1, REG.RW_ESP32_DELAY)

    dev_con.disconnect()
    gui_window.close()


if __name__ == "__main__":
    main()
