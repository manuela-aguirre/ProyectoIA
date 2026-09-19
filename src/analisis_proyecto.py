import csv
import os
from collections import Counter

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "biblioteca_csv")

COLUMNAS_NUMERICAS = {
    "libro.csv": {"int": ["id_libro", "stock", "id_editorial"]},
    "ejemplar.csv": {
        "int": ["id_ejemplar", "id_libro", "id_ubicacion", "no_ejemplar", "paginas", "anio_edicion"],
        "float": ["valor"],
    },
    "prestamo.csv": {"int": ["id_prestamo", "id_usuario", "multa"]},
    "prestamo_ejemplar.csv": {"int": ["id_prestamo", "id_ejemplar"]},
    "genero.csv": {"int": ["id_genero"]},
    "libro_genero.csv": {"int": ["id_libro", "id_genero"]},
}


def leer_datos(ruta_archivo, columnas_int=None, columnas_float=None):
    """
    Lee un archivo CSV con csv.DictReader y lo convierte en una lista de
    diccionarios, convirtiendo las columnas indicadas a int o float.

    Parámetros:
        ruta_archivo (str): ruta al archivo .csv a leer.
        columnas_int (list[str], opcional): columnas a convertir a int.
        columnas_float (list[str], opcional): columnas a convertir a float.

    Retorna:
        list[dict]: lista de diccionarios con los datos ya tipados.
    """
    columnas_int = columnas_int or []
    columnas_float = columnas_float or []
    datos = []

    with open(ruta_archivo, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            for columna in columnas_int:
                valor = fila.get(columna, "")
                try:
                    fila[columna] = int(valor)
                except (TypeError, ValueError):
                    fila[columna] = None
            for columna in columnas_float:
                valor = fila.get(columna, "")
                try:
                    fila[columna] = float(valor)
                except (TypeError, ValueError):
                    fila[columna] = None
            datos.append(fila)

    return datos


def cargar_todos_los_datos():
    """Carga todos los archivos CSV del proyecto con sus columnas ya tipadas."""
    datos = {}
    for nombre_archivo in [
        "libro.csv", "ejemplar.csv", "prestamo.csv",
        "prestamo_ejemplar.csv", "genero.csv", "libro_genero.csv",
    ]:
        ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
        config = COLUMNAS_NUMERICAS.get(nombre_archivo, {})
        datos[nombre_archivo] = leer_datos(
            ruta,
            columnas_int=config.get("int"),
            columnas_float=config.get("float"),
        )
    return datos


def calcular_estadisticas(datos):
    """
    Calcula las estadísticas relevantes para el proyecto de biblioteca.

    Retorna:
        dict: diccionario con las estadísticas calculadas.
    """
    libros = datos["libro.csv"]
    ejemplares = datos["ejemplar.csv"]
    prestamos = datos["prestamo.csv"]
    prestamos_ejemplar = datos["prestamo_ejemplar.csv"]
    generos = datos["genero.csv"]
    libro_genero = datos["libro_genero.csv"]

    estadisticas = {}

    estadisticas["total_libros"] = len(libros)

    valores = [e["valor"] for e in ejemplares if isinstance(e["valor"], float)]
    estadisticas["total_ejemplares"] = len(ejemplares)
    estadisticas["promedio_valor_ejemplar"] = sum(valores) / len(valores) if valores else 0

    ejemplar_a_libro = {e["id_ejemplar"]: e["id_libro"] for e in ejemplares}
    libro_id_a_titulo = {l["id_libro"]: l["titulo"] for l in libros}
    conteo_prestamos_libro = Counter()
    for p in prestamos_ejemplar:
        id_libro = ejemplar_a_libro.get(p["id_ejemplar"])
        if id_libro is not None:
            conteo_prestamos_libro[id_libro] += 1

    if conteo_prestamos_libro:
        id_libro_top, cantidad_top = conteo_prestamos_libro.most_common(1)[0]
        estadisticas["libro_mas_prestado"] = libro_id_a_titulo.get(id_libro_top, "Desconocido")
        estadisticas["veces_prestado"] = cantidad_top
    else:
        estadisticas["libro_mas_prestado"] = None
        estadisticas["veces_prestado"] = 0

    conteo_fechas = Counter(p["fecha_prestamo"] for p in prestamos if p.get("fecha_prestamo"))
    if conteo_fechas:
        fecha_top, cantidad_fecha = conteo_fechas.most_common(1)[0]
        estadisticas["dia_mas_prestamos"] = fecha_top
        estadisticas["prestamos_en_ese_dia"] = cantidad_fecha
    else:
        estadisticas["dia_mas_prestamos"] = None
        estadisticas["prestamos_en_ese_dia"] = 0

    multas = [p["multa"] for p in prestamos if isinstance(p["multa"], int) and p["multa"] > 0]
    estadisticas["promedio_multa"] = sum(multas) / len(multas) if multas else 0
    estadisticas["prestamos_con_multa"] = len(multas)

    carreras_objetivo = {
        "Ingenieria de Sistemas", "Contabilidad", "Agropecuaria",
        "Administracion de Empresas", "Diseno e Integracion Multimedia",
    }
    id_genero_a_nombre = {g["id_genero"]: g["nombre"] for g in generos}
    nombre_a_id_genero = {v: k for k, v in id_genero_a_nombre.items()}
    ids_carreras = {nombre_a_id_genero[n] for n in carreras_objetivo if n in nombre_a_id_genero}

    libros_de_carrera = {lg["id_libro"] for lg in libro_genero if lg["id_genero"] in ids_carreras}
    estadisticas["libros_orientados_carreras"] = len(libros_de_carrera)
    estadisticas["porcentaje_libros_carreras"] = (
        len(libros_de_carrera) / len(libros) * 100 if libros else 0
    )

    conteo_generos = Counter(lg["id_genero"] for lg in libro_genero)
    generos_top = conteo_generos.most_common(3)
    estadisticas["top_generos"] = [
        (id_genero_a_nombre.get(id_g, "Desconocido"), cant) for id_g, cant in generos_top
    ]

    return estadisticas


def main():
    datos = cargar_todos_los_datos()
    estadisticas = calcular_estadisticas(datos)

    print("ESTADÍSTICAS DEL PROYECTO - BIBLIOTECA")
    for clave, valor in estadisticas.items():
        print(f"  - {clave}: {valor}")


if __name__ == "__main__":
    main()
