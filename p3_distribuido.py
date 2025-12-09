import pandas as pd


ruta = "ventas.csv"
chunksize = 1000

total_final_global = 0.0
ventas_por_producto = {}
chunk_mas_alto = None
valor_mas_alto = 0.0

print("Procesando en chunks de", chunksize)
for i, chunk in enumerate(pd.read_csv(ruta, chunksize=chunksize)):
    print(f"Procesando chunk {i} con {len(chunk)} filas")

    
    chunk["Cantidad"] = pd.to_numeric(chunk["Cantidad"], errors="coerce").fillna(0)

    chunk["PrecioUnitario"] = pd.to_numeric(chunk["PrecioUnitario"], errors="coerce").fillna(0)
    chunk["Total"] = pd.to_numeric(chunk["Total"], errors="coerce").fillna(0)

    
    chunk["Subtotal"] = chunk["Cantidad"] * chunk["PrecioUnitario"]

    def impuesto_por_valor(x):
        if x < 5000:
            return x * 0.10
        elif x <= 20000:
            return x * 0.15
        else:
            return x * 0.18

    chunk["Impuesto"] = chunk["Total"].apply(impuesto_por_valor)
    chunk["Total_Final"] = chunk["Total"] + chunk["Impuesto"]

    suma_chunk = chunk["Total_Final"].sum()
    total_final_global += suma_chunk

    print(f" -> Total_Final chunk {i}: {suma_chunk}")


    if suma_chunk > valor_mas_alto:
        valor_mas_alto = suma_chunk
        chunk_mas_alto = i

  
    grp = chunk.groupby("Producto")["Total_Final"].sum()
    for prod, val in grp.items():
        ventas_por_producto[prod] = ventas_por_producto.get(prod, 0.0) + val

print("---- RESULTADOS AGREGADOS ----")
print("Total Final Global:", total_final_global)


top5 = sorted(ventas_por_producto.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 productos mas vendidos:")
for prod, val in top5:
    print(f"  {prod}: {val}")

print("Chunk con mayor contribucion en ventas:", chunk_mas_alto)


#YAHIR ALEXIS LOPEZ 0703200503633