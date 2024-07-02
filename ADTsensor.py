import spidev
import time
from statistics import mean

def read_status_register(spi):
    # Read the status register (0x00)
    return spi.xfer2([0x00, 0x00])[1]

def reset_serial_interface(spi):
    spi.xfer2([0xFF] * 32)

def read_register(spi, register):
    # Send the read command (0x40) OR'd with the register address
    return spi.xfer2([0x40 | register, 0x00])[1]

def write_register(spi, register, value):
    # Send the write command (0x00) OR'd with the register address
    # followed by the value to write to the register
    spi.xfer2([0x00 | register, value])

def initialize_device(spi):
    # Send 32 consecutive '1's to reset the device
    spi.xfer2([0xFF] * 32)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 400000
spi.mode = 0b11

initialize_device(spi)

times_to_run = 15
temperatures = []

try:
    # Read the current configuration register value
    current_config = read_register(spi, 0x01)
    print(f"Current Configuration: {current_config:08b}")

    # Set Bit 7 to 1 to change resolution to 16 bits
    write_register(spi, 0x01, 0b10010000)

    # Verify the new configuration
    updated_config = read_register(spi, 0x01)
    print(f"Updated Configuration: {updated_config:08b}")

    if updated_config != current_config:
        print("Configuration register did not update correctly.")

    while True: #len(temperatures) <= (times_to_run - 1):
        # Check the status register for errors or shutdown mode
        status = read_status_register(spi)
        if status != 0:
            print(f"Status Register: {status:08b}")
            
        if status & 0x80:  # Check for communication error
            print("SPI communication error.")
            
        if status & 0x40:  # Check if the sensor is in shutdown mode
            print("Sensor is in shutdown mode.")

        READ_TEMPERATURE_CMD = [0x50, 0x00]
        response = spi.xfer2(READ_TEMPERATURE_CMD + [0x00, 0x00])
        raw_temperature = (response[1] << 8) | response[2]

        if raw_temperature & 0x8000:
            temperature = ((raw_temperature ^ 0xFFFF) + 1) * -0.0078
        else:
            temperature = raw_temperature * 0.0078

        if temperature != 0.00:
            print(f"Temperature: {temperature:.2f}C")
            #temperatures.append(temperature)
        else:
            print("0C Detected")

        #reset_serial_interface(spi)
        time.sleep(1)
finally:
    #temperature_average = mean(temperatures)
    #print(f"Temperature: {temperature_average:.2f}C")
    spi.close()