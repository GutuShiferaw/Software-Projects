import numpy as geek
def euclid(a,b):
    if (b==0):
        return a
    else:
        return (euclid(b, geek.mod(a,b)))


num1 = int(input("please enter first number"))
num2= int(input("please enter second number"))
if num1<num2:
    n = num1
    n2 = num2
    print (euclid(n2,n))
else:
    print(euclid(num1,num2))