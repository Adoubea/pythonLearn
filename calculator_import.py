#!/usr/bin/env python3
import getopt,sys,os,configparser
from datetime import datetime
from multiprocessing import Process, Queue

def Usage():
    print('Usage: ./calculator.py -C cityname -c configfile -d userdata -o resultdata')
def handlecfg():
    try:
        opts,args = getopt.getopt(sys.argv[1:],'-h-C:-c:-d:-o:',['help'])
    except:
        Usage()
        sys.exit(-1)

    argDict = {}
    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            Usage()
            sys.exit(1)
        elif opt_name in ('-C'):
            argDict['cityname'] = opt_value.upper()
        elif opt_name in ('-c'):
            if os.path.isfile(opt_value):
                argDict['cfgfile'] = opt_value
            else:
                Usage()
                sys.exit(1)
        elif opt_name in ('-d'):
            if os.path.isfile(opt_value):
                argDict['userdata'] = opt_value
            else:
                Usage()
                sys.exit(1)
        elif opt_name in ('-o'):
            argDict['rdata'] = opt_value
            
    if argDict.get('cityname') == None:
        argDict['cityname'] = 'DEFAULT'
    if argDict.get('cfgfile') == None:
        Usage()
        sys.exit(1)
    if argDict.get('userdata') == None:
        Usage()
        sys.exit(1)
    if argDict.get('rdata') == None:
        Usage()
        sys.exit(1)

    return argDict

class Salary:
    def __init__(self,data):
        self._salaryInfo = []
        self._sstr = ''
        dlist = data.split(',')
        if len(dlist) == 2:
            try:
                val = 0
                val = int(dlist[1].strip('\n').strip())
            except:
                print('user.csv format error')
        
            self._wkNo = dlist[0].strip()
            self._salary = val
            self._salaryInfo.append(dlist[0].strip())
            self._salaryInfo.append(val)
            self._sstr += dlist[0].strip()
            self._sstr += ','
            self._sstr += str(val)
            self._sstr += ','
            

    def _calcTaxincome(self,salary, shebao):
        a = salary - shebao - 3500
        b = 0
        if a <= 0:
            b = 0
        elif a <= 1500:
            b = a * 0.03
        elif a <= 4500:
            b = a * 0.1 - 105
        elif a <= 9000:
            b = a * 0.2 - 555
        elif a <= 35000:
            b = a * 0.25 - 1005
        elif a <= 55000:
            b = a * 0.3 - 2755
        elif a <= 80000:
            b = a * 0.35 - 5505
        else:
            b = a * 0.45 - 13505
        return b

    def calcSalary(self,jishu,tax):
        if self._salary <= jishu[0]:
            self._salaryInfo.append(jishu[0]*tax)
        elif self._salary >= jishu[1]:
            self._salaryInfo.append(jishu[1]*tax)
        else:
            self._salaryInfo.append(self._salaryInfo[1]*tax)
        self._sstr += format(self._salaryInfo[2],'.2f')
        taxincome = self._calcTaxincome(self._salaryInfo[1],self._salaryInfo[2])
        self._salaryInfo.append(taxincome)
        self._sstr += ','
        self._sstr += format(taxincome,'.2f')
        self._sstr += ','
        self._salaryInfo.append(self._salaryInfo[1]-self._salaryInfo[2]-taxincome)
        self._sstr += format(self._salaryInfo[4],'.2f')
        #self._sstr += '\n'

    def getStr(self):
        return self._sstr

queue1 = Queue()
queue2 = Queue()

def readUserData(q,userfile):
    with open(userfile, 'r') as file:
        datalist = file.readlines()
        q.put('\t'.join(datalist))
            

def calcData(q1,q2,jishu,tax):
    strlist = q1.get()
    datalist = strlist.split('\t')
    reslist = []
    for data in datalist:
        #print('process2: ' + data)
        s = Salary(data)
        s.calcSalary(jishu,tax)
        reslist.append(s.getStr())
    q2.put('\t'.join(reslist))

def writefile(q,outfile):
    with open(outfile, 'a') as file:
        #while not q.empty():
        datalist = q.get()
        #print('process3: ' + datalist)
        strlist = datalist.split('\t')
        for ostr in strlist:
            ostr += ','+datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%s')
            ostr +='\n'
            file.write(ostr)

if __name__ == '__main__':
    argfile = handlecfg()
    if len(argfile) == 4:
        try:
            cfg = configparser.ConfigParser()
            cfg.read(argfile['cfgfile'])
            jishu = (cfg.getfloat(argfile['cityname'],'JiShuL'),cfg.getfloat(argfile['cityname'],'JiShuH'))
            tax = 0
            for key,val in cfg.items(argfile['cityname']):
                if key.upper() in ('JISHUL','JISHUH'):
                    continue
                tax += float(val.strip())
        except:
            print('parser error')
            sys.exit(1)
        p1 = Process(target=readUserData,args=(queue1,argfile['userdata']))
        p2 = Process(target=calcData,args=(queue1, queue2, jishu, tax))
        p3 = Process(target=writefile, args=(queue2,argfile['rdata']))

        p1.start()
        p2.start()
        p3.start()

        p3.join()
        p2.join()
        p1.join()
