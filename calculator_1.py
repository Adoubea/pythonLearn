#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print("Parameter Error") 

def CalcTax(salarystr):
    try:
        salary = int(salarystr)
    except:
        print("Parameter Error")
        return None

    salary -= salary * 0.165
    if salary < 0:
        print("Parameter Error")
    elif salary > 3500:
        taxincome = salary - 3500
        tax = 0.00
        if taxincome <= 1500:
            tax = taxincome * 0.03 - 0
        elif taxincome <= 4500:
            tax = taxincome * 0.1 - 105 
        elif taxincome <= 9000:
            tax = taxincome * 0.2 - 555
        elif taxincome <= 35000:
            tax = taxincome * 0.25 - 1005
        elif taxincome <= 55000:
            tax = taxincome * 0.3 - 2755
        elif taxincome <=80000:
            tax = taxincome * 0.35 - 5505
        else:
            tax = taxincome * 0.45 - 13505
        salary -= tax
    return salary
        

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        strlist = arg.split(':')        
        try:
            salary = CalcTax(strlist[1])
            print(strlist[0],end=":")
        except:
            print('Parameter Error')
        print(format(salary,'.2f'))

