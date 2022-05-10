import gpio
from bsp import board
import time
import i2c

pin = D16

def wakeUp(dataPin):   # Start signal
    print("Sleep Value (expected 1 due to PULLUP): ", gpio.get(dataPin))
    gpio.mode(dataPin, OUTPUT)
    gpio.low(dataPin) #900 micros low value 
    sleep(900, MICROS)
    print("Low value: ", gpio.get(dataPin))
    gpio.set(dataPin, HIGH)
    sleep(40, MICROS) #40 micros high value 
    gpio.mode(dataPin, INPUT)
    print("High value again: ",gpio.get(dataPin))
    sleep(5, MILLIS)

def DHT22isAwake(dataPin) -> bool:
    gpio.mode(dataPin, INPUT)
    print("Response (Expected 80 us of low signal): ", gpio.get(dataPin))
    if(gpio.get(dataPin) != 0):
        #raise Exception("Error in response signal (NOT LOW)")
        print("Error in response signal (NOT LOW)")
        return False
    sleep(80, MICROS)

    print("Response (Expected 80 us high value): ", gpio.get(dataPin))
    if(gpio.get(dataPin) != 1):
        #raise Exception("Error in response signal (NOT HIGH)")
        print("Error in response signal (NOT HIGH)")
        return False
    sleep(80, MICROS)

    return True

def getBit(dataPin) -> int: #Every received bit begin with 50 us of low value
    if(gpio.get(dataPin) != 0):
        # raise Exception("Error during receiving bit...")
        print("Error during receiving bit...")
    sleep(50, MICROS)
    sleep(28, MICROS) #if after 28 us the signal is still high -> bit 1, else bit 0
    if(gpio.get(dataPin) == 0):
        return 0
    else:
        return 1

def read(dataPin) -> (int, int, int, int, int):
    hum_int = nextByte(dataPin),
    hum_dec = nextByte(dataPin),
    temp_int = nextByte(dataPin),
    temp_dec = nextByte(dataPin),
    checksum = nextByte(dataPin)
    return(hum_int, hum_dec, temp_int, temp_dec, checksum)

def nextByte(dataPin) -> int:
    byte = 0x00
    for i in range(0,8):
        bit_i = getBit(dataPin)
        byte = byte | (bit_i << (7 - i))
    return byte

i2c_scan_buf = i2c.scan()

while True:
    wakeUp(pin)
    if(DHT22isAwake(pin)):
        print(read(pin)) #I need to convert received data, but it's just too see if I receive something
    else: 
        print("Failed...")
    sleep(2000)
