window_manager/
├── main.py                 # Punto de entrada
├── core/                   # Lógica de negocio
│   ├── __init__.py
│   ├── window_controller.py
│   ├── window_capture.py   # Nuevo: captura de ventanas
│   └── automation_engine.py
├── gui/                    # Capa de presentación
│   ├── __init__.py
│   ├── main_window.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── window_list.py
│   │   ├── control_panel.py
│   │   └── window_preview.py  # Nuevo: previsualización en tiempo real
│   └── styles/
│       ├── __init__.py
│       └── theme.py
├── models/                 # Modelos de datos
│   ├── __init__.py
│   └── window_data.py
├── utils/                  # Utilidades
│   ├── __init__.py
│   └── helpers.py
└── config/                 # Configuración
    ├── __init__.py
    └── settings.py