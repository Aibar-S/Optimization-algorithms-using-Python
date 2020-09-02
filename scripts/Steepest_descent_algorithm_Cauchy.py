import sympy as sp
from sympy.plotting import plot
from sympy import simplify, solve, symbols
import math as math
import numpy as np
from math import exp
from math import sin
from math import sqrt

#Использую SymPy чтобы пользователь мог заносить функцию при запросе
#макс размерность задачи = 10
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')

lambdaAK = sp.Symbol('lambdaAK')
print("Примечание:\n 1) Можно использовать только 'x1','x2','x3,...,x10 как переменную/неизвестную \n 2) все действия (+, -, /, *) такие же как и в обычном Python коде \n 3) степень обозначается как ** \n 4) exp(), sin(x), ln(x), sqrt(), Abs() \n 5) вместо pi использовать число 3.14 (Например, если надо ввести pi/4, то вводим 0.785)")
f_x = input('Теперь введите функцию сюда и нажмите "Enter": ')
f_x = sp.sympify(f_x)

#Ввод данных
number = int(input('Введите размерность задачи: '))
aa0 = list(map(float, input("введите координаты начальной точки через пробел): ").split()))
eps_x_all = float(input("введите погрешность по аргументу eps_x: "))
eps_y_all = float(input("введите погрешность по функции eps_y: "))

#Присваиваю изначальное значение чтобы loop заработал для 0 итерации
eps_x_stop_all = 100.0
eps_y_stop_all = 100.0

eps_x=0.000001
eps_y=0.000001

#создаю ключи
list_x=[x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]
keys=[]
for i in range(0,number):
    keys.append(list_x[i])

#Вычисление производной для всех аргументов
proizv=[]
for i in keys:
    proizv.append(sp.Derivative(f_x, i).doit())

#начало loopa
k=0
while ((eps_y_stop_all > eps_y_all) or (eps_x_stop_all > eps_x_all)):
    aa=[]
    for i in range(0,number):
        aa.append(aa0[i])
    
    vector_x0=np.array(aa)
    
    #создаю dictionary чтобы вставить внутрь производной
    dict2={}
    dict2=dict(zip(keys,aa))
    
    #высчитываем значение функции    
    fx_x=f_x.evalf(subs=dict2)
    
    #Подставляем и решаем производную для всех аргументов
    solution=[]
    for i in range(0,number):
        solution.append(proizv[i].evalf(subs=dict2))
    
    #вычисляем вектор fx    
    vector_fx=np.array(solution)
    d0=-vector_fx
    
    vector_f_lambda=vector_x0 + lambdaAK*d0
    
    #создаю еще один dictionary чтобы вставить в уравнение с лямбдой
    dict3={}
    dict3=dict(zip(keys,vector_f_lambda))    
    solution_fx=simplify(f_x.subs(dict3))

    #Добавил так же вычисление lambda тем методом который описан в методичке чтобы сравнить с результатами минимизации функции
    proizv_lambda=sp.Derivative(solution_fx, lambdaAK).doit()
    proizv_lambda_solve=solve(proizv_lambda)
    
    #Решение для нахождения значения Lambda представлено ниже
    #Следующие параметры введены для инициализации поиска решения для Lambda
    iter=0
    #дельту сделал равной eps_x
    delta=eps_x
    #начальный интервал ввел как -10 и 10
    a=-1000
    b=1000
    eps_x_stop = 100.0
    eps_y_stop = 100.0
    while ((eps_y_stop > eps_y) or (eps_x_stop > eps_x)):
        a0 = a
        b0 = b
        x_sr_0 = (a0 + b0) / 2
        x_1 = x_sr_0 - delta/2
        x_2 = x_sr_0 + delta/2
        
        solution1=solution_fx.evalf(subs={lambdaAK:x_1})
        solution2=solution_fx.evalf(subs={lambdaAK:x_2})
        
        if solution1 > solution2:
            a=x_1
            b=b0
        else:
            a=a0
            b=x_2
        
        x_sr_1 = (a + b)/2
        
        eps_y_stop = abs( solution_fx.evalf(subs={lambdaAK:x_sr_0}) - solution_fx.evalf(subs={lambdaAK:x_sr_1}) )
        eps_x_stop = abs((a0 - b0)/2)
        fx_x_sr = solution_fx.evalf(subs={lambdaAK:x_sr_0})
    vector_x1=vector_x0 + x_sr_0*d0
    
    for i in range(0,number):
        aa0[i]=vector_x1[i]
    
    #обновляю dictionary чтобы вставить внутрь производной
    dict2={}
    dict2=dict(zip(keys,aa0))
    solution=[]
    for i in range(0,number):
        solution.append(proizv[i].evalf(subs=dict2))
    
    vector_fx2=np.array(solution)
    d1=-vector_fx2
    d0d1=np.dot(d0,d1)
    
    vector_diff=vector_x1 - vector_x0
    
    eps_x_stop_all = math.sqrt((vector_diff*vector_diff).sum())
    eps_y_stop_all = math.sqrt((vector_fx2*vector_fx2).sum())
    
    
    d0d1 = round(d0d1, 100)
    
    print("iteration",k)
    print("xk",vector_x0)
    print("fx_k",fx_x)
    print("vector_fx_k",vector_fx)
    print("dk",d0)
    print("lambda",x_sr_0)
    print("lambda2",proizv_lambda_solve[0])
    print("eps_x",eps_x_stop_all)
    print("eps_y",eps_y_stop_all)
    
    k=k+1
 
fx_x=f_x.evalf(subs=dict2)
print("iteration",k)
print("xk",vector_x1)
print("fx_k",fx_x)

length_eps_x=len(str(eps_x_all).split('.')[1])
length_eps_y=len(str(eps_y_all).split('.')[1])
fx_x = round(fx_x, length_eps_y)
vectorr=np.around(vector_x1.astype(np.double), length_eps_x)

print("\nЗначение аргумента",vectorr)
print("Значение функции",fx_x)