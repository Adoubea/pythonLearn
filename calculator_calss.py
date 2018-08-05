#!/usr/bin/env python3

import sys
import os

def handleArgv(argvs):
    argFileDict = {}
    if len(argvs) != 7:
        print('Parameters Error!')
    else:
        for i,argv in enumerate(argvs):
            if i == 0:
                continue
            elif i == 6:
                break
            else:
                if argv == '-c':
                    if os.path.isfile(argvs[i+1]) == True:
                        argFileDict['cfg'] = argvs[i+1]
                    else:
                        print('cfg file not exists')
                        break
                elif argv == '-d':
                    if os.path.isfile(argvs[i+1]) == True:
                        argFileDict['user'] = argvs[i+1]
                    else:
                        print('user.csv not exists')
                        break
                elif argv == '-o':
                    argFileDict['out'] = argvs[i+1]
                    
    return argFileDict
                   
class Config:
    def __init__(self):
        self._cfgfile = ''
        self._datadict = {'JiShuL':0,'JiShuH':0,'YangLao':0,'YiLiao':0,'ShiYe':0,'GongShang':0,'ShengYu':0,'GongJiJin':0}

    def setCfg(self,filename):
        if os.path.isfile(filename) == True:
            self._cfgfile = filename
            self._readcfgfile()

    def _cfgData(self, datalist):
        if len(datalist) == 2:
            try:
                a = datalist[1].strip('\n').strip()
                #print(type(a), a)
                value = float(datalist[1].strip('\n').strip())
            except:
                print(self._cfgfile, "format error")
                return -1
            if self._datadict.get(datalist[0].strip()) != None:
                self._datadict[datalist[0].strip()] = value
            else:
                print(self._cfgfile, "format error")
                return -1
        else:
            print(self._cfgfile, "format error")
            return -1

    def _readcfgfile(self):
        with open(self._cfgfile, 'r') as file:
            for line in file:
                strlist = line.split('=')
                #print(strlist)
                self._cfgData(strlist)
                
    def getJiShuRange(self):
        jishu = (self._datadict['JiShuL'],self._datadict['JiShuH'])
        return jishu

    def getTaxRate(self):
        taxRate = 0
        for key,value in self._datadict.items():
            if key in ('JiShuL','JiShuH'):
                continue
            else:
                taxRate += value
        return taxRate

    def showCfg(self):
        print(self._datadict)

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
        self._sstr += '\n'

    def getStr(self):
        return self._sstr


if __name__ == '__main__':
    argfile = handleArgv(sys.argv)
    if len(argfile) == 3:
        cfg = Config()
        cfg.setCfg(argfile['cfg'])
        #cfg.showCfg()
        tax = cfg.getTaxRate()
        jishu = cfg.getJiShuRange()
        with open(argfile['out'],'a') as file:
            with open(argfile['user'],'r') as ufile:
                for data in ufile:
                    s = Salary(data)
                    s.calcSalary(jishu,tax)
                    #print(s.getStr())
                    file.write(s.getStr())
    
