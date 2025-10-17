import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl

df = pd.read_csv("sales_data_sample.csv",encoding='ISO-8859-1')

"""columns = 'ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER',
       'SALES', 'ORDERDATE', 'STATUS', 'QTR_ID', 'MONTH_ID', 'YEAR_ID',
       'PRODUCTLINE', 'MSRP', 'PRODUCTCODE', 'CUSTOMERNAME', 'PHONE',
       'ADDRESSLINE1', 'ADDRESSLINE2', 'CITY', 'STATE', 'POSTALCODE',
       'COUNTRY', 'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME',
       'DEALSIZE'
"""
#df["ORDERDATE"]=pd.to_datetime(["ORDERDATE"])
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"] )
ndf=df.groupby("ORDERDATE")["PRICEEACH"].sum().to_frame().reset_index()
ndf=ndf.sort_values(by="ORDERDATE")

grado_del_polinomio = len(ndf)-1

coeficientes = np.polyfit(list(ndf.index),list(ndf["PRICEEACH"]), 5)

func_pol = np.poly1d(coeficientes)

y_ajustado = func_pol(list(ndf["PRICEEACH"]))

print(y_ajustado)

print(ndf)
#print(coeficientes)

#print(df["PRICEEACH"])

mpl.plot(ndf["ORDERDATE"], y_ajustado, color="red")

mpl.scatter(ndf["ORDERDATE"],ndf["PRICEEACH"])

mpl.xticks(rotation=90)

mpl.show()
"""
"""
