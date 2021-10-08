import threading
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
global sampleTime
sampleTime =10
def main():
    global startT
    
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    
    #SampleSize button setup
    button = digitalio.DigitalInOut(board.D23)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

    # create an analog input channel on pin 1,2
    global chan1,chan2
    chan2 = AnalogIn(mcp, MCP.P2)
    chan1 = AnalogIn(mcp, MCP.P1)
    #output headings
    print("Runtime     Temp Reading      Temp      Light Reading")
    prev_state = button.value
    global sampleTime
    #Store Start time for runtime calculations
    startT = int(round(time.time()))
    print_output()
    while(True):
        curr_state = button.value
        if(curr_state!= prev_state):
            if(sampleTime == 10):
                sampleTime = 5
            elif(sampleTime == 5):
                sampleTime = 1
            else:
                sampleTime =10
        time.sleep(0.15)

def print_output():
    """
    This function prints the output read from the sensors to the screen every sampleTime in seconds
    """
    global sampleTime,startT,chan1,chan2
    thread = threading.Timer(sampleTime, print_output)
    thread.daemon = True  
    thread.start()
    #calculate current runtime in seconds
    t = ((int(round(time.time())))-startT)
    #calculate current temp from voltage output from sensor
    temp = str(round((((chan1.voltage)-0.5)/0.01),1))
    if(t == 0):
        print("{}s              {}         {}C        {}".format(str(t),str(chan1.value),str(temp),str(chan2.value)))
    else:
        print("{}s             {}         {}C        {}".format(str(t),str(chan1.value),str(temp),str(chan2.value)))
    

if __name__ == "__main__":
    try:
        main()
            
    except Exception as e:
        print(e)
