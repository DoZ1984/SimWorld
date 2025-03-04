# Estructura del Proyecto

src/
├── main.py                 # Punto de entrada principal
├── world/                  # Núcleo del simulador
│   ├── __init__.py
│   ├── world.py           # Clase principal del mundo
│   ├── time_manager.py    # Gestión del tiempo de simulación
│   └── event_manager.py    # Nuevo
├── entities/               # Entidades del mundo
│   ├── __init__.py
│   ├── person.py          # Clase Persona con atributos detallados
│   ├── corporation.py     # Corporaciones y empresas
│   ├── government.py      # Sistemas de gobierno
│   ├── job_market.py       # Nuevo
│   └── relationship.py      # Nuevo
├── systems/                # Subsistemas de simulación
│   ├── __init__.py
│   ├── economy.py         # Sistema económico
│   ├── politics.py        # Sistema político
│   ├── crime.py           # Sistema de crimen y justicia
│   ├── climate.py         # Sistema climático y desastres
│   ├── social.py           # Nuevo
│   └── education.py         # Nuevo
├── utils/                  # Utilidades y herramientas
│   ├── __init__.py
│   ├── data_loader.py     # Carga de datos iniciales
│   ├── logger.py          # Sistema de registro y estadísticas
│   ├── visualizer.py      # Herramientas de visualización
│   ├── name_generator.py   # Nuevo
│   └── helpers.py           # Nuevo
├── events/
│   ├── __init__.py
│   ├── base.py
│   ├── economic.py
│   ├── political.py
│   ├── natural.py
│   └── custom.py            # Nuevo
└── data/                    # Nueva carpeta
    ├── names/
    │   ├── first_names.csv
    │   └── last_names.csv
    └── config/
        └── default.yaml

# Actualización: 2024-03-17
## Cambios Implementados:
- Estructura completa de archivos implementada
- Sistema de nombres multicultural con 15k nombres
- Módulo de relaciones sociales básico
- Plantilla para sistema educativo
- Helpers para cálculos estadísticos
- Configuraciones iniciales en YAML

## Próximos Pasos:
1. Implementar sistema de educación básica
2. Crear modelo de familias y relaciones familiares
3. Desarrollar sistema de reputación dinámica
4. Integrar base de datos SQLite para persistencia
5. Implementar primer conjunto de eventos económicos

Reglas de Actualización:
- Verificar estructura antes de cada commit
- Actualizar este archivo tras cambios en la arquitectura
- Mantener consistencia entre documentación y código
- Usar comentarios detallados en el código fuente

Carpetas y Archivos

�� /simulador  (Núcleo del simulador)

📄 __init__.py (Inicialización del módulo)

📄 simulador.py (Clase principal del simulador)

📄 config.py (Configuración general del simulador)

📂 /modelos  (Definición de clases y entidades)

📄 individuo.py (Clase Individuo con atributos y métodos)

📄 sociedad.py (Clase Sociedad y estructuras sociales)

📄 economia.py (Sistema económico y corporaciones)

📄 politica.py (Gobiernos, leyes y sistemas políticos)

📄 crimen.py (Crimen, justicia y seguridad)

📄 desastres.py (Eventos y catástrofes naturales)

📄 tecnologia.py (Avances científicos y tecnológicos)

📂 /eventos  (Sistema de eventos y sucesos dinámicos)

📄 eventos_base.py (Modelo base de eventos)

📄 politicos.py (Eventos políticos y sociales)

📄 economicos.py (Eventos económicos y crisis)

📄 naturales.py (Desastres naturales y pandemias)

📄 personalizados.py (Eventos creados por el usuario)

📂 /datos  (Almacenamiento y persistencia)

📄 database.py (Manejo de base de datos local con SQLite)

📄 poblacion.json (Datos de individuos y sociedad)

📄 economia.json (Datos económicos y comerciales)

📄 politica.json (Datos de gobiernos y leyes)

📂 /interfaz  (Visualización y control del usuario)

📄 graficos.py (Generación de gráficos y reportes)

📄 control.py (Interacción y comandos del usuario)

📂 /utilidades  (Herramientas y funciones auxiliares)

📄 logger.py (Sistema de logs y depuración)

📄 utils.py (Funciones de utilidad para cálculos y transformaciones)

📄 main.py (Archivo principal para ejecutar el simulador)

Reglas de Actualización:

Cada vez que se agregue o elimine un archivo o carpeta, este documento debe actualizarse.

Antes de cada avance, la IA debe verificar que la estructura es correcta y está documentada.