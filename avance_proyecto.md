# Entregable: Avance de Proyecto – Primer Corte

**Proyecto:** Sistema de Análisis para la Biblioteca Académica
**Fecha de sustentación:** 21 de septiembre de 2026

---

## A. Definición del proyecto

| Elemento | Contenido |
|---|---|
| **Nombre del proyecto** | Sistema de Análisis de Demanda Bibliográfica |
| **Problemática** | Una biblioteca académica en Cartago, Valle, reorientó su colección para apoyar cinco programas (Ingeniería de Sistemas, Contabilidad, Agropecuaria, Administración de Empresas y Diseño e Integración Multimedia), pero no cuenta con un mecanismo claro para saber qué libros tienen alta demanda y pocos ejemplares disponibles, lo que puede dejar a los estudiantes sin acceso al material que más necesitan. |
| **Objetivo** | Analizar los datos de préstamos y stock del catálogo para identificar qué libros presentan alta demanda con bajo stock, generando información que apoye las decisiones de adquisición de nuevos ejemplares. |
| **Datos** | Base de datos de la biblioteca en formato CSV (11 archivos relacionados: libros, ejemplares, géneros, préstamos, usuarios, autores, editoriales, ubicaciones). Fuente: datos simulados para el proyecto académico, con estructura relacional equivalente a un sistema real de gestión bibliotecaria. |

---

## B. Estructura de datos

- **Archivo de datos:** `biblioteca_csv/` — 11 archivos CSV cargados en Python con `csv.DictReader`.
- **Lista de diccionarios:** cada archivo se convierte en una lista de diccionarios mediante la función `leer_datos()` / `cargar_datos()`.
- **Funciones definidas:**
  - `leer_datos(ruta_archivo)`: lee un CSV y lo convierte en lista de diccionarios.
  - `cargar_datos(carpeta_datos)`: carga los tres archivos necesarios (`libro.csv`, `ejemplar.csv`, `prestamo_ejemplar.csv`).
  - `construir_array_stock_prestamos(...)`: cruza los archivos y arma un array de NumPy con `[stock, préstamos]` por libro.
  - `calcular_estadisticas(...)`: calcula las estadísticas descriptivas.
  - `generar_visualizaciones(...)`: genera los gráficos con Matplotlib.
  - `libros_alta_demanda_bajo_stock(...)`: filtra los libros candidatos a compra usando indexación booleana de NumPy.

---

## C. Análisis exploratorio de datos (EDA) básico

**Variables analizadas:** `stock` (ejemplares disponibles por libro) y `préstamos` (veces que se ha prestado cada libro).

### Estadísticas con NumPy

| Variable | Promedio | Máximo | Mínimo | Desviación estándar |
|---|---|---|---|---|
| Stock | 2.20 | 5 | 1 | 1.19 |
| Préstamos | 1.05 | 7 | 0 | 1.16 |

### Gráfico con Matplotlib

Se generaron tres visualizaciones:
1. **Histograma** de la distribución de préstamos por libro (`distribucion_prestamos.png`).
2. **Gráfico de barras** con los préstamos totales por cada una de las 5 carreras priorizadas (`prestamos_por_carrera.png`).
3. **Gráfico de barras agrupadas** comparando stock vs préstamos para los 12 libros más críticos — alta demanda y bajo stock (`libros_criticos_stock_vs_prestamos.png`). Esta es la visualización que conecta directamente con la problemática del proyecto: muestra de un vistazo la brecha entre cuánto se pide un libro y cuántos ejemplares hay disponibles.

### Hallazgos

1. **La demanda está concentrada en pocos libros:** casi 480 de los 1200 libros del catálogo no registran ningún préstamo, mientras que un grupo reducido concentra entre 5 y 7 préstamos. Esto confirma un patrón típico de bibliotecas: pocos títulos populares y una larga cola de baja rotación.
2. **Administración de Empresas es la carrera con más préstamos (217), seguida de cerca por Contabilidad (205) e Ingeniería de Sistemas (201), mientras que Agropecuaria y Diseño e Integración Multimedia quedan últimas (195 cada una):** esto sugiere que, aunque el catálogo se repartió de forma pareja entre las 5 carreras, la demanda real de los estudiantes no es igual de pareja, y podría valer la pena reforzar la colección de las carreras con menor uso o investigar por qué su demanda es más baja. Además, se identificaron **65 libros** con alta demanda (3 o más préstamos) y bajo stock (3 ejemplares o menos) — candidatos directos para priorizar en la próxima compra de material.

---

## D. Control de versiones

- Repositorio en GitHub con el código (`cargar_datos.py`, `analisis_proyecto.py`, `eda_proyecto.py`) y los datos (`biblioteca_csv/`).
- Commits sugeridos para cubrir el mínimo de 3:
  1. `Carga inicial de datos CSV de la biblioteca`
  2. `Agrega análisis estadístico con NumPy`
  3. `Agrega visualizaciones con Matplotlib y detección de libros de alta demanda`
- `README.md` con la descripción del proyecto (ver archivo separado `README.md`).

---
