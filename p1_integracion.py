import pandas as pd

print("=== CARGANDO ARCHIVOS ===")
ventas = pd.read_csv("ventas.csv")
clientes = pd.read_csv("clientes.csv")
productos = pd.read_csv("productos.csv")


v = ventas.copy()
c = clientes.copy()
p = productos.copy()

print("\n=== VALIDANDO PRODUCTOS ===")
antes = len(v)
v = v[v["Producto"].isin(p["Producto"])]
rech_prod = antes - len(v)
print("Filas rechazadas por producto:", rech_prod)

print("\n=== VALIDANDO CLIENTES ===")
antes2 = len(v)
v = v[v["Cliente"].isin(c["Cliente"])]
rech_cli = antes2 - len(v)
print("Filas rechazadas por cliente:", rech_cli)

print("\n=== CORRIGIENDO TIPOS ===")

numericas = ["Cantidad", "PrecioUnitario", "Total"] 
for col in numericas:
    v[col] = pd.to_numeric(v[col], errors="coerce")
    prom = v[col].mean()
    v[col] = v[col].fillna(prom)
    print(f"Columna {col} corregida con promedio {prom:.2f}")

print("\n=== INTEGRACIÓN DE DATOS ===")
v = v.merge(c, on="Cliente", how="left")
print("Merge con clientes listo.")
v = v.merge(p, on="Producto", how="left")
print("Merge con productos listo.")

print("\n=== RESULTADOS ===")
print("Filas finales:", len(v))
print("Primeras 10 filas:")
print(v.head(10))

#YAHIR ALEXIS LOPEZ 0703200503633