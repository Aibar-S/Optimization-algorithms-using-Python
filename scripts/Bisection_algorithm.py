import sympy as sp
from sympy.plotting import plot
import math as math
from math import exp
from math import sin
from math import sqrt

#Использую SymPy чтобы пользователь мог заносить функцию при запросе
x = sp.Symbol('x')
print("Примечание:\n 1) Можно использовать только 'x' как переменную/неизвестную \n 2) все действия (+, -, /, *) такие же как и в обычном Python коде \n 3) степень обозначается как ** \n 4) exp(), sin(x), ln(x), sqrt(), Abs() \n 5) вместо pi использовать число 3.14 (Например, если надо ввести pi/4, то вводим 0.785)")
f_x = input('Теперь введите функцию сюда и нажмите "Enter": ')
f_x = sp.sympify(f_x)

#Ввод данных
a,b = map(float, input("введите начальный интервал (начало интервала и конец интервала через пробел): ").split())
eps_x = float(input("введите погрешность по аргументу eps_x: "))
eps_y = float(input("введите погрешность по функции eps_y: "))
delta = float(input("введите дельту (пара координат будет разнесена на эту величину; значение должно находиться внутри [0;eps_x]): "))

while delta < 0 or delta > eps_x:
    print("дельта не может быть < 0 или >", eps_x)
    delta = float(input("введите дельту заново: "))

#Присваиваю изначальнве значение чтобы loop заработал для 0 итерации
eps_x_stop = 100.0
eps_y_stop = 100.0

#отображаю график в пределах изначального интервала
plot(f_x, (x, a, b))

#Основное решеное представлено ниже
iter=0
while ((eps_y_stop > eps_y) or (eps_x_stop > eps_x)):
    a0 = a
    b0 = b
    x_sr_0 = (a0 + b0) / 2
    x1 = x_sr_0 - delta/2
    x2 = x_sr_0 + delta/2
    
    solution1=f_x.evalf(subs={x:x1})
    solution2=f_x.evalf(subs={x:x2})
    
    if solution1 > solution2:
        a=x1
        b=b0
    else:
        a=a0
        b=x2
    
    x_sr_1 = (a + b)/2
    fx_x_sr = f_x.evalf(subs={x:x_sr_0})
    eps_y_stop = abs( fx_x_sr - f_x.evalf(subs={x:x_sr_1}) )
    eps_x_stop = abs((a0 - b0)/2)
    #Вывожу на экран все промежуточные значения и решения
    print("итерация", iter)
    print("a_k=",a0,"b_k=",b0)
    print("x_sr_k=",x_sr_0)
    print("f(x_sr_k)=",fx_x_sr)
    print("x1_k=",x1,"x2_k=",x2)
    print("f(x1_k)=",solution1,"f(x2_k)=",solution2)
    print("точность по аргументу", eps_x_stop)
    print("точность по функции", eps_y_stop)
    iter=iter+1

#Округляю аргумент до точности eps_x и функцию до точности eps_y
length_eps_x=len(str(eps_x).split('.')[1])
length_eps_y=len(str(eps_y).split('.')[1])
x_sr_0_answer = round(x_sr_0, length_eps_x)
fx_x_sr = round(fx_x_sr, length_eps_x)
#Печатаю финальное решение
print("Финальное Решение:")
print("Значение аргумента:",x_sr_0_answer)
print("Значение функции:",fx_x_sr)
print("Количество итераций:",iter-1)
print("Количество вычислений функции (внутри каждой итерации функциф рассчитывается 4 раза):",(iter-1)*4)

#Этот loop для того чтобы вычислить x(k+2) для вычисления коэффициента сходимости
x_sr_k=x_sr_0
x_sr_k1=x_sr_1
a0 = a
b0 = b
x_sr_0 = (a0 + b0) / 2
x1 = x_sr_0 - delta/2
x2 = x_sr_0 + delta/2

solution1=f_x.evalf(subs={x:x1})
solution2=f_x.evalf(subs={x:x2})

if solution1 > solution2:
    a=x1
    b=b0
else:
    a=a0
    b=x2

x_sr_1 = (a + b)/2
x_sr_k2=x_sr_1
coeff_shodimosti=abs(x_sr_k1-x_sr_k2) / abs(x_sr_k-x_sr_k1)
print("коэффициент сходимости:",coeff_shodimosti)