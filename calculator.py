#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Parameter Error") 
salary = 0.00
try:
    salary = int(sys.argv[1])
except:
    print("Parameter Error")

if __name__ == '__main__':
    if salary < 0:
        print("Parameter Error")
    elif salary <= 3500:
        print(format(0,".2f"))
    else:
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
        print(format(tax,".2f"))
        
    
