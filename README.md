# Sistema de Análisis de Demanda Bibliográfica

Proyecto académico de Inteligencia Artificial — análisis de la demanda de préstamos en una biblioteca académica de Cartago, Valle.

## Problemática

La biblioteca reorientó su colección hacia cinco programas académicos (Ingeniería de Sistemas, Contabilidad, Agropecuaria, Administración de Empresas y Diseño e Integración Multimedia), pero no cuenta con una forma clara de saber qué libros tienen alta demanda y pocos ejemplares disponibles.

## Objetivo

Analizar los datos de préstamos y stock del catálogo para identificar qué libros presentan alta demanda con bajo stock, y así apoyar las decisiones de adquisición de nuevos ejemplares.

## Tecnologías

- Python
- NumPy
- Matplotlib
- Docker / Docker Compose
- Git / GitHub

## Estructura del proyecto

```
biblioteca-ia/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
├── avance_proyecto.md
│
├── src/
│   ├── main.py                # Punto de entrada: ejecuta todo el flujo
│   ├── cargar_datos.py        # Carga los CSV y muestra un resumen general
│   ├── analisis_proyecto.py   # Estadísticas relevantes del proyecto
│   └── eda_proyecto.py        # EDA con NumPy y Matplotlib (stock vs préstamos)
│
├── data/
│   └── biblioteca_csv/        # libro.csv, ejemplar.csv, prestamo.csv, etc.
│
├── outputs/                   # Gráficas generadas (PNG)
├── notebooks/                 # Jupyter notebooks (exploración adicional)
└── tests/                     # Pruebas
```

## Ejecución

Desde la raíz del proyecto:

```bash
docker compose build
docker compose up -d
```

Abrir una terminal dentro del contenedor:

```bash
docker exec -it biblioteca_ia bash
```

Y ejecutar cualquiera de los scripts:

```bash
python src/main.py               # Ejecuta todo el flujo completo
python src/cargar_datos.py       # Solo el resumen general
python src/analisis_proyecto.py  # Solo las estadísticas del proyecto
python src/eda_proyecto.py       # Solo el EDA con NumPy y Matplotlib
```

Detener el entorno:

```bash
docker compose down
```

## Análisis Exploratorio de Datos

Ver el detalle completo en `avance_proyecto.md`.

**Hallazgos principales:**
- La mayoría de los libros del catálogo casi no se prestan; la demanda se concentra en un grupo pequeño de títulos.
- Se identificaron 65 libros con alta demanda y bajo stock, candidatos prioritarios para la próxima compra de material.

Las gráficas generadas (`distribucion_prestamos.png` y `stock_vs_prestamos.png`) quedan disponibles en la carpeta `outputs/`.

## Próximos pasos

- Incorporar variables como género/carrera, editorial y año de edición al análisis.
- Explorar un modelo simple de clasificación con Scikit-Learn.
- Automatizar un reporte periódico de libros a priorizar en compra.
