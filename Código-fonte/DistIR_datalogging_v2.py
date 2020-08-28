#Script Oficial das medidas: Segunda Lei de Newton
import pyb
import math
def DistIRloop(msdelay=20):
    red_led = pyb.LED(1)
    green_led = pyb.LED(2)
    orange_led = pyb.LED(3)
    blue_led = pyb.LED(4)
    orange_led.on()
    userswitch = pyb.Switch()
    while not userswitch():
        pyb.delay(100)
    orange_led.off()
    green_led.on()
    pyb.delay(1000)
    datalogfilename = '/sd/distirlog.csv'
    log = open(datalogfilename, 'a')
    log.write("t (s), d (cm)\n")
    green_led.off()
    blue_led.on()
    initialtimems = pyb.millis()
    while not userswitch():
        adcint = pyb.ADC(pyb.Pin('X4')).read()
        times = ((pyb.millis()) - initialtimems)/1000
        adcv = (adcint*3.3/4095)
        dcm = (9.89703/(adcv - 0.0189332))**(1/0.734319) # (A/(v-v0))^(1/B)
        print("%f s, %f cm" % (times, dcm))
        log.write("%f, %f\n" % (times, dcm))
        pyb.delay(msdelay)
    log.close()
    pyb.sync()
    blue_led.off()
    red_led.on()
DistIRloop()
