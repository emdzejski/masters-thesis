import numpy as np


# def sigmoid(x,a=-0.56,z=90,c=-3.5,d=0.5):
#     y = a/( 1 + np.exp( (x-z)/c ) ) + d
#     return y

def sigmoid(x,a=1,z=220,c=1,d=1):
    y = a/( 1 + np.exp( (x-z)/c ) ) + d
    return y

def DoseResponse(x, a =1, b = 1, z=220,d=1): #dose response sigmoid
    y = a + (b-a)/(1+np.power(10, (z-x)*d ))
    return y

def hill(x,a=0.7,b=0.01,z=90,d=15): #hill function
    y= a + (b-a)*np.power(x,d) / (np.power(z,d) + np.power(x,d))
    return y

def logDoseResponse(x,a=1,b=1,z=90,d=1): #logistic dose response
    y = b + (a-b)/(1 + np.power(x/z,d))
    return y

def logistic5params(x,a=1,b=1,z=90,d=1,e=1): #logistic with 5 params
    y = a + (b-a)/ np.power( (1 + np.power(z/x,d)), e )
    return y

def atan(x, a=20, z = 5, c=1):
    y = -np.arctan(x/a - z ) + c
    return y

def tanh(x, a=10,z=90,c=0.5):
   y = -np.tanh(x/a - z) + c 
   return y