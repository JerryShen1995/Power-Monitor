import binhex
try:
    import serial
except ImportError:
    print ("You do not have the pyserial library installed.")
    raise

class PowerMonitor:

    device = ''
    baudrate=0
    con = 0
    status = 'not hosting'
    acq = 10
    acqm = 'dynamic'
    funcm = 'optim'
    form = 'ascii_dec'
    voltage = 3300000000
    frequency = 100
    output_type = 'current'
    trigger_source = 'sw'
    trigger_delay = 0.001
    power_supply = 'on'
    temperature_mode = 'c'
    temperature = 0
    
    def helloworld(self):
        self.con.write('lcd 1 "Hello World"\n'.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                print ('done, exiting')
                break

    def htc(self):
        self.con.write('htc\n'.encode())
        self.status = 'hosting'
        while True:
            data = self.con.readline()
            if __debug__:
                if len(data)==0:
                    break
            else:
                if len(data) != 0: 
                    print ( data.decode(), end='')
                else:
                    print ('done, exiting')
                    break
    def hrc(self):
        self.con.write('hrc\n'.encode())
        self.status = 'not hosting'
        while True:
            data = self.con.readline()
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                print ('done, exiting')
                break

    def help(self):
        self.con.write('help\n'.encode())
    
        while True:
            data = self.con.readline()
        
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                print ('done, exiting')
                break
            
    def acqtime(self,x):
        x = self.__scientific(x)
        acqtime = 'acqtime '+x+'\n'
        self.con.write(acqtime.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return self.__convert(x)

    def acqmode(self,x):
        acqmode = 'acqmode '+x+'\n'
        self.con.write(acqmode.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        if x == 'dyn':
            return 'dynamic'
        elif x == 'stat':
            return 'static'
                

    def funcmode(self,x):
        funcmode = 'funcmode '+x+'\n'
        self.con.write(funcmode.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return x

    def format(self,x):                
        forma = 'format '+x+'\n'
        self.con.write(forma.encode())

        while True:
            data = self.con.readline()
            print(data)
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return x

    def volt(self,x):
        x = self.__scientific(x)
        volt = 'volt '+x+'\n'
        self.con.write(volt.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return self.__convert(x,-1)

    def freq(self,x):
        x = self.__scientific(x)
        freq = 'freq '+x+'\n'
        self.con.write(freq.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return self.__convert(x)

    def output(self,x):
        output = 'output '+x+'\n'
        self.con.write(output.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return x
        

    def trigsrc(self,x):
        trigsrc = 'trigsrc '+x+'\n'
        self.con.write(trigsrc.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return x

    def trigdelay(self,x):
        x = self.__scientific(x)
        trigdelay = 'trigdelay '+x+'\n'
        self.con.write(trigdelay.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return self.__convert(x,-1)

    def currthres(self,x):
        currthres = 'currthres '+x+'\n'
        self.con.write(currthres.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break

    def pwrend(self,x):
        pwrend = 'pwrend '+x+'\n'
        self.con.write(pwrend.encode())
        
        while True:
            data = self.con.readline()
            
            if len(data) != 0: 
                print ( data.decode(), end='')
            else:
                break
        return x

    def temp(self,x):
        self.temperature_mode = x[-1:]
        temp = 'temp '+x+'\n'
        self.con.write(temp.encode())
        temperature = 1.0
        while True:
            data = self.con.readline()
            
            if len(data) != 0:
                try:
                    temperature = float(data.decode()[-7:])
                except ValueError:
                    temperature = temperature
                print( data.decode(), end='')
            else:
                break
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
            

    def __init__(self, comPort, baudRate=3686400):
        self.device = comPort
        self.baudrate = baudRate
        self.con = serial.Serial(self.device, self.baudrate,
                        timeout=5 )
        self.open()
        
        pass

    def __bytetodec(self,x):
        result = []
        for i in x:
            result.append(i)
        return result
    
    def __hextodec(self,x,y):
        d2=x%16
        d1=(x-d2)/16
        d4=x%16
        d3=(x-d4)/16
        d=d2*256+d3*16+d4
        return d*16**(0-float(d1))

    def __hexprocess(self,x):
        result = []
        while True:
            if x[0]==240 and x[1]==243:
                x=x[9:]
            if x[0]==240 and x[1]==244:
                return result
            result.append(self.__hextodec(x[0],x[1]))
            x=x[2:]

    def open(self):
        self.htc()
        self.temperature = self.temp('degc')
        
    def read (self, voltage, samplesPerSecond, samplingTimeInSeconds, startDelayInSeconds):
        self.voltage = self.volt(voltage)
        self.frequency = self.freq(samplesPerSecond)
        self.acq = self.acqtime(samplingTimeInSeconds)
        self.trigger_delay = self.trigdelay(startDelayInSeconds)
        self.con.write('start\n'.encode())

        result = []
        temp = []
        print('starting')
        if self.form == 'ascii_dec':            
            while True:
                data = self.con.readline()
                if len(data) != 0:
                    #result.append(data.decode())
                    try:
                        result.append(float(self.__convert(data.decode()[1:8])))
                    except ValueError:
                        print(data.decode(),end='')
                else:
                    print ('done, exiting')
                    break
        else:
            while True:
                data = self.con.readline()
                if len(data) != 0:
                    try:
                        print(data.decode(),end='')
                    except UnicodeDecodeError:
                        temp = temp + self.__bytetodec(data)
                else:
                    result = self.__hexprocess(temp)
                    print(len(result))
                    print('done')
                    break
        return result
        pass

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
pm = PowerMonitor('/dev/ttyACM0')
#pm.help()
pm.form=pm.format('bin_hexa')
data = pm.read('3.3','1000','10','5')
print ('first 100 results')
print(data[:100])
#pm.status_printout()
#pm.close()
#pm.status_printout()
