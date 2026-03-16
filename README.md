# Sistema de Gestión de Shopping

Trabajo Práctico N°3 de Algoritmos y Estructuras de Datos — UTN FRRo.

Sistema de consola para gestionar locales, usuarios y promociones de un shopping. Desarrollado en Python con persistencia en archivos binarios.

## Funcionalidades

- **Administrador:** gestión de locales, alta de dueños, aprobación de promociones y reportes.
- **Dueño de local:** creación de descuentos/promociones y reporte de uso.
- **Cliente:** búsqueda y solicitud de descuentos disponibles.

## Conceptos aplicados

- Programación Orientada a Objetos (clases, instancias, atributos)
- Archivos de acceso directo con `pickle`
- Búsqueda secuencial y búsqueda dicotómica
- Ordenamiento burbuja sobre archivos
- Validación de datos y manejo de errores

## Requisitos

- Python 3.10 o superior (se usa `match/case`)
- No requiere librerías externas

## Cómo ejecutar

```bash
git clone https://github.com/tu-usuario/sistema-shopping.git
cd sistema-shopping
python sistema_shopping.py
```

Al iniciar por primera vez se crea automáticamente la carpeta `datos_shopping/` con los archivos necesarios.

**Usuario admin por defecto:**
- Correo: `admin@shopping.com`
- Contraseña: `12345678`

## Estructura del proyecto

```
sistema-shopping/
├── sistema_shopping.py   # Código principal
├── datos_shopping/       # Archivos .dat generados al ejecutar (ignorados por git)
└── README.md
```

## Equipo

Desarrollado por Ian Kasperczak, Lautaro Peralta y Tomás Moreno como trabajo práctico grupal.
