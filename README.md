

### Python Virtual Environment Setup 
```python
$ python -m venv venv            
$ source venv/bin/activate       
$ pip install -r requirements.txt
```

### Run unit tests
```python
$ cd test
$ pytest
```



# Point Cloud Generator

![Licencia](https://img.shields.io/badge/Licencia-MIT-blue.svg?style=for-the-badge)
![Versión](https://img.shields.io/badge/Versión-1.0.0-brightgreen.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)

## Descripción

*This project, developed for the course CE-5302: Computer Engineering Design Project, focuses on the implementation of an algorithm for point cloud stacking without camera pose information. Using techniques from computer vision and photogrammetry, the project aims to generate three-dimensional maps from individual point clouds.*

---

Este proyecto, desarrollado para el curso CE-5302: Proyecto de Diseño en Ingeniería en Computadores, se centra en la implementación de un algoritmo para la apilación de nubes de puntos sin información de la pose de la cámara. Utilizando técnicas de visión por computadora y fotogrametría, el proyecto tiene como objetivo generar mapas tridimensionales a partir de nubes de puntos individuales.

Este proyecto permite la carga, preprocesamiento y combinación de nubes de puntos utilizando la biblioteca Open3D. El proyecto incluye funcionalidades para:

- Cargar nubes de puntos desde archivos.
- Preprocesar las nubes de puntos (filtrado, eliminación de valores atípicos, etc.).
- Registrar nubes de puntos mediante métodos ICP.
- Optimizar la combinación de nubes de puntos.
- Guardar la nube de puntos combinada en un archivo .pcd.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Archivo de Configuración](#archivo-de-configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

## 1. Instalación

Estas son las instrucciones para instalar y configurar el entorno de desarrollo.

### Prerrequisitos

- Python 3.8 o superior
- pip

### Clonar el Repositorio

```sh
git clone https://github.com/JulianCamacho/point-cloud-generator
cd point-cloud-generator
```

### Crear un Entorno Virtual

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto:

```sh
python -m venv env
source env/bin/activate  # En Windows: `env\Scripts\activate`
```

### Instalar Dependencias

Instalar las dependencias necesarias utilizando `pip`:

```sh
pip install -r requirements.txt
```

## 2. Uso

### Ejecución Básica

Para ejecutar el proyecto, utilizar el siguiente comando:

```sh
python main.py
```

## 3. Archivo de Configuración

El archivo de configuración JSON debe contener parámetros necesarios para la carga y procesamiento de nubes de puntos. Asegúrese de que su archivo JSON tenga la siguiente estructura:

```json
{
    "input_path": "../data/cloud-points",
    "config_params": {
        "voxel_size": 0.02,
        "remove_outliers_params": {
            "nb_neighbors": 20,
            "std_ratio": 2.0
        },
        "combinability_threshold": 0.5
    },
    "output_file": "nube_pcd_combinada.pcd"
}
```

### Explicación de los Parámetros

- **input_path**: Ruta al directorio donde se encuentran los archivos de nubes de puntos.
- **config_params**:
  - **voxel_size**: Tamaño del voxel para el muestreo.
  - **remove_outliers_params**:
    - **nb_neighbors**: Número de vecinos para considerar al eliminar valores atípicos.
    - **std_ratio**: Ratio estándar para eliminar valores atípicos.
  - **combinability_threshold**: Umbral para determinar la combinabilidad de las nubes de puntos.
- **output_file**: Nombre del archivo `.pcd` donde se guardará la nube de puntos combinada.



## 4. Estructura del Proyecto

Explica la estructura del proyecto y la función de cada archivo/directorio importante.

```plaintext
point-cloud-generator/
├── data/                           # Directorio para los archivos de entrada
│   ├── cloud-points/               # Nubes de puntos individuales (.pcd)
├── doc                             # Documentación del proyecto
├── results/                        # Directorio para los archivos de salida
│   ├── nube_combinada.pcd          # Nube de puntos combinada
├── src/                            # Código fuente del proyecto
│   ├── config_reader.py            # Lectura de archivo de configuración
│   ├── main.py                     # Archivo principal toplevel
│   ├── pc_comparator.py            # Comparador de nubes de puntos
│   ├── pc_full_registration.py     # Aplicación de registration
│   ├── pc_preprocessing.py         # Preprocesamiento de las nubes
│   ├── pc_reader.py                # Lector de nubes de puntos .pcd
│   ├── pc_stacking.py              # Aplicación del algoritmo
│   ├── pc_writer.py                # Guardado de la nube resultante
│   ├── pose_graph_optimization.py  # Optimización del grafo de poses
├── tests/                          # Pruebas unitarias y funcionales
│   ├── test_stacker.py             # Pruebas para el algoritmo de stacking
├── utils                           # Utilidades varias para el proyecto
│   └── ply2pcd.py                  # Transformar archivos .ply a .pcd
├── README.md                       # Información del proyecto
├── requirements.txt                # Dependencias del proyecto
└── LICENSE                         # Licencia del proyecto
```

## 5. Contribuir

¡Contribuciones son bienvenidas! Por favor sigue estos pasos para contribuir:

1. Haz un Fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios.
4. Haz commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`).
5. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
6. Abre un Pull Request.

## 6. Licencia

Este proyecto está licenciado como código abierto bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 7. Contacto

José Julián Camacho Hernández - jjulian.341@gmail.com

Link del proyecto: [https://github.com/JulianCamacho/point-cloud-generator](https://github.com/JulianCamacho/point-cloud-generator)

