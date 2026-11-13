# RSIRaman - Guía de Usuario

**RSIRaman v1.1.0**  
Reimplementación de RSIScan.exe (Raman Systems, Windows XP)  
Compatible con **Linux** y **Windows 10/11**

---

## 1. Introducción

RSIRaman es una aplicación para leer, visualizar y procesar datos de detectores Raman. Es una versión moderna y multiplataforma del software original RSIScan.exe, que solo funcionaba en Windows XP.

### Funcionalidades principales

- **Lectura de archivos** `.spc` (formato Thermo Grams) y `.csv` (texto delimitado)
- **Calibración** mediante archivos `.cfn` (polinomio de 5to orden)
- **Control de tiempo de integración** (milissegundos)
- **Eje X seleccionable**: número de onda (cm⁻¹) o longitud de onda (nm)
- **Procesamiento**: suavizado binomial, resta de línea base, detección de picos
- **Adquisición simulada** de espectrómetros Ocean Optics (USB2000, HR2000, QE65000, etc.)
- **Guardado** de resultados en formato CSV

---

## 2. Instalación

### 2.1. En Windows (10 / 11)

#### Opción A: Instalador automático
1. Copie la carpeta `RSIRaman_Distribution` a su computadora
2. Haga doble clic en `install_windows.bat`
3. Siga las instrucciones en pantalla
4. Al finalizar, aparecerá un acceso directo en el escritorio

#### Opción B: Instalación manual
1. Instale Python 3 desde https://www.python.org/ (marque "Add Python to PATH")
2. Abra una terminal (Command Prompt o PowerShell)
3. Navegue a la carpeta `RSIRaman_Distribution/RSIRaman/`
4. Ejecute:
   ```
   pip install -r requirements.txt
   python main.py
   ```

### 2.2. En Linux

#### Opción A: Instalador automático
1. Copie la carpeta `RSIRaman_Distribution` a su directorio personal
2. Abra una terminal y ejecute:
   ```bash
   chmod +x install_linux.sh
   ./install_linux.sh
   ```
3. El instalador copiará los archivos, instalará dependencias y creará un acceso directo en el escritorio

#### Opción B: Instalación manual
1. Instale Python 3 y pip3 (por ejemplo: `sudo apt install python3-pip python3-tk` en Ubuntu/Debian)
2. Navegue a la carpeta `RSIRaman_Distribution/RSIRaman/`
3. Ejecute:
   ```bash
   pip3 install --user -r requirements.txt
   python3 main.py
   ```

---

## 3. Uso de la Aplicación

### 3.1. Inicio

Al iniciar RSIRaman verá una ventana dividida en dos áreas:

- **Panel izquierdo**: Controles de archivo, tiempo de integración, eje X, suavizado, detección de picos y hardware
- **Panel derecho**: Gráfico del espectro con barra de estado inferior

### 3.2. Cargar un espectro

1. Haga clic en **Archivo → Abrir...** o use el botón correspondiente
2. Seleccione un archivo `.spc` o `.csv`
3. El espectro se cargará y se mostrará en el gráfico

**Archivos de ejemplo incluidos:**
- `Data/Log/RDSample0004.csv` — Espectro de muestra en formato CSV
- `Data/Log/RDSample0004.spc` — Espectro de muestra en formato SPC
- `Configuration Files/ADUD4392.cfn` — Archivo de calibración de ejemplo

### 3.3. Modificar el tiempo de integración

El tiempo de integración determina cuánto tiempo está expuesto el detector a la luz láser durante cada medición.

1. En el panel izquierdo, busque **"Tiempo de integración (ms)"**
2. Ingrese el valor deseado en milissegundos (por ejemplo: `10000` para 10 segundos)
3. Haga clic en **Aplicar**
4. El valor se guarda y se usará en la próxima toma de muestra simulada

> **Nota:** Este valor se muestra en la barra de estado y se utiliza al conectar el espectrómetro o tomar una muestra.

### 3.4. Cambiar el eje X: Número de onda ↔ Longitud de onda

RSIRaman permite alternar entre dos representaciones del eje horizontal:

| Modo | Unidad | Descripción |
|------|--------|-------------|
| Número de onda | cm⁻¹ | Desplazamiento Raman relativo al láser |
| Longitud de onda | nm | Longitud de onda absoluta de la luz detectada |

**Para cambiar el eje X:**

1. Haga clic en el menú **Calibración**
2. Seleccione **"Eje X: Número de onda (cm⁻¹)"** o **"Eje X: Longitud de onda (nm)"**
3. O use los botones en el panel izquierdo

> **Importante:** Para que la conversión sea precisa, debe cargar primero un archivo de calibración `.cfn` (ver sección 3.5). Si no hay calibración cargada, se usará una conversión aproximada basada en el archivo `ADUD4392.cfn` (láser 532 nm).

### 3.5. Cargar calibración (.cfn)

La calibración relaciona el número de píxel del detector con la longitud de onda y el número de onda.

1. Haga clic en **Calibración → Cargar calibración (.cfn)...**
2. Seleccione un archivo `.cfn` (por ejemplo: `Configuration Files/ADUD4392.cfn`)
3. Se mostrará un mensaje confirmando la carga y la longitud de onda del láser

Una vez cargada la calibración:
- El eje X se muestra en **número de onda (cm⁻¹)** por defecto
- Puede cambiar a **longitud de onda (nm)** en cualquier momento

### 3.6. Procesamiento de espectros

#### Suavizado binomial
El suavizado reduce el ruido del espectro usando un filtro binomial de 7 puntos (el mismo que usa RSIScan original).

1. En el panel izquierdo, ajuste **"Suavizado binomial (pasadas)"** (0-10)
2. Haga clic en el botón **Detectar picos** o el cambio se aplica automáticamente
3. Mayor número de pasadas = espectro más suave pero menos detalle

#### Restar línea base
Elimina el fondo oscuro o ruido de fondo del espectro.

1. Haga clic en **Procesar → Restar línea base**
2. O use el botón en el panel izquierdo

#### Detectar picos
Identifica automáticamente los picos Raman en el espectro.

1. Ajuste **Sensibilidad picos** (altura mínima en counts, default: 10)
2. Ajuste **Espaciado picos** (distancia mínima entre picos, default: 20)
3. Haga clic en **Detectar picos**
4. Los picos se marcarán en rojo en el gráfico con sus valores

### 3.7. Adquisición simulada (sin hardware)

RSIRaman incluye un modo de simulación para pruebas sin necesidad de un espectrómetro real.

1. Haga clic en **Hardware → Conectar espectrómetro (simulado)**
2. Aparecerá un mensaje confirmando la conexión
3. Haga clic en **Toma de muestra (simulado)**
4. Se generará un espectro sintético con picos Raman realistas
5. Puede guardar el resultado como CSV

> **Nota:** Para usar un espectrómetro real (Ocean Optics USB2000, HR2000, QE65000, etc.), se requiere implementar la comunicación USB mediante `pyusb`. Actualmente está en modo simulado.

### 3.8. Guardar resultados

1. Haga clic en **Archivo → Guardar como CSV...**
2. Seleccione la ubicación y nombre de archivo
3. El espectro actual (con procesamiento aplicado) se guardará en formato CSV compatible con Excel y otros programas

---

## 4. Formatos de archivo soportados

| Formato | Extensión | Descripción |
|---------|-----------|-------------|
| CSV | `.csv` | Texto delimitado con coma. Primera línea es cabecera con fecha/hora |
| SPC | `.spc` | Formato binario Thermo Grams / Galactic Industries |
| Calibración | `.cfn` | Archivo de configuración con coeficientes polinomiales |

### Formatos de archivo CSV soportados

RSIRaman soporta dos variantes del formato CSV:

**Formato estándar (archivos de ejemplo en Data/Log):**
```
"CH: 0  1:00:45 PM 11/4/2007"
0,-28.33333
2.10063507572057,-28.33333
4.20127015144113,-28.33333
...
```

**Formato con sección de picos (archivos exportados desde RSIScan original):**
```
""
"CH: 0  1:00:45 PM 11/4/2007"
0,-28.33333
...                                  <- datos de curva continua (hasta 2048 puntos)
Peaks                                <- etiqueta que separa los bloques
390.7,253.9                          <- coordenadas de picos (x,y)
436.9,456.6
...
```

**Particularidades manejadas automáticamente:**
- Primera fila vacía o con comillas vacías `""` → se ignora
- Bloque de datos separado por la etiqueta `Peaks` → los picos se cargan y se muestran automáticamente en rojo sobre el gráfico
- Si no se separan los bloques, el eje X se leerían como texto y la gráfica se deformaría → RSIRaman evita este problema

### Ejemplo de archivo .cfn (calibración)
```
[COEFFICENTS]
Coefficient 1=3.62766573554561
Coefficient 2=-5.67557718583225E-04
Coefficient 3=-7.15552314679604E-07
Intercept=-217.5116195969
Laser Wavelength=532
Coefficient 4=7.53835032085828E-10
Coefficient 5=-2.3931207544578E-13
```

---

## 5. Ejemplo de uso completo

1. **Inicie RSIRaman**
2. **Cargue un archivo:** `Archivo → Abrir → Data/Log/RDSample0004.csv`
3. **Cargue calibración:** `Calibración → Cargar calibración (.cfn) → Configuration Files/ADUD4392.cfn`
4. **Cambie el eje:** `Calibración → Eje X: Longitud de onda (nm)` (o deje en número de onda)
5. **Aplique suavizado:** Ajuste pasadas a 2 y aplique
6. **Detecte picos:** Ajuste sensibilidad a 100, espaciado a 20, y haga clic en Detectar picos
7. **Guarde el resultado:** `Archivo → Guardar como CSV...`

---

## 6. Distribución a otros dispositivos

RSIRaman está diseñado para ser fácilmente transferible a otras computadoras.

### Para llevar RSIRaman en una USB o compartirlo:

1. Copie toda la carpeta `RSIRaman_Distribution/` a una memoria USB o comprímala en ZIP
2. En la computadora de destino:
   - **Windows:** Ejecute `install_windows.bat`
   - **Linux:** Ejecute `./install_linux.sh` (con permisos de ejecución)
3. No se requiere conexión a internet para usar la aplicación (solo para instalar dependencias la primera vez)

### Estructura de la carpeta de distribución

```
RSIRaman_Distribution/
├── RSIRaman/                    # Código fuente y ejecutable
│   ├── main.py                  # Punto de entrada
│   ├── requirements.txt         # Dependencias de Python
│   ├── rsiraman/                # Paquete principal
│   │   ├── __init__.py
│   │   ├── gui_common.py        # Interfaz gráfica
│   │   ├── spcreader.py         # Lector .spc
│   │   ├── csvreader.py         # Lector/escritor .csv
│   │   ├── calibration.py       # Calibración polinomial
│   │   ├── processing.py        # Procesamiento de señales
│   │   ├── usb_acquisition.py   # Adquisición USB (simulado)
│   │   └── config.py            # Manejo de configuración
│   ├── Configuration Files/     # Archivos .cfn de ejemplo
│   └── Data/                    # Datos de ejemplo (.spc, .csv)
├── install_linux.sh             # Instalador para Linux
├── install_windows.bat          # Instalador para Windows
├── GUIA_USUARIO.md              # Esta guía
└── README.md                    # Inicio rápido
```

---

## 7. Solución de problemas

| Problema | Solución |
|----------|----------|
| "Python no se encuentra" | Instale Python 3 y asegúrese de agregarlo al PATH |
| "No se puede importar tkinter" | Instale `python3-tk` (Linux) o reinstale Python (Windows) |
| "No se puede importar matplotlib" | Ejecute: `pip install matplotlib numpy scipy` |
| El gráfico no se muestra | Asegúrese de tener un entorno gráfico funcionando (X11 en Linux) |
| No se detecta el espectrómetro | Actualmente solo hay modo simulado. Para hardware real se necesita implementación USB adicional |
| El eje X no cambia | Cargue primero un archivo de calibración `.cfn` |

---

## 8. Acerca de RSIRaman

RSIRaman es una reimplementación del software RSIScan.exe v1.3.62 de Raman Systems, originalmente desarrollado en Visual Basic 6 para Windows XP.

Esta versión está escrita en Python 3 y es compatible con Linux y Windows modernos. No está afiliada con Raman Systems, Inc.

**Versión:** 1.1.0  
**Fecha:** Noviembre 2026  
**Licencia:** Uso educativo e investigación

---

## 9. Contacto y soporte

Para reportar problemas o sugerencias, consulte el archivo `README.md` incluido en la distribución o contacte al desarrollador del proyecto.
