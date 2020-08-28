#Script Oficial das medidas: Segunda Lei de Newton
import pyb
import math
def DistIRloop(msdelay=20):
    red = pyb.LED(1)
    red.on()
    userswitch = pyb.Switch()
    initialtimems = pyb.millis()
    datalogfilename = '/sd/distirlog.csv'
    log = open(datalogfilename, 'a')
    log.write("t (s), d (cm)\n")
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
    red.off()
DistIRloop()
