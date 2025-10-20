import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl

df = pd.read_csv("sales_data_sample.csv",encoding='ISO-8859-1')
varianza=0
media=0


"""columns = 'ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER',
       'SALES', 'ORDERDATE', 'STATUS', 'QTR_ID', 'MONTH_ID', 'YEAR_ID',
       'PRODUCTLINE', 'MSRP', 'PRODUCTCODE', 'CUSTOMERNAME', 'PHONE',
       'ADDRESSLINE1', 'ADDRESSLINE2', 'CITY', 'STATE', 'POSTALCODE',
       'COUNTRY', 'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME',
       'DEALSIZE'
"""

print(len(df))
#agrupamos por fecha de compra y sumamos el monto de venta
ndf=df.groupby("ORDERDATE")["PRICEEACH"].sum().to_frame().reset_index()

#definiendo la columna como un dato de fecha
ndf["ORDERDATE"] = pd.to_datetime(ndf["ORDERDATE"] )

#reescribimos la columna para incluir las fechas sin ventas
ndf =ndf.resample("D", on="ORDERDATE").sum()

#ordenamos por fecha de compra
ndf=ndf.sort_values(by="ORDERDATE").reset_index()

"""
---------------------------------------------
   MEDIA, VARIANZA Y DESVIACION ESTANDAR
---------------------------------------------
"""
media = ndf["PRICEEACH"].mean()
varianza = ndf["PRICEEACH"].var()
desv_estandar = ndf["PRICEEACH"].std()
print(f"""
--MÉTODO CLÁSICO--

Media: {media}
Varianza: {varianza}
Desviacion estandar: {desv_estandar}
""")


"""
---------------------------------------------
          REGRESIÓN LINEAL
---------------------------------------------
#  y = a + bx
"""

#calculando "a"
#tamaño de la muestra
n = len(ndf)
sum_y = ndf["PRICEEACH"].sum()
a=sum_y/n


#Calculando "b"
#ajustndo la x, suma de los valores enumerados sobre
sum_xy = 0
sum_x2 = 0

avg=sum(range(len(ndf)))/n
ndf["x_ajustada"] = list(range(len(ndf)))
ndf["x_ajustada"]-=avg
sum_xy=sum(ndf["x_ajustada"]*ndf["PRICEEACH"])
sum_x2=sum(ndf["x_ajustada"]**2)
b=sum_xy/sum_x2
#y=a+bx
ndf["Y_REG_LIN"]=a+b*ndf["x_ajustada"]

varianza=(sum(((ndf["PRICEEACH"]-ndf["Y_REG_LIN"])**2)))/(n-1)#1 grado de libertad
desv_std = varianza**(1/2)


print(f"""
--MÉTODO REGRESIÓN LINEAL--

Media: {media}
Varianza: {varianza}
Desviacion estandar: {desv_std}

""")


"""
---------------------------------------------
          REGRESIÓN POLINOMIAL
---------------------------------------------
"""

#print("valores", sum_xy, sum_x2)

#definimos los coeficientes del polinomio
coeficientes = np.polyfit(list(ndf["x_ajustada"]),list(ndf["PRICEEACH"]), 70)

#generamos la funcion polinomica 
func_pol = np.poly1d(coeficientes)


ndf["Y_REG_POL"]=func_pol(ndf["x_ajustada"])
varianza=(sum(((ndf["PRICEEACH"]-ndf["Y_REG_POL"])**2)))/(n-1)#1 grado de libertad
desv_std = varianza**(1/2)
#y_ajustado = func_pol(list(ndf["PRICEEACH"]))

print(f"""
--MÉTODO REGRESIÓN POLINOMIAL--

Media: {media}
Varianza: {varianza}
Desviacion estandar: {desv_std}
""")
   
#print(ndf)

mpl.plot(ndf["ORDERDATE"], [media for _ in range(len(ndf))], color="red")
mpl.plot(ndf["ORDERDATE"], ndf["Y_REG_LIN"], color="green")
mpl.plot(ndf["ORDERDATE"], ndf["Y_REG_POL"], color="purple")

mpl.scatter(ndf["ORDERDATE"],ndf["PRICEEACH"])

mpl.xticks(rotation=90)

#mpl.show()
"""
"""
rl=0
rp=0
for x in range(439, 439+90):
    rl+=a+b*x
    rp+= func_pol(x)
print(f"""
Calculo de un trimestre adelantado por:

Suma de la media: {media*90}
Regresión lineal: {rl}
Regresión polinomial: {rp}
""")
print(func_pol(520))
