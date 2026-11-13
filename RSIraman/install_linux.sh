#!/bin/bash
#==============================================================================
# RSIRaman - Instalador para Linux
#==============================================================================
# Este script instala RSIRaman en sistemas Linux (Ubuntu, Fedora, Debian, etc.)
# Requiere: Python 3.7+, pip3, y privilegios de administrador (opcional)
#==============================================================================

set -e

INSTALL_DIR="$HOME/RSIRaman"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================================================="
echo "  RSIRaman - Instalador para Linux"
echo "  Reimplementación de RSIScan.exe (Raman Systems)"
echo "=============================================================================="
echo ""

# Detectar gestor de paquetes
if command -v apt-get &> /dev/null; then
    PKG_MGR="apt"
elif command -v dnf &> /dev/null; then
    PKG_MGR="dnf"
elif command -v yum &> /dev/null; then
    PKG_MGR="yum"
elif command -v pacman &> /dev/null; then
    PKG_MGR="pacman"
else
    PKG_MGR="unknown"
fi

echo "[1/5] Verificando dependencias del sistema..."

# Verificar Python 3
if ! command -v python3 &> /dev/null; then
    echo "  ERROR: Python 3 no está instalado."
    echo "  Instálelo manualmente antes de continuar."
    exit 1
fi
echo "  Python 3 encontrado: $(python3 --version)"

# Verificar pip3
if ! command -v pip3 &> /dev/null; then
    echo "  Instalando pip3..."
    if [ "$PKG_MGR" = "apt" ]; then
        sudo apt-get update && sudo apt-get install -y python3-pip python3-tk
    elif [ "$PKG_MGR" = "dnf" ]; then
        sudo dnf install -y python3-pip python3-tkinter
    elif [ "$PKG_MGR" = "yum" ]; then
        sudo yum install -y python3-pip python3-tkinter
    elif [ "$PKG_MGR" = "pacman" ]; then
        sudo pacman -S --needed python-pip tk
    fi
fi
echo "  pip3 encontrado"

echo ""
echo "[2/5] Copiando archivos a $INSTALL_DIR..."

if [ -d "$INSTALL_DIR" ]; then
    echo "  El directorio ya existe. Sobrescribiendo..."
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
cp -r "$SCRIPT_DIR/RSIRaman/"* "$INSTALL_DIR/"

echo "  Archivos copiados."

echo ""
echo "[3/5] Instalando dependencias de Python..."

pip3 install --user -r "$INSTALL_DIR/requirements.txt"

echo "  Dependencias instaladas."

echo ""
echo "[4/5] Creando acceso directo..."

# Crear script de lanzamiento (nombre que no colisione con el paquete rsiraman/)
cat > "$INSTALL_DIR/run_rsiraman" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec python3 main.py "\$@"
EOF
chmod +x "$INSTALL_DIR/run_rsiraman"

# Crear acceso directo en el escritorio (si existe)
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/RSIRaman.desktop" << EOF
[Desktop Entry]
Name=RSIRaman - Espectrómetro Raman
Comment=Lectura y análisis de espectros Raman
Exec=$INSTALL_DIR/run_rsiraman
Icon=$INSTALL_DIR/rsiraman_icon.png
Terminal=false
Type=Application
Categories=Science;Education;
EOF
    chmod +x "$HOME/Desktop/RSIRaman.desktop"
    echo "  Acceso directo creado en el escritorio."
fi

echo ""
echo "[5/5] Verificando instalación..."

if python3 -c "import tkinter; import matplotlib; import numpy; import scipy; import usb; print('Todas las dependencias OK')" 2>/dev/null; then
    echo "  Instalación verificada correctamente."
else
    echo "  ADVERTENCIA: Algunas dependencias de Python podrían faltar."
    echo "  Intente ejecutar: pip3 install -r $INSTALL_DIR/requirements.txt"
fi

echo ""
echo "=============================================================================="
echo "  ¡Instalación completada!"
echo ""
echo "  Para ejecutar RSIRaman:"
echo "    $INSTALL_DIR/run_rsiraman"
echo ""
echo "  O desde el menú de aplicaciones / escritorio."
echo "=============================================================================="
