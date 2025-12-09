import pandas as pd

v = pd.read_csv("ventas.csv")
c = pd.read_csv("clientes.csv")
p = pd.read_csv("productos.csv")

v["Cliente"] = v["Cliente"].astype(str)
c["Cliente"] = c["Cliente"].astype(str)


print("Haciendo merges...")
df = v.merge(c, on="Cliente", how="left")
df = df.merge(p, on="Producto", how="left")


for col in ["Total", "PrecioUnitario"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)


print("Agrupando por Cliente y Producto")
rep = df.groupby(["Cliente", "Producto"]).agg(
    Total_Sum=("Total", "sum"),
    Precio_Prom=("PrecioUnitario", "mean"),
    Cantidad_Compras=("Cantidad", "count")
).reset_index()


print("Ordenando por Total descendente")
rep = rep.sort_values(by=["Total_Sum"], ascending=[False])


rep.to_csv("reporte_multinivel.csv", index=False)
print("Reporte exportado: reporte_multinivel.csv")


print("La columna 'Ciudad' no está disponible para este cálculo.")

cliente_var = df.groupby("Cliente")["Producto"].nunique().idxmax()
print("Cliente con mayor variedad de productos:", cliente_var)

#Yahir Alexis Lopez Ponce 0703200503633