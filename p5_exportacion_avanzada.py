import pandas as pd
import os
import re


def limpiar_nombre(s):
    if pd.isna(s):
        s = "sin_nombre"
    s = str(s)
  
    s = re.sub(r'[^A-Za-z0-9\-_.]', '_', s)
    
    return s[:80]

ventas = pd.read_csv("ventas.csv")


ventas["Total"] = pd.to_numeric(ventas["Total"], errors="coerce").fillna(0)

ventas["PrecioUnitario"] = pd.to_numeric(ventas["PrecioUnitario"], errors="coerce").fillna(0) 

productos = ventas["Producto"].fillna("sin_producto").unique()

resumen_global = []

for prod in productos:
    prod_limpio = limpiar_nombre(prod)
    carpeta = os.path.join("salidas", f"Producto={prod_limpio}")
    os.makedirs(carpeta, exist_ok=True)

    dfp = ventas[ventas["Producto"].fillna("sin_producto") == prod]

   
    archivo = os.path.join(carpeta, f"archivo_{prod_limpio}.csv")
    dfp.to_csv(archivo, index=False)


    total_prod = dfp["Total"].sum()
    registros = len(dfp)
    
    pu_prom = dfp["PrecioUnitario"].mean() if registros > 0 else 0 

    resumen_txt = (
        f"Producto: {prod}\n"
        f"Total de ventas: {total_prod}\n"
        f"Cantidad de registros: {registros}\n"
        f"Precio Unitario promedio: {pu_prom}\n"
    )

    with open(os.path.join(carpeta, "resumen.txt"), "w", encoding="utf-8") as f:
        f.write(resumen_txt)

    resumen_global.append([prod, total_prod, registros, pu_prom])


df_res_global = pd.DataFrame(resumen_global, columns=["Producto", "Total", "Registros", "PU_Promedio"])
df_res_global.to_csv("resumen_global.csv", index=False)

print("Exportacion segmentada completada. Carpetas en ./salidas/")
print("Resumen global guardado en resumen_global.csv")
#Yahir Alexis Lopez Ponce 0703200503633