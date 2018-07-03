try:
    import serial
except ImportError:
    print ("You do not have the pyserial library installed.")
    raise

class PowerMonitor:
    import logging
    log = logging.getLogger
    import numpy as np
    device = ''
    baudrate=0
    con = 0
    status = 'not hosting'
    acq = 10
    acqm = 'dynamic'
    funcm = 'optim'
    form = 'ascii_dec'
    voltage = 3.3
    frequency = 100
    output_type = 'current'
    trigger_source = 'sw'
    trigger_delay = 0.001
    power_supply = 'on'
    temperature_mode = 'c'
    temperature = 0
    reading = 0

    def psrst(self):
        self.device = ''
        self.baudrate=0
        self.status = 'not hosting'
        self.acq = 10
        self.acqm = 'dynamic'
        self.funcm = 'optim'
        self.form = 'ascii_dec'
        self.voltage = 3.3
        self.frequency = 100
        self.output_type = 'current'
        self.trigger_source = 'sw'
        self.trigger_delay = 0.001
        self.power_supply = 'on'
        self.temperature_mode = 'c'
        self.temperature = 0
        self.con.write('psrst\n'.encode())
        import time
        print('Restarting, please wait.')
        time.sleep(5)
        ports = ['COM5','/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3','/dev/ttyACM4','/dev/tty.usbmodem1121']
        for i in ports:
            try:
                self.con = serial.Serial(i, self.baudrate,
                                         timeout=5, write_timeout=3)
                device = i
                print('Current Port is '+ i)
            except:
                pass
        print('PowerShield Boosting, please wait.')
        time.sleep(10)
        self.htc()
    
    def sta(self):
        self.con.write('status\n'.encode())
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                print ('done, exiting')
                break
    
    def helloworld(self):
        self.con.write('lcd 1 "Hello World"\n'.encode())
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                print ('done, exiting')
                break
    
    def readline(self):
        result = ''
        data = self.con.read()
        result = data
        while True:
            try:
                data = self.con.read()
                if data.decode()=='\n':
                    return result
                else:
                    result = result + data
            except:
                print('Timeout!')
                return result
        return result

    def htc(self):
        self.con.write('htc\n'.encode())
        self.status = 'hosting'
        data = self.con.readline()
        while len(data) != 0:
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
                
    def hrc(self):
        self.con.write('hrc\n'.encode())
        self.status = 'not hosting'
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')

    def help(self):
        self.con.write('help\n'.encode())
        data = self.con.readline()
        while len(data) != 0: 
            print ( data.decode(), end='')
            data = self.con.readline()
            
    def acqtime(self,x):
        x = self.__scientific(x)
        acqtime = 'acqtime '+x+'\n'
        self.con.write(acqtime.encode())
        data = self.con.readline()        
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return self.__convert(x)

    def acqmode(self,x):
        acqmode = 'acqmode '+x+'\n'
        self.con.write(acqmode.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        if x == 'dyn':
            return 'dynamic'
        elif x == 'stat':
            return 'static'
                

    def funcmode(self,x):
        funcmode = 'funcmode '+x+'\n'
        self.con.write(funcmode.encode())
        data = self.con.readline()        
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return x

    def format(self,x):                
        forma = 'format '+x+'\n'
        self.con.write(forma.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return x

    def volt(self,x):
        x = self.__scientific(x)
        volt = 'volt '+x+'\n'
        self.con.write(volt.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()    
        self.logging.debug('done, exiting')
        return self.__convert(x,-1)

    def freq(self,x):
        x = self.__scientific(x)
        freq = 'freq '+x+'\n'
        self.con.write(freq.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return self.__convert(x)

    def output(self,x):
        output = 'output '+x+'\n'
        self.con.write(output.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return x
        

    def trigsrc(self,x):
        trigsrc = 'trigsrc '+x+'\n'
        self.con.write(trigsrc.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return x

    def trigdelay(self,x):
        x = self.__scientific(x)
        trigdelay = 'trigdelay '+x+'\n'
        self.con.write(trigdelay.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return self.__convert(x,-1)

    def currthres(self,x):
        currthres = 'currthres '+x+'\n'
        self.con.write(currthres.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')

    def pwrend(self,x):
        pwrend = 'pwrend '+x+'\n'
        self.con.write(pwrend.encode())
        data = self.con.readline()
        while len(data) != 0: 
            self.logging.debug( data.decode())
            data = self.con.readline()
        self.logging.debug('done, exiting')
        return x

    def temp(self,x):
        self.temperature_mode = x[-1:]
        temp = 'temp '+x+'\n'
        self.con.write(temp.encode())
        temperature = 1.0
        data = self.con.readline()
        while len(data) != 0:
            try:
                temperature = float(data.decode()[-7:])
            except ValueError:
                temperature = temperature
            print( data.decode(), end='')
            data = self.con.readline()
        return temperature
    
    def __convert(self,x,ind=0):
        try:
            #numerical numbers only
            return float(x)
        except ValueError:
            if x[-2:-1] == '+' or x[-2:-1] == '-':
                #scientific notation
                return 10**int(x[-2:])*float(x[:-2])
            if x[-3:-2] == '+' or x[-3:-2] == '-':
                #scientific notation
                return 10**int(x[-3:])*float(x[:-3])
            if x[-1:]=='u':
                return float(x[:-1])*0.000001
            if x[-1:]=='k':
                return float(x[:-1])*1000
            if ind == 1:
                #mega
                return float(x[:-1])*1000000
            else:
                #milli
                return float(x[:-1])*0.001
            
    def __scientific(self,x):
        number = self.__convert(x)
        coef = 0
        if int(number)==number:
            return str(int(number))
        elif number > 0:
            while True:
                if int(number)==number:
                    return str(int(number))+'-'+str(coef)
                else:
                    coef=coef+1
                    number = number * 10
        elif number < 0:
            while True:
                if int(number)==number:
                    return str(int(number))+'+'+str(coef)
                else:
                    coef=coef+1
                    number = number * 10
            

    def __init__(self, debug=False,baudRate=3864000):
        ports = ['COM5','/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3','/dev/ttyACM4','/dev/tty.usbmodem1121']
        for i in ports:
            try:
                self.con = serial.Serial(i, self.baudrate,
                                         timeout=5, write_timeout=3)
                device = i
                print('Current Port is '+ i)
            except:
                pass

        if debug==True:
            self.logging.basicConfig(level=self.logging.DEBUG)
        else:
            self.logging.basicConfig(level=self.logging.WARNING)
            
        self.device = device
        self.baudrate = baudRate
        self.close()
        self.open()
        
        pass
        
    counter = 1
    def __bytetodec(self,x):
        result = []
        j=0
        buff = -1
        for i in x:
            result.append(i)
            if buff >0:
                buff = buff + 1
            if buff == 6:
                print("Buffer at Percentage "+ str(i))
                buff = -1
            if i==243 and j == 240:
                print("Timestamp Number "+ str(self.counter))
                buff = 1
                self.counter = self.counter +1
            if i==241 and j == 240:
                print("Error")
            j=i
        return result
    
    def __hextodec(self,x,y):
        d2=x%16
        d1=x//16
        d4=y%16
        d3=y//16
        d=d2*256+d3*16+d4
        return d*16**(0-float(d1))
    
    leftover = []
    def __hexprocess(self,x):
        result = []
        x = self.np.append(self.leftover,x)
        while len(x)>=2:
            if x[0]==240:
                if x[1]==243:
                    #print("Timestamp Number "+ str(self.counter))
                    #print("Buffer at Percentage "+ str(x[6]))
                    self.counter = self.counter +1
                    if self.counter%1000==0:
                        print("Timestamp Number "+ str(self.counter))
                    x=x[9:]
                elif x[1]==244:
                    x=x[4:]
                    for i in x:
                        print(chr(int(i)), end='')
                    return result
                else:
                    result.append(self.__hextodec(x[0],x[1]))
                    x=x[2:]
            else:
                result.append(self.__hextodec(x[0],x[1]))
                x=x[2:]
        self.leftover = x
        return result
        
    
    def open(self):
        self.htc()
        #self.temperature = self.temp('degc')
        
    def read (self, voltage, samplesPerSecond, samplingTimeInSeconds, startDelayInSeconds):
        self.reading=0
        self.counter = 0
        self.leftover = []
        if self.__convert(samplesPerSecond)>20000 and self.form!='bin_hexa':
            print('Larger than 20000Hz, changing format')
            self.form=self.format('bin_hexa')
            self.frequency = self.freq(samplesPerSecond)
        elif self.__convert(samplesPerSecond)<=20000 and self.form!='ascii_dec':
            self.frequency = self.freq(samplesPerSecond)
            print('Smaller than 20000Hz, changing format')
            self.form=self.format('ascii_dec')
        else:
            self.frequency = self.freq(samplesPerSecond)
        
        if self.__convert(voltage)!=self.voltage:    
            self.voltage = self.volt(voltage)
        else:
            print("Voltage set.")
        
        if self.__convert(samplingTimeInSeconds)!=self.acq:
            self.acq = self.acqtime(samplingTimeInSeconds)
        else:
            print("Sampling time set.")
        
        if self.__convert(startDelayInSeconds)!=self.trigger_delay:
            self.trigger_delay = self.trigdelay(startDelayInSeconds)
        else:
            print("Trigger delay set.")

        self.con.write('start\n'.encode())
        
        result = []
        temp = []
        print('starting')
        if self.__convert(samplesPerSecond)<=20000:            
            data = self.con.readline()
            while len(data) != 0:
                try:
                    result.append(float(self.__convert(data.decode()[1:8])))
                except ValueError:
                    print(data.decode(),end='')
                data = self.con.readline()
            print ('done, exiting')
        else:
            for i in range(0,3):
                data = self.con.readline()
                print(data.decode(),end='')
            data = self.con.read(100000)
            while len(data)!=0:
                try:
                    result = self.np.append(result,self.__hexprocess(self.np.frombuffer(data,dtype=self.np.uint8)))
                except:
                    self.psrst()
                    break
                #temp=self.np.append(temp,self.__bytetodec(data))
                #try:
                #    temp=self.np.append(temp,self.np.frombuffer(data,dtype=self.np.uint8))
                #except MemoryError:
                #    break
                data = self.con.read(100000)
            #result = self.__hexprocess(temp)
        print(len(result))

        import time
        start = time.time()
        self.np.savez_compressed("result",result)
        end = time.time()
        print(end - start)
        
##        import csv
##        import gzip
##        f = gzip.open('result.csv', 'wb')
##        writer = csv.writer(f)
##        for i in result:
##            writer.writerow(result)
##        f.close()
        
##          option #2: >90sec, csv file
##        with open('result.csv', 'w') as f:
##            writer = csv.writer(f)
##            import time
##            start = time.time()
##            for i in result:
##                writer.writerow([i])
##            end = time.time()
##            print('CSV file generated.')
##            print(end - start)
        import matplotlib.pyplot as plt
        if len(result)<=100000:
            plt.plot(range(0,len(result)),result)
        else:
            print("Too many entries, printing every 100th entry")
            plt.plot(range(0,len(result[1::100])),result[1::100])
        plt.title('Result')
        plt.xlabel('Time')
        plt.ylabel(self.output_type)
        plt.savefig('foo.png')
        plt.close()
        return result
        pass
    def timestamp(self):
        return self.counter
    def close(self):
        self.hrc()
        pass

    def status_printout(self):
        print()
        print('Current Status:')
        if self.status == 'hosting':
            print('Device: ' + self.device)
            print('Baudrate: ' + str(self.baudrate))
            print('Temperature: ' + str(self.temperature) + self.temperature_mode)
            print('Format: ' + self.form)
            print('Voltage: '+str(self.voltage)+'V')
            print('Frequency: '+ str(self.frequency)+'Hz')
            print('Acquisition time: ' + str(self.acq) + 's')
            print('Acquisition mode: ' + self.acqm)
            print('Trigger delay time: ' + str(self.trigger_delay) + 's')
        else:
            print('Device is not hosting')
            
#test
pm = PowerMonitor()
#import cProfile
#cProfile.run("data = pm.read('3.3','100k','100','5')")
data = pm.read('3.3','100k','0','5')
pm.psrst()

