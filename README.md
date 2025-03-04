# Simulador de Sociedades Complejas

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simulador de mundo ultra detallado que modela sociedades complejas con múltiples sistemas interconectados.

## Características Principales
- Simulación de individuos con necesidades y comportamientos complejos
- Sistema económico dinámico con oferta/demanda
- Modelado político y legal
- Sistema de eventos globales y catástrofes
- Interfaz de usuario para control y visualización

## Requisitos
- Python 3.10+
- Dependencias: `pip install -r requirements.txt`

## Uso
```python
from world import World

config = WorldConfig(population_size=1000)
world = World(config)
world.run(years=10)
```

## Estructura del Proyecto
Ver [SIM_files.md](SIM_files.md)

## Contribución
1. Haz fork del proyecto
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request 