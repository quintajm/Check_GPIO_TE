'''
Program: read_gpio.py
Author: Nathan Kidd
Purpose: This program reads all the GPIOS of the pi in order to help with troubleshooting.
'''
import os
os.system("sudo apt install raspi-gpio")
os.system("sudo pip3 install paho-mqtt") #install mqtt library
import paho.mqtt.client as mqtt
from subprocess import check_output
#from datetime import datetime
import datetime
from datetime import date

print("NOTE: make sure 'raspi-gpio' is installed from the CLI. You can use the following command to install it:\n\napt install raspi-gpio")

### LUS03 board ###
I2C_f3, I2C_r3 = "__________\nCSI1 and DSI1 I2C Bus:", [0,1]
CS_dig_f3, CS_dig_r3 = "__________\nCS1 Control Or Digital Output:", [2,3,4,5]
dig1_f3, dig1_r3 = "__________\nDigital Out:", [6,7]
ethSPI_f3, ethSPI_r3 = "__________\nEthernet SPI Interface 0:", [8,9,10,11]
dig2_f3, dig2_r3 = "__________\nDigital Out:", [12,13]
RS232_f3, RS232_r3 = "__________\nRS232 Serial Out:", [14,15]
cellCon_f3, cellCon_r3 = "__________\nCell Modem Control:", [16,17]
microSPI_f3, microSPI_r3 = "__________\nAUX Micro SPI Interface 1:", [18,19,20,21]
ethCon_f3, ethCon_r3 = "__________\nEthernet Control:", [22,23]
microCon_f3, microCon_r3 = "__________\nAUX Micro Control:", [24,25]
USBcon_f3, USBcon_r3 = "__________\nUSB Configure [26], From AUX - Data Available[27]:", [26,27]
camera_f3, camera_r3 = "__________\nCSI0 Camera Controls:", [28,29,30,31]
cellSPI_f3, cellSPI_r3 = "__________\nCell Modem Serial Interface:", [32,33]
digIn1_f3, digIn1_r3 = "__________\nDigital in:", [34,35]
digIn2_f3, digIn2_r3 = "__________\nDigital in:", [36,37]
digIn3_f3, digIn3_r3 = "__________\nDigital in:", [38,39]
digIn4_f3, digIn4_r3 = "__________\nDigital in:", [40,41]
battery_f3, battery_r3 = "__________\nBattery installed:", [42]
audio_f3, audio_r3 = "__________\nAudio Controls:", [43,44,45]

### LUSO7 board ###
AUX_format7, AUX_range7 = "__________\nAUX I2C Bus:", [0,1]
audioData_format7, audioData_range7 = "__________\nAudio SDA1 and SCL1", [2,3]
digital_format7, digital_range7 = "__________\nDigital Inputs (1-2):", [4,5]
term1_format7, term1_range7 = "___________\nTERMINATED GPIOS:", [6,7]
ethernet_format7, ethernet_range7 = "__________\nEthernet SPI Interface:", [8,9,10,11]
PIC12_format7, PIC12_range7 = "__________\nPIC12 OUT & RPCM:", [12,13]
term2_format7, term2_range7 = "__________\nTERMINATED GPIOS:", [14,15]
cell_format7, cell_range7 = "__________\nCell Modem Control:", [16,17]
microSPI_format7, microSPI_range7 = "__________\nAux Micro SPI Interface 1:", [18,19,20,21]
ethControl_format7, ethControl_range7 = "__________\nEthernet Control:", [22,23]
microControl_format7, microControl_range7 = "__________\nAUX Micro Control:", [24,25]
term3_format7, term3_range7 = "__________\nTERMINATED GPIO:", [26]
USBconfig_format7, USBconfig_range7 = "__________\nUSB Configure From AUX - Data Available:", [27]
modem_format7, modem_range7 = "__________\nCell Modem PCM CLK, PCM FS, PCM DIN, PCM DOUT:", [28,29,30,31]
modemSerial_format7, modemSerial_range7 = "__________\nCell Modem Serial Interface:", [32,33]
error_format7, error_range7 = "__________\nState of Network, Cellular, and Error state:", [34,35,36,37]
term4_format7, term4_range7 = "___________\nTERMINATED GPIOS:", [38,39,40,41]
battery_format7, battery_range7 = "__________\nBattery Installed:", [42]
audio_format7, audio_range7 = "__________\nAudio Controls:", [43,44,45]
#_______________________________________
### GET OUTPUT FROM 'raspi-gpio get' ###
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def get_output():
    return check_output(["raspi-gpio","get"])
    #print(output.decode('utf-8').split('\n'))
#_______________________________________
############# PARSE OUTPUT #############
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def parse(output):
    #print(output)
    split = output.decode('utf-8').split('\n')
    del split[-1]
    sub = []
    #print(split)
    for line in split:
        #print(line)
        if 'BANK' in line:
            #print(line)
            split.remove(line)
            continue
    text = split
    return text
#_______________________________________
#########Transfer data over mqtt########
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def transferData(output_name):
    # This is the Publisher
    with open(output_name,'r') as file:
        message = file.readlines()
        
    client = mqtt.Client()
    client.connect("10.0.0.211",1883,60) #10.0.0.211
    client.publish("transferData", f"{message}");
    client.disconnect();
#_______________________________________
########## SAVE RAW OUTPUT #############
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def save_output(text,serial_number):
    
    output_name = f"{serial_number}_output.txt"
    now = datetime.datetime.now()
    text.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    text.append(serial_number)
    with open(output_name, "w") as f:
        f.write('\n'.join(text)+'\n')
    print(f"GPIO states saved to {output_name}")
    #Transfer data from output_file over mqtt to Pi
    transferData(output_name)
#_______________________________________
########## PRINT THE DATA ##############
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    

def data_print(text, data_format, data_range):
    print(data_format)
    for i in data_range:
        print(text[i])


########################################        
############### MAIN ###################
########################################
def main():
    print("")
    output = get_output()
    text = parse(output)
    choice = input("\nIs this an LUS03 or LUS07 board? [input 3 or 7]: ")
    serial_number = input("\Whats thew serial number on the board? ")
    save_output(text,serial_number)
    
    if choice == '3':
        data_print(text, I2C_f3, I2C_r3)
        data_print(text, CS_dig_f3, CS_dig_r3)
        data_print(text, dig1_f3, dig1_r3)
        data_print(text, ethSPI_f3, ethSPI_r3)
        data_print(text, RS232_f3, RS232_r3)
        data_print(text, cellCon_f3, cellCon_r3)
        data_print(text, microSPI_f3, microSPI_r3)
        data_print(text, ethCon_f3, ethCon_r3)
        data_print(text, microCon_f3, microCon_r3)
        data_print(text, USBcon_f3, USBcon_r3)
        data_print(text, camera_f3, camera_r3)
        data_print(text, cellSPI_f3, cellSPI_r3)
        data_print(text, digIn1_f3, digIn1_r3)
        data_print(text, digIn2_f3, digIn2_r3)
        data_print(text, digIn3_f3, digIn3_r3)
        data_print(text, digIn4_f3, digIn4_r3)
        data_print(text, battery_f3, battery_r3 )
        data_print(text, audio_f3, audio_r3)
        
    if choice == '7':
        data_print(text, AUX_format7, AUX_range7)
        data_print(text, audioData_format7, audioData_range7)
        data_print(text, digital_format7, digital_range7)
        data_print(text, term1_format7, term1_range7)
        data_print(text, ethernet_format7, ethernet_range7)
        data_print(text, PIC12_format7, PIC12_range7)
        data_print(text, term2_format7, term2_range7)
        data_print(text, cell_format7, cell_range7)
        data_print(text, microSPI_format7, microSPI_range7)
        data_print(text, ethControl_format7, ethControl_range7)
        data_print(text, microControl_format7, microControl_range7)
        data_print(text, term3_format7, term3_range7)
        data_print(text, USBconfig_format7, USBconfig_range7)
        data_print(text, modem_format7, modem_range7)
        data_print(text, modemSerial_format7, modemSerial_range7)
        data_print(text, error_format7, error_range7)
        data_print(text, term4_format7, term4_range7)
        data_print(text, battery_format7, battery_range7)
        data_print(text, audio_format7, audio_range7)



if __name__ == "__main__":
    main()