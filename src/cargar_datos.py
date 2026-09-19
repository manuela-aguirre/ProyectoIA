import csv
import os
from collections import Counter

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "biblioteca_csv")


def leer_datos(ruta_archivo):
    """
    Lee un archivo CSV y lo convierte en una lista de diccionarios.

    Parámetros:
        ruta_archivo (str): ruta al archivo .csv a leer.

    Retorna:
        list[dict]: lista de diccionarios con los datos del archivo.
    """
    datos = []
    with open(ruta_archivo, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            datos.append(fila)
    return datos


def mostrar_resumen(datos, nombre_archivo, columna_numerica=None):
    """
    Muestra la cantidad total de registros y, si se indica una columna
    numérica, el promedio de esa columna.

    Parámetros:
        datos (list[dict]): datos ya leídos con leer_datos().
        nombre_archivo (str): nombre descriptivo del archivo.
        columna_numerica (str, opcional): columna numérica para el promedio.
    """
    total_registros = len(datos)
    print(f"\nArchivo: {nombre_archivo}")
    print(f"  - Cantidad total de registros: {total_registros}")

    if columna_numerica and total_registros > 0 and columna_numerica in datos[0]:
        valores = []
        for fila in datos:
            valor_texto = fila.get(columna_numerica, "")
            try:
                valores.append(float(valor_texto))
            except (TypeError, ValueError):
                continue

        if valores:
            promedio = sum(valores) / len(valores)
            print(f"  - Promedio de la columna '{columna_numerica}': {promedio:.2f}")
        else:
            print(f"  - No se encontraron valores numéricos válidos en '{columna_numerica}'.")


def libro_mas_prestado(prestamos_ejemplar, ejemplares, libros):
    """
    Determina cuál es el libro con más préstamos registrados.

    Parámetros:
        prestamos_ejemplar (list[dict]): datos de prestamo_ejemplar.csv.
        ejemplares (list[dict]): datos de ejemplar.csv.
        libros (list[dict]): datos de libro.csv.

    Retorna:
        tuple: (titulo_libro, cantidad_prestamos) o (None, 0) si no hay datos.
    """
    ejemplar_a_libro = {e["id_ejemplar"]: e["id_libro"] for e in ejemplares}
    libro_id_a_titulo = {l["id_libro"]: l["titulo"] for l in libros}

    conteo = Counter()
    for prestamo in prestamos_ejemplar:
        id_libro = ejemplar_a_libro.get(prestamo["id_ejemplar"])
        if id_libro:
            conteo[id_libro] += 1

    if not conteo:
        return None, 0

    id_libro_top, cantidad = conteo.most_common(1)[0]
    titulo = libro_id_a_titulo.get(id_libro_top, "Desconocido")
    return titulo, cantidad


def dia_con_mas_prestamos(prestamos):
    """
    Determina qué día (fecha) tuvo la mayor cantidad de préstamos.

    Parámetros:
        prestamos (list[dict]): datos de prestamo.csv.

    Retorna:
        tuple: (fecha, cantidad_prestamos) o (None, 0) si no hay datos.
    """
    conteo = Counter(p["fecha_prestamo"] for p in prestamos if p.get("fecha_prestamo"))

    if not conteo:
        return None, 0

    fecha_top, cantidad = conteo.most_common(1)[0]
    return fecha_top, cantidad


def main():
    archivos_csv = [
        "autor.csv",
        "autor_libro.csv",
        "editorial.csv",
        "ejemplar.csv",
        "genero.csv",
        "libro.csv",
        "libro_genero.csv",
        "prestamo.csv",
        "prestamo_ejemplar.csv",
        "ubicacion.csv",
        "usuario.csv",
    ]

    print("RESUMEN DE DATOS - BIBLIOTECA")

    datos_por_archivo = {}
    for nombre_archivo in archivos_csv:
        ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
        datos = leer_datos(ruta)
        datos_por_archivo[nombre_archivo] = datos

        if nombre_archivo == "ejemplar.csv":
            mostrar_resumen(datos, nombre_archivo, columna_numerica="valor")
        else:
            mostrar_resumen(datos, nombre_archivo)

    titulo_top, cantidad_top = libro_mas_prestado(
        datos_por_archivo["prestamo_ejemplar.csv"],
        datos_por_archivo["ejemplar.csv"],
        datos_por_archivo["libro.csv"],
    )
    print(f"\nLibro más prestado: {titulo_top} ({cantidad_top} préstamos)")

    fecha_top, cantidad_fecha = dia_con_mas_prestamos(datos_por_archivo["prestamo.csv"])
    print(f"Día con más préstamos: {fecha_top} ({cantidad_fecha} préstamos)")


if __name__ == "__main__":
    main()
