import pandas as pd

print("=== CARGANDO DATOS ===")
df = pd.read_csv("ventas.csv")

print("=== CORRIGIENDO TIPOS ===")
df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(0)

df["PrecioUnitario"] = pd.to_numeric(df["PrecioUnitario"], errors="coerce").fillna(0)
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)

print("=== CALCULANDO SUBTOTAL ===")
df["Subtotal"] = df["Cantidad"] * df["PrecioUnitario"]

df["Dif"] = abs(df["Subtotal"] - df["Total"])
df["Error_Relativo"] = df["Dif"] / df["Total"].replace(0, 1)

print("=== DETECTANDO INCONSISTENCIAS ===")
incons = df[df["Error_Relativo"] > 0.05]

print("Registros inconsistentes:", len(incons))
print("Promedio error relativo:", incons["Error_Relativo"].mean()) 

print("Producto con más inconsistencias:")
print(incons["Producto"].value_counts().head(1))

print("=== EXPORTANDO ===")
incons.to_csv("inconsistencias.csv", index=False)
print("Archivo inconsistencias.csv generado.")

#YAHIR ALEXIS LOPEZ 0703200503633