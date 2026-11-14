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
