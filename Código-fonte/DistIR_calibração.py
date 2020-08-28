## 25/07/2018 Script oficial das medidas em laboratório
import pyb
import math
def DistIRloopMeanStdDevCorr(numADCreadings=50, msdelay=20):
    adc = pyb.ADC('X4')
    samplesADC = [0.0]*numADCreadings; meanADC = 0.0
    samplesDist = [0.0]*numADCreadings; meanDist = 0.0
    i = 0
    t1=pyb.micros()
    while (i < numADCreadings):
        adcint = adc.read()
        samplesADC[i] = adcint
        meanADC += adcint
        adcv = (adcint*3.3/4095)
        dcm =  ((9.89703)/(adcv - 0.0189332))**(1/0.734319) #(A)/(y - y0))^(1/4.20) ((-0.1)/(adcv - 19.4))**(1/4.20)
        samplesDist[i] = dcm
        meanDist += dcm
        i += 1
        pyb.delay(msdelay)
    t2=pyb.micros()
    print("\n%d ADC readings done after %u us." % (numADCreadings, t2-t1))
    print("Mean time for each ADC reading = %15.13f us, with delay of %d ms" % ((t2-t1)/numADCreadings,msdelay))
    meanADC /= numADCreadings
    varianceADC = 0.0
    for adcint in samplesADC:
        varianceADC += (adcint - meanADC)**2
    varianceADC /= (numADCreadings - 1)
    stddevADC = math.sqrt(varianceADC)
    meanDist /= numADCreadings
    varianceDist = 0.0
    for dcm in samplesDist:
        varianceDist += (dcm - meanDist)**2
    varianceDist /= (numADCreadings - 1)
    stddevDist = math.sqrt(varianceDist)
#    print("%u ADC readings :\n%s" %(numADCreadings, str(samplesADC)))
    print("Mean of ADC readings (0-4095) = %15.13f" % meanADC)
    print("Mean of ADC readings (0-3300 mV) = %15.13f" % (meanADC*3300/4095))
    print("Standard deviation of ADC readings (0-4095) = %15.13f" % stddevADC)
    print("Standard deviation of ADC readings (0-3300 mV) = %15.13f" % (stddevADC*3300/4095))
#    print("%u distance readings :\n%s" %(numADCreadings, str(samplesDist)))
    print("Mean of distance readings (0-150 cm) = %15.13f" % meanDist)
    print("Standard deviation of distance readings (cm) = %15.13f" % stddevDist)
#   Remove spikes from the ADC readings, above (mean + 1.5 times the standard deviation) :
    print("Removing ADC spikes from samples...")
    numADCreadingsCorr = numADCreadings
    cutoffvalueADC = meanADC + 1.5*stddevADC
    meanADC = 0.0; meanDist = 0.0
    i = 0
    while (i < numADCreadingsCorr):
        if samplesADC[i] > cutoffvalueADC:
            del samplesADC[i]
            del samplesDist[i]
            numADCreadingsCorr -= 1
        else:
            i += 1
    i = 0
    while (i < numADCreadingsCorr):
        meanADC += samplesADC[i]
        meanDist += samplesDist[i]
        i += 1
    meanADC /= numADCreadingsCorr
    varianceADC = 0.0
    for adcint in samplesADC:
        varianceADC += (adcint - meanADC)**2
    varianceADC /= (numADCreadingsCorr - 1)
    stddevADC = math.sqrt(varianceADC)
    meanDist /= numADCreadingsCorr
    varianceDist = 0.0
    for dcm in samplesDist:
        varianceDist += (dcm - meanDist)**2
    varianceDist /= (numADCreadingsCorr - 1)
    stddevDist = math.sqrt(varianceDist)
#    print("%u ADC readings after removing spikes :\n%s" %(numADCreadingsCorr, str(samplesADC)))
    print("Mean of ADC readings (0-4095) = %15.13f" % meanADC)
    print("Mean of ADC readings (0-3300 mV) = %15.13f" % (meanADC*3300/4095))
    print("Standard deviation of ADC readings (0-4095) = %15.13f" % stddevADC)
    print("Standard deviation of ADC readings (0-3300 mV) = %15.13f" % (math.sqrt(varianceADC)*3300/4095))
#    print("%u distance readings after removing spikes :\n%s" %(numADCreadingsCorr, str(samplesDist)))
    print("Mean of distance readings (0-150 cm) = %15.13f" % meanDist)
    print("Standard deviation of distance readings (cm) = %15.13f" % stddevDist)
while True:
    DistIRloopMeanStdDevCorr(50,150)
