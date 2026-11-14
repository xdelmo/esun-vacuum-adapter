#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="${PROJECT_DIR}/output"
BAMBU_CLI="/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"

echo "==> 1. Esecuzione verifiche geometriche FDM (pytest)..."
"${PROJECT_DIR}/.venv/bin/python" -m pytest "${PROJECT_DIR}/checks/check_fit.py" -v

echo "==> 2. Generazione solido CAD (STEP e STL)..."
"${PROJECT_DIR}/.venv/bin/python" "${PROJECT_DIR}/src/generate_adapter.py"

echo "==> 3. Generazione progetto 3MF con Bambu Studio CLI..."
mkdir -p "${OUTPUT_DIR}"

if [ -f "$BAMBU_CLI" ]; then
  "$BAMBU_CLI" \
    "${OUTPUT_DIR}/esun_adapter.stl" \
    --load-settings "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/machine/Bambu Lab A1 mini 0.4 nozzle.json;/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/process/0.16mm Optimal @BBL A1M.json" \
    --load-filaments "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL/filament/Generic PLA @BBL A1M.json" \
    --export-3mf "${OUTPUT_DIR}/esun_adapter_temp.3mf"

  echo "==> 4. Applicazione patch impostazioni PLA ermetico..."
  "${PROJECT_DIR}/.venv/bin/python" "${PROJECT_DIR}/src/patch_3mf.py" \
    "${OUTPUT_DIR}/esun_adapter_temp.3mf" \
    "${OUTPUT_DIR}/esun_adapter.3mf"
  rm -f "${OUTPUT_DIR}/esun_adapter_temp.3mf"
  echo "==> Fatto! File 3MF pronto per la stampa in output/esun_adapter.3mf"
else
  echo "AVVISO: Bambu Studio CLI non trovata in $BAMBU_CLI. STL e STEP sono comunque disponibili in output/."
fi
