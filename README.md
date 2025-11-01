window_manager/
    ├── main.py                 # Punto de entrada
    ├── core/                   # Lógica de negocio
    │   ├── __init__.py
    │   ├── window_controller.py
    │   ├── window_capture.py   # Nuevo: captura de ventanas
    │   └── automation_engine.py
    ├── native/
    │   ├── CMakeLists.txt / setup.py      # Configuración de compilación   FUNCIONES MULTIPLATAFORMAS 
    │   ├── window_manager.cpp/.h          # Funciones de gestión de ventanas (listar, activar, bloquear)
    │   ├── window_capture.cpp/.h          # Captura de pantalla de ventanas
    │   ├── input_controller.cpp/.h        # Simulación de input (clicks, teclado)
    │   ├── utils.cpp/.h                   # Funciones auxiliares (conversión, errores, logging)
    │   ├── bindings.cpp                   # Punto de entrada pybind11 que expone todo a Python
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
    │   ├── __init__.py
    │   └── helpers.py
    └── config/                 # Configuración
        ├── __init__.py
        └── settings.py.


    https://dribbble.com/shots/25543032-Sidebar-Design-Dark-mode
