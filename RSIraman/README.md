# RSIRaman - Espectrómetro Raman

**v1.1.0** — Reimplementación de RSIScan.exe (Raman Systems, Windows XP)  
Compatible con **Linux** y **Windows 10/11**

---

## ¿Qué es RSIRaman?

RSIRaman lee, visualiza y procesa datos de detectores Raman. Es una versión moderna y multiplataforma del software original RSIScan.exe, diseñado para funcionar en Windows XP.

---

## Instalación rápida

### Windows
1. Ejecute `install_windows.bat`
2. O manualmente: `pip install -r RSIRaman/requirements.txt` y luego `python RSIRaman/main.py`

### Linux
1. Ejecute `chmod +x install_linux.sh && ./install_linux.sh`
2. O manualmente: `pip3 install --user -r RSIRaman/requirements.txt` y luego `python3 RSIRaman/main.py`

---

## Uso básico

```
python main.py                    # Abre la GUI
python main.py --file archivo.csv # Carga un archivo al iniciar
python main.py --cal archivo.cfn  # Carga calibración al iniciar
```

### Funcionalidades principales
- 📁 Abrir archivos `.spc` y `.csv`
- ⚙️ Control de tiempo de integración (ms)
- 📐 Eje X: número de onda (cm⁻¹) ↔ longitud de onda (nm)
- 📊 Calibración polinomial (.cfn)
- 🔍 Suavizado binomial, línea base, detección de picos
- 💾 Guardar como CSV
- 🔌 Adquisición USB simulada (Ocean Optics)

---

## Documentación

Consulte `GUIA_USUARIO.md` para la guía completa de instalación y uso.

---

## Estructura

```
RSIRaman_Distribution/
├── install_linux.sh      # Instalador Linux
├── install_windows.bat   # Instalador Windows
├── GUIA_USUARIO.md       # Guía de usuario completa
├── README.md             # Este archivo
└── RSIRaman/             # Código fuente
    ├── main.py
    ├── requirements.txt
    └── rsiraman/         # Paquete Python
```

---

## Licencia

Uso educativo e investigación. No afiliado con Raman Systems, Inc.
