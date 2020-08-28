#Script Oficial das medidas: Segunda Lei de Newton
print('DistIR LCD v2 20181107')
import os
print('MicroPython {}; {}'.format(os.uname()[3], os.uname()[4]))
import gc
gc.collect()
print('Initial available RAM: {} bytes'.format(gc.mem_free()))
import pyb
import math
import time
import lcd160cr
gc.collect()
print('RAM after importing some modules: {} bytes'.format(gc.mem_free())) # 99120 bytes

try:
    flagLCD160CR = True
    lcd = lcd160cr.LCD160CR('XY')   # display on the right side of Pyboard, default position
except OSError:
    print('LCD160CR display not found on the right side of Pyboard')   # OSError: [Errno 19] ENODEV
    flagLCD160CR = False

if flagLCD160CR:
    print('LCD160CR display turned on')
    ti_us = time.ticks_us()
    import framebuf
    print('Time to import framebuf module: {:.3f} ms'.format(time.ticks_diff(time.ticks_us(), ti_us)*1.0e-3))
    fbufh = lcd.h-10
    fbuf = framebuf.FrameBuffer(bytearray(lcd.w * fbufh * 2), lcd.w, fbufh, framebuf.RGB565)
    gc.collect()
    print('RAM after lcd160cr and framebuf import and initialization: {} bytes'.format(gc.mem_free())) # 58608 bytes
    lcd.set_orient(lcd160cr.PORTRAIT)
    lcd.set_pen(0, 0)
    lcd.erase()
    lcd.set_spi_win(0, 0, lcd.w, fbufh)

def DistIRloop(msdelay=20):
    red_led = pyb.LED(1)
    green_led = pyb.LED(2)
    orange_led = pyb.LED(3)
    blue_led = pyb.LED(4)
    orange_led.on()
    fbuf.fill(0)
    fbuf.text('Tecle USR', 25, 20, lcd.rgb(255, 255, 0))
    lcd.show_framebuf(fbuf)
    userswitch = pyb.Switch()
    while not userswitch():
        pyb.delay(100)
    orange_led.off()
    green_led.on()
    fbuf.text('Preparando...', 10, 50, lcd.rgb(0, 255, 0))
    lcd.show_framebuf(fbuf)
    pyb.delay(1000)
    datalogfilename = '/sd/distirlog.csv'
    log = open(datalogfilename, 'a')
    log.write("t (s), d (cm)\n")
    green_led.off()
    blue_led.on()
    fbuf.text('Medindo...', 15, 80, lcd.rgb(0, 255, 255))
    lcd.show_framebuf(fbuf)
    pyb.delay(3000)
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
    fbuf.text('Fim !', 35, 110, lcd.rgb(255, 0, 0))
    lcd.show_framebuf(fbuf)

DistIRloop()
