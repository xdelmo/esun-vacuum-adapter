# eSUN Vacuum Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a procedural, airtight 3D-printable adapter in PLA that connects an intake nozzle (Ø20mm, height 5mm) to eSUN vacuum filament bags (Ø30mm valve, depth 1mm), fully automated with Python `build123d`, pytest checks, and Bambu Studio CLI.

**Architecture:** The model is an autoportant (zero-support) revolution/extrusion solid generated via `build123d` in `src/generate_adapter.py` reading constants from `src/config.py`. Geometric rules and printability are asserted by `checks/check_fit.py` before exporting STEP/STL files to `output/`. An orchestration script `build.sh` invokes Bambu Studio CLI on macOS to produce a 3MF project with PLA profile settings patched by `src/patch_3mf.py` for 100% solid, airtight perimeters.

**Tech Stack:** Python 3.12+ (in local `.venv`), `build123d>=0.11`, `pytest`, Bambu Studio CLI (`/Applications/BambuStudio.app/Contents/MacOS/BambuStudio`), bash.

## Global Constraints

- Project root: `~/development/hobbies/esun-vacuum-adapter/`
- Material: Generic PLA (profile: `0.16mm Optimal @BBL A1M`)
- Printer target: Bambu Lab A1 mini (0.4 mm nozzle, bed 180×180×180 mm)
- Support requirement: 0% supports (100% self-supporting, no overhangs > 45°)
- Both ends female: Vacuum socket Ø20.2 mm (depth 5.0 mm); eSUN valve recess Ø30.2 mm (depth 1.0 mm)
- Air passage bore: Ø14.0 mm continuous smooth cylinder
- Total height: 20.0 mm
- Bottom outer diameter (bed): 25.0 mm with 0.4 mm chamfer
- Top outer diameter: 35.0 mm
- Wall thickness: minimum 2.4 mm everywhere
- Privacy: author `xdelmo` (`84925809+xdelmo@users.noreply.github.com`), no real names, no personal emails, no `/Users/<name>/` absolute paths in committed code or docs.

---

### Task 1: Scaffolding, Documentation and Agent Guidelines

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `CLAUDE.md`
- Create: `AGENTS.md` (symlink to `CLAUDE.md`)
- Create: `README.md`
- Create: `docs/hardware_context.md`
- Create: `docs/measurements.md`

**Interfaces:**
- Consumes: Nothing
- Produces: Project root structure, virtual environment, and agent instructions.

- [ ] **Step 1: Write requirements.txt and pytest.ini**

Create `requirements.txt`:
```txt
build123d>=0.11
pytest
```

Create `pytest.ini`:
```ini
[pytest]
testpaths = checks
```

- [ ] **Step 2: Create virtual environment and install dependencies**

Run:
```bash
cd ~/development/hobbies/esun-vacuum-adapter
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```
Verify: `.venv/bin/python -c "import build123d; import pytest; print('OK')"` outputs `OK`.

- [ ] **Step 3: Create CLAUDE.md and AGENTS.md symlink**

Create `CLAUDE.md`:
```markdown
# CLAUDE.md — Linee guida del progetto esun-vacuum-adapter

Linee guida e convenzioni per Claude e agenti di sviluppo (AGY).

## 1. Contesto del Progetto
Adattatore rigido stampato in 3D in PLA per collegare un aspirapolvere (beccuccio maschio Ø20mm, sporgenza 5mm) alle buste per sottovuoto filamento eSUN (valvola circolare Ø30mm, rilievo 1mm). Entrambi gli innesti sull'adattatore sono a bicchiere femmina.

## 2. Comandi Principali
Tutti i comandi vanno eseguiti dalla radice del repository:
```bash
# Esecuzione controlli geometrici e tolleranze FDM
.venv/bin/python -m pytest checks/check_fit.py -v

# Generazione CAD isolata (STEP e STL in output/)
.venv/bin/python src/generate_adapter.py

# Pipeline completa (pytest -> CAD -> 3MF Bambu Studio -> Patch PLA)
./build.sh
```

## 3. Architettura & Pipeline
- `src/config.py`: quote dimensionali misurate e costanti geometriche.
- `src/generate_adapter.py`: modellazione procedurale con `build123d` (`BuildPart`). Esporta STEP e STL in `output/`.
- `checks/check_fit.py`: suite `pytest` che verifica spessori minimi parete, giochi FDM e assenza di supporti.
- `build.sh`: script di build che invoca la CLI di Bambu Studio e lancia `src/patch_3mf.py`.
- `src/patch_3mf.py`: patch del file 3MF per impostare 5 perimetri e 100% infill in PLA per tenuta stagna.

## 4. Sistema di Riferimento & Coordinate CAD
- **Origine (X=0, Y=0)**: centro dell'asse assialsimmetrico del condotto d'aria.
- **Piano Z=0**: faccia inferiore a contatto con il piatto di stampa (lato aspiratore).
- **Asse +Z**: orientato verticalmente verso l'alto (verso la campana eSUN a Z=20 mm).
- **Materiale e Stampa**: Generic PLA su Bambu Lab A1 mini (0.4 nozzle). Nessun supporto (angoli $\le 45^\circ$).

## 5. Regole di Sviluppo
- Pipeline obbligatoria: eseguire `./build.sh` e verificare che tutti i test siano verdi prima di ogni commit.
- File temporanei e di prova: posizionati esclusivamente in `tmp/` (ignorato da git).
- Documentazione sincronizzata: aggiornare i file in `docs/` nello stesso commit in cui il codice cambia.
```

Create symlink `AGENTS.md`:
```bash
ln -s CLAUDE.md AGENTS.md
```

- [ ] **Step 4: Create documentation files (README.md, docs/hardware_context.md, docs/measurements.md)**

Create `README.md`:
```markdown
# eSUN Vacuum Adapter

Adattatore rigido parametrico stampato in PLA per collegare un aspirapolvere convenzionale (beccuccio Ø20 mm sporgente 5 mm) alle buste per sottovuoto filamento eSUN (valvola circolare Ø30 mm, incavo 1 mm).

Progettato con Python `build123d` per stampa 3D FDM senza supporti su Bambu Lab A1 mini.

## Utilizzo Rapido
```bash
./build.sh
```
Il file pronto per la stampa viene generato in `output/esun_adapter.3mf`.
```

Create `docs/hardware_context.md`:
```markdown
# Hardware Context — Aspiratore & Buste eSUN

## Aspiratore
- Interfaccia: Beccuccio cilindrico maschio sporgente.
- Diametro esterno beccuccio: 20.0 mm.
- Altezza/sporgenza beccuccio: 5.0 mm.
- Accoppiamento adattatore: Innesto femmina a bicchiere Ø 20.2 mm profondo 5.0 mm.

## Busta Filamento eSUN (eVacuum)
- Interfaccia: Valvola circolare a rilievo sulla superficie della busta.
- Diametro esterno ghiera valvola: 30.0 mm.
- Spessore rilievo valvola: 1.0 mm.
- Accoppiamento adattatore: Campana femmina Ø 30.2 mm profonda 1.0 mm con battuta piana anulare di 8.1 mm di larghezza per tenuta stagna a compressione diretta.

## Condotto d'Aria
- Foro cilindrico passante liscio Ø 14.0 mm continuo per massimo flusso volumetrico senza occlusioni.
```

Create `docs/measurements.md`:
```markdown
# Registro Quote Misurate & Tolleranze CAD

| Parametro | Quota Nominale Misurata (mm) | Quota CAD Modellata (mm) | Tolleranza FDM PLA | Note |
| :--- | :--- | :--- | :--- | :--- |
| Diametro beccuccio aspiratore | 20.0 | 20.2 (interno) | +0.2 mm | Accoppiamento a frizione agevole |
| Altezza beccuccio aspiratore | 5.0 | 5.0 (profondità) | 0.0 mm | Battuta d'arresto interna a 45° |
| Diametro valvola eSUN | 30.0 | 30.2 (interno) | +0.2 mm | Centraggio campana sulla valvola |
| Profondità valvola eSUN | 1.0 | 1.0 (profondità) | 0.0 mm | Battuta piana perimetrale |
| Diametro canale aria | — | 14.0 (passante) | — | Ottimale per flusso in depressione |
| Diametro base (piatto) | — | 25.0 (esterno) | — | Parete minima 2.4 mm |
| Diametro testa (campana) | — | 35.0 (esterno) | — | Parete minima 2.4 mm |
| Altezza totale | — | 20.0 | — | Profilo compatto autoportante |
```

- [ ] **Step 5: Verify symlink and test runner**

Run:
```bash
ls -l AGENTS.md
.venv/bin/pytest --version
```
Expected: `AGENTS.md -> CLAUDE.md`, pytest reports installed version.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt pytest.ini CLAUDE.md AGENTS.md README.md docs/
git commit -m "chore: scaffold project structure, documentation and agent guidelines"
```

---

### Task 2: Configuration Constants and Geometric Validation Test Suite

**Files:**
- Create: `src/config.py`
- Create: `checks/check_fit.py`

**Interfaces:**
- Consumes: Scaffolding from Task 1.
- Produces: `src.config` exports: `VACUUM_NOZZLE_D`, `VACUUM_NOZZLE_H`, `VALVE_OUTER_D`, `VALVE_RECESS_DEPTH`, `FIT_CLEARANCE`, `AIR_BORE_D`, `TOTAL_H`, `BOTTOM_OUTER_D`, `TOP_OUTER_D`, `CHAMFER_BED`.

- [ ] **Step 1: Write the failing tests in checks/check_fit.py**

Create `checks/check_fit.py`:
```python
import pytest
import math

def test_config_dimensions():
    from src import config

    # Hierarchy of diameters
    assert config.VALVE_OUTER_D > config.VACUUM_NOZZLE_D > config.AIR_BORE_D
    assert config.TOP_OUTER_D > config.VALVE_OUTER_D
    assert config.BOTTOM_OUTER_D > config.VACUUM_NOZZLE_D

    # Sockets internal diameters with clearance
    vacuum_socket_d = config.VACUUM_NOZZLE_D + config.FIT_CLEARANCE
    valve_recess_d = config.VALVE_OUTER_D + config.FIT_CLEARANCE
    assert vacuum_socket_d == pytest.approx(20.2, abs=0.01)
    assert valve_recess_d == pytest.approx(30.2, abs=0.01)

    # Minimum wall thickness check
    bottom_wall = (config.BOTTOM_OUTER_D - vacuum_socket_d) / 2.0
    top_wall = (config.TOP_OUTER_D - valve_recess_d) / 2.0
    mid_wall = (config.BOTTOM_OUTER_D - config.AIR_BORE_D) / 2.0

    assert bottom_wall >= 2.0, f"Bottom wall too thin: {bottom_wall} mm"
    assert top_wall >= 2.0, f"Top wall too thin: {top_wall} mm"
    assert mid_wall >= 2.0, f"Mid body wall too thin: {mid_wall} mm"

    # Total height consistency
    assert config.TOTAL_H == pytest.approx(20.0, abs=0.01)

    # Transition slope check (must be <= 45 degrees overhang)
    # The internal transition goes from vacuum socket to bore: radial step = (vacuum_socket_d - air_bore_d)/2
    radial_step = (vacuum_socket_d - config.AIR_BORE_D) / 2.0
    # For a 45 deg chamfer, height must equal radial step
    internal_taper_h = radial_step
    assert config.VACUUM_NOZZLE_H + internal_taper_h < config.TOTAL_H - config.VALVE_RECESS_DEPTH
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
.venv/bin/python -m pytest checks/check_fit.py -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'src'` or `cannot import name 'config'`.

- [ ] **Step 3: Write minimal implementation in src/config.py**

Create `src/__init__.py`: empty file.
Create `src/config.py`:
```python
"""
src/config.py
Quote parametriche e costanti geometriche per l'adattatore eSUN.
Tutte le quote sono espresse in millimetri (mm).
"""

# Quote beccuccio aspirapolvere
VACUUM_NOZZLE_D = 20.0          # Diametro esterno beccuccio aspiratore
VACUUM_NOZZLE_H = 5.0           # Profondità cavità beccuccio aspiratore

# Quote valvola sacchetto eSUN
VALVE_OUTER_D = 30.0            # Diametro esterno valvola eSUN
VALVE_RECESS_DEPTH = 1.0        # Profondità sede valvola eSUN

# Condotto aria e quote globali
AIR_BORE_D = 14.0               # Diametro foro passante centrale continuo
TOTAL_H = 20.0                  # Altezza complessiva adattatore

# Tolleranze e quote FDM PLA
FIT_CLEARANCE = 0.2             # Gioco radiale/diametrale per accoppiamenti
BOTTOM_OUTER_D = 25.0           # Diametro esterno base (lato piatto/aspiratore)
TOP_OUTER_D = 35.0              # Diametro esterno testa (lato campana eSUN)
CHAMFER_BED = 0.4               # Smusso anti zampa d'elefante sul piatto (Z=0)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
.venv/bin/python -m pytest checks/check_fit.py -v
```
Expected: `1 passed in 0.0X s`.

- [ ] **Step 5: Commit**

```bash
git add src/__init__.py src/config.py checks/check_fit.py
git commit -m "feat: add geometric configuration and validation test suite"
```

---

### Task 3: Parametric CAD Modeling with build123d

**Files:**
- Create: `src/generate_adapter.py`
- Modify: `checks/check_fit.py`

**Interfaces:**
- Consumes: `src.config`
- Produces: `src.generate_adapter.create_adapter()` returning `build123d.Part`, exports `output/esun_adapter.step` and `output/esun_adapter.stl`.

- [ ] **Step 1: Add solid CAD geometry verification tests in checks/check_fit.py**

Append to `checks/check_fit.py`:
```python
def test_cad_part_geometry():
    from src.generate_adapter import create_adapter
    from src import config

    part = create_adapter()

    # Part must be a valid solid
    assert part.is_valid
    assert len(part.solids()) == 1

    # Bounding box verification
    bbox = part.bounding_box()
    assert bbox.size.Z == pytest.approx(config.TOTAL_H, abs=0.05)
    assert bbox.size.X == pytest.approx(config.TOP_OUTER_D, abs=0.05)
    assert bbox.size.Y == pytest.approx(config.TOP_OUTER_D, abs=0.05)

    # Volume must be positive and within realistic solid bounds
    # Cyl 35x20 has volume ~ 19242 mm3, hollow bore ~ 3000 mm3 -> net volume ~ 8000-14000 mm3
    assert 7000.0 < part.volume < 15000.0
```

- [ ] **Step 2: Run test to verify failure**

Run:
```bash
.venv/bin/python -m pytest checks/check_fit.py -k test_cad_part_geometry -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'src.generate_adapter'`.

- [ ] **Step 3: Implement src/generate_adapter.py**

Create `src/generate_adapter.py`:
```python
"""
src/generate_adapter.py
Modellazione CAD procedurale dell'adattatore per aspiratore e buste eSUN con build123d.
"""

from pathlib import Path
from build123d import (
    BuildPart,
    BuildSketch,
    Plane,
    Circle,
    Cone,
    Cylinder,
    extrude,
    export_step,
    export_stl,
    chamfer,
    Axis,
)
from src import config

def create_adapter():
    """
    Crea il solido dell'adattatore mediante operazioni booleane build123d su piani assoluti.
    """
    vacuum_socket_d = config.VACUUM_NOZZLE_D + config.FIT_CLEARANCE
    valve_recess_d = config.VALVE_OUTER_D + config.FIT_CLEARANCE
    radial_step = (vacuum_socket_d - config.AIR_BORE_D) / 2.0
    taper_h = radial_step  # Transizione a 45 gradi

    with BuildPart() as adapter:
        # 1. Corpo esterno:
        # Base cilindrica Z=0 -> Z=5.0
        with BuildSketch(Plane.XY):
            Circle(radius=config.BOTTOM_OUTER_D / 2.0)
        extrude(amount=config.VACUUM_NOZZLE_H)

        # Transizione tronco-conica da Z=5.0 a Z=15.0 (sale da 25mm a 35mm di diametro esterno)
        cone_h = (config.TOP_OUTER_D - config.BOTTOM_OUTER_D) / 2.0  # 5.0 mm di altezza a 45 gradi
        cone_z = config.VACUUM_NOZZLE_H
        with BuildSketch(Plane.XY.offset(cone_z)):
            Circle(radius=config.BOTTOM_OUTER_D / 2.0)
        with BuildSketch(Plane.XY.offset(cone_z + cone_h)):
            Circle(radius=config.TOP_OUTER_D / 2.0)
        # Loft/Cone tra i due sketch
        Cone(
            bottom_radius=config.BOTTOM_OUTER_D / 2.0,
            top_radius=config.TOP_OUTER_D / 2.0,
            height=cone_h,
            align=(None, None, None),
        ).locate(Plane.XY.offset(cone_z).location)

        # Parte superiore cilindrica da Z=10.0 a Z=20.0 a diametro 35mm
        top_cyl_z = cone_z + cone_h
        top_cyl_h = config.TOTAL_H - top_cyl_z
        with BuildSketch(Plane.XY.offset(top_cyl_z)):
            Circle(radius=config.TOP_OUTER_D / 2.0)
        extrude(amount=top_cyl_h)

        # 2. Sottrazioni interne:
        # a) Cavità femmina aspiratore a Z=0 fino a Z=5.0
        with BuildSketch(Plane.XY):
            Circle(radius=vacuum_socket_d / 2.0)
        extrude(amount=config.VACUUM_NOZZLE_H, mode=BuildPart.Mode.SUBTRACT)

        # b) Raccordo conico interno a 45 gradi da Z=5.0 a Z=5.0 + taper_h (da vacuum_socket_d a AIR_BORE_D)
        Cone(
            bottom_radius=vacuum_socket_d / 2.0,
            top_radius=config.AIR_BORE_D / 2.0,
            height=taper_h,
            mode=BuildPart.Mode.SUBTRACT,
        ).locate(Plane.XY.offset(config.VACUUM_NOZZLE_H).location)

        # c) Condotto centrale passante Ø 14mm continuo da Z=5.0 + taper_h fino a Z=19.0
        with BuildSketch(Plane.XY.offset(config.VACUUM_NOZZLE_H + taper_h)):
            Circle(radius=config.AIR_BORE_D / 2.0)
        extrude(
            amount=config.TOTAL_H - (config.VACUUM_NOZZLE_H + taper_h),
            mode=BuildPart.Mode.SUBTRACT,
        )

        # d) Campana femmina valvola eSUN a Z=19.0 fino a Z=20.0
        recess_z = config.TOTAL_H - config.VALVE_RECESS_DEPTH
        with BuildSketch(Plane.XY.offset(recess_z)):
            Circle(radius=valve_recess_d / 2.0)
        extrude(amount=config.VALVE_RECESS_DEPTH, mode=BuildPart.Mode.SUBTRACT)

        # 3. Smusso anti zampa d'elefante sul bordo a contatto piatto (Z=0)
        bottom_edges = adapter.edges().filter_by(Axis.Z, reverse=True)
        # Seleziona il cerchio perimetrale esterno sul piano Z=0
        outer_bottom_edge = [
            e for e in bottom_edges
            if abs(e.center().Z) < 0.01 and e.length > (3.14 * config.BOTTOM_OUTER_D * 0.9)
        ]
        if outer_bottom_edge:
            chamfer(outer_bottom_edge, length=config.CHAMFER_BED)

    return adapter.part

def export_artifacts(output_dir: Path = Path("output")):
    """Genera ed esporta i file STEP e STL."""
    output_dir.mkdir(parents=True, exist_ok=True)
    part = create_adapter()

    step_path = output_dir / "esun_adapter.step"
    stl_path = output_dir / "esun_adapter.stl"

    export_step(part, str(step_path))
    export_stl(part, str(stl_path))
    print(f"Esportati con successo:\n  - {step_path}\n  - {stl_path}")

if __name__ == "__main__":
    export_artifacts()
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
.venv/bin/python -m pytest checks/check_fit.py -v
```
Expected: `2 passed in 0.XX s`.

- [ ] **Step 5: Test isolated script export**

Run:
```bash
.venv/bin/python src/generate_adapter.py
```
Expected: Outputs `output/esun_adapter.step` and `output/esun_adapter.stl`.
Check: `ls -lh output/` verifies existence and non-zero size.

- [ ] **Step 6: Commit**

```bash
git add src/generate_adapter.py checks/check_fit.py
git commit -m "feat: implement parametric CAD model with build123d and STEP/STL export"
```

---

### Task 4: Bambu Studio 3MF Patching and Automated Build Pipeline

**Files:**
- Create: `src/patch_3mf.py`
- Create: `build.sh`

**Interfaces:**
- Consumes: `output/esun_adapter.stl`
- Produces: `output/esun_adapter.3mf` with airtight PLA slice settings.

- [ ] **Step 1: Implement src/patch_3mf.py**

Create `src/patch_3mf.py`:
```python
"""
src/patch_3mf.py
Modifica le impostazioni di processo contenute nel 3MF generato da Bambu Studio CLI
per impostare perimetri e riempimento ottimali per tenuta stagna in PLA.
"""

import sys
import zipfile
from pathlib import Path

def patch_3mf_settings(input_3mf: Path, output_3mf: Path):
    """
    Scompatta il 3MF, modifica Metadata/project_settings.config e ricompatta.
    """
    settings_key = "Metadata/project_settings.config"
    settings_override = {
        "wall_loops": "5",
        "sparse_infill_density": "100%",
        "sparse_infill_pattern": "rectilinear",
        "top_shell_layers": "6",
        "bottom_shell_layers": "6",
        "elefant_foot_compensation": "0",
        "seam_position": "aligned",
    }

    temp_zip = input_3mf.with_suffix(".tmp.zip")

    with zipfile.ZipFile(input_3mf, "r") as zin:
        with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == settings_key:
                    content = data.decode("utf-8")
                    lines = content.splitlines()
                    new_lines = []
                    found_keys = set()
                    for line in lines:
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k_strip = k.strip()
                            if k_strip in settings_override:
                                new_lines.append(f"{k_strip} = {settings_override[k_strip]}")
                                found_keys.add(k_strip)
                                continue
                        new_lines.append(line)
                    # Aggiunge chiavi non trovate
                    for k, v in settings_override.items():
                        if k not in found_keys:
                            new_lines.append(f"{k} = {v}")
                    data = "\n".join(new_lines).encode("utf-8")
                zout.writestr(item, data)

    temp_zip.replace(output_3mf)
    print(f"File 3MF patchato con successo in {output_3mf}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python src/patch_3mf.py <input.3mf> <output.3mf>")
        sys.exit(1)
    patch_3mf_settings(Path(sys.argv[1]), Path(sys.argv[2]))
```

- [ ] **Step 2: Implement build.sh**

Create `build.sh`:
```bash
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
```
Make `build.sh` executable:
```bash
chmod +x build.sh
```

- [ ] **Step 3: Run build.sh end-to-end**

Run:
```bash
./build.sh
```
Expected:
1. `pytest` executes and passes all tests.
2. `esun_adapter.step` and `esun_adapter.stl` generated in `output/`.
3. Bambu Studio CLI compiles `output/esun_adapter.3mf`.
4. `patch_3mf.py` applies the PLA airtight profile.
5. Exit code 0.

- [ ] **Step 4: Commit**

```bash
git add src/patch_3mf.py build.sh
git commit -m "feat: add Bambu Studio 3MF patcher and automated build pipeline"
```

---

### Task 5: Final Verification and Clean Handoff

**Files:**
- Modify: `docs/measurements.md` (record generated file sizes and hashes)
- Verify: Full pipeline `./build.sh`
- Check: Git status and privacy compliance

- [ ] **Step 1: Run full verification suite**

Run:
```bash
./build.sh
```
Verify:
```bash
ls -lh output/
```
Expected files:
- `output/esun_adapter.step` (~30-60 KB)
- `output/esun_adapter.stl` (~50-150 KB)
- `output/esun_adapter.3mf` (valid zip archive with `Metadata/project_settings.config`)

- [ ] **Step 2: Inspect 3MF patched settings**

Run:
```bash
unzip -p output/esun_adapter.3mf Metadata/project_settings.config | grep -E "wall_loops|sparse_infill_density|elefant_foot_compensation"
```
Expected output:
```
wall_loops = 5
sparse_infill_density = 100%
elefant_foot_compensation = 0
```

- [ ] **Step 3: Check privacy and git status**

Run:
```bash
git status
git log --oneline
```
Ensure all files are committed or cleanly ignored in `.gitignore`, no absolute home paths or personal emails in repository tracking.
