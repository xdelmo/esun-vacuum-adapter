# Adattatore per aspirapolvere e buste sottovuoto eSUN — Design

Data: 2026-11-14 · Stato: approvato dall'utente (2026-11-14)

## Intento

L'utente necessita di un adattatore rigido da stampare in 3D in PLA per collegare un aspirapolvere alle buste sottovuoto per filamento 3D marca eSUN (eVacuum bags). L'aspiratore presenta un beccuccio cilindrico sporgente con diametro esterno di 20 mm e altezza di 5 mm. La busta eSUN presenta una valvola circolare di diametro 30 mm con rilievo di 1 mm. L'adattatore accoppia entrambi i terminali tramite innesto femmina, consentendo un'aspirazione rapida, stabile ed ermetica senza perdite di carico.

Successo = l'adattatore calza saldamente sul beccuccio dell'aspiratore (Ø 20 mm, profondità 5 mm), si appoggia a battuta piana sulla valvola eSUN (Ø 30 mm, profondità 1 mm), non richiede supporti di stampa, è a tenuta d'aria stagna in depressione ed è gestito con la stessa pipeline e struttura di `~/development/hobbies/bosch-gl40-bag-adapter/`.

## Obiettivi

- Progettazione CAD procedurale e parametrica con Python `build123d`.
- Due innesti femmina (cavità a bicchiere coassiali):
  1. **Lato Aspiratore**: cavità cilindrica interna Ø 20.2 mm (+0.2 mm gioco FDM), profondità 5.0 mm, con raccordo interno autoportante a 45° verso il foro centrale.
  2. **Lato Busta eSUN**: campana femmina interna Ø 30.2 mm (+0.2 mm gioco FDM), profondità 1.0 mm, con battuta piana anulare di 8.1 mm di larghezza per la sigillatura diretta a contatto contro la superficie della valvola del sacchetto.
- Condotto centrale continuo passante liscio a Ø 14.0 mm (portata d'aria ottimale, senza griglie interne).
- Geometria autoportante al 100% senza supporti (altezza complessiva 20.0 mm, sbalzi max 45°).
- Nuovo repository in `~/development/hobbies/esun-vacuum-adapter/` con l'architettura standard del portfolio:
  - `CLAUDE.md` e symlink `AGENTS.md`
  - `src/config.py` con quote parametriche verificate e tolleranze FDM
  - `src/generate_adapter.py` basato su `build123d` con export STEP e STL in `output/`
  - `checks/check_fit.py` con suite `pytest`
  - `build.sh` per orchestrazione: test → CAD → Bambu Studio CLI → patch 3MF
  - `src/patch_3mf.py` per garantire 100% infill / 5 perimetri in PLA
  - `docs/` con contesto hardware e registro misurazioni

## Non-obiettivi

- Nessuna guarnizione ausiliaria in TPU o O-ring aggiuntivo (tenuta piana diretta rigida in PLA indotta dalla depressione).
- Nessuna griglia interna a crociera (il foro centrale passante resta liscio e aperto).
- Compatibilità con valvole rettangolari o sacchetti per abiti con diametro > 30 mm.

## Anti-obiettivi (fallisce anche se "funziona")

- Trafilamenti d'aria attraverso i perimetri o tra i layer sotto forte depressione.
- Tolleranza troppo stretta che impedisce l'inserimento sul beccuccio da 20 mm o deforma l'ugello dell'aspiratore.
- Superficie di tenuta sulla valvola irregolare o con difetti di planarità dovuti a ponti o supporti.
- Flessione o collasso radiale delle pareti sotto il vuoto continuo.

## Vincoli

- **Stampante**: Bambu Lab A1 mini (piatto 180×180×180 mm, ugello 0.4 mm).
- **Materiale**: Generic PLA (profilo *0.16mm Optimal @BBL A1M*).
- **Orientamento sul piatto**: Faccia lato aspiratore appoggiata sul piatto PEI (Z=0); faccia lato campana eSUN rivolta in alto a Z=20 mm.
- **Spessore minimo parete**: $\ge 2.4\text{ mm}$ in qualsiasi sezione radiale.
- **Tolleranze FDM (PLA)**:
  - Gioco innesto aspiratore: `+0.2 mm` sul diametro (nominale interno 20.2 mm).
  - Gioco campana valvola eSUN: `+0.2 mm` sul diametro (nominale interno 30.2 mm).
  - Smusso anti zampa d'elefante a contatto piatto: 0.4 mm a 45°.

## Approcci considerati

- **Approccio 1 (Raccordo Conico Diretto e Compatto) — Scelto**:
  Corpo conico continuo a 45° tra la base Ø 25 mm e la testa Ø 35 mm. Monolitico, compatto (20 mm di altezza totale), stampa senza supporti, pareti massicce e rigide.
- **Approccio 2 (Corpo Allungato con Grip Esterno)**:
  Presa migliorata ma altezza maggiore (30 mm) e materiale superfluo.
- **Approccio 3 (Ultra-Low-Profile a Flangia Piatta)**:
  Altezza 8 mm, ma transizione d'aria a spigolo vivo, minor rigidità strutturale e presa manuale difficile.

## Specifiche Geometriche Dettagliate

### Sistema di Coordinate
- **Origine (X=0, Y=0)**: Asse centrale di rivoluzione / simmetria del condotto d'aria.
- **Piano Z=0**: Faccia inferiore a contatto con il piatto di stampa (bordo esterno lato aspiratore).
- **Asse +Z**: Diretto verticalmente verso l'alto lungo la direzione di crescita dei layer.

### Quote Parametriche (`src/config.py`)
- `VACUUM_NOZZLE_D = 20.0`: Diametro esterno nominale del beccuccio aspiratore.
- `VACUUM_NOZZLE_H = 5.0`: Altezza nominale del beccuccio aspiratore.
- `VALVE_OUTER_D = 30.0`: Diametro esterno nominale della valvola eSUN.
- `VALVE_RECESS_DEPTH = 1.0`: Profondità nominale dell'incavo per la valvola.
- `FIT_CLEARANCE = 0.2`: Gioco radiale/diametrale per accoppiamenti FDM in PLA.
- `AIR_BORE_D = 14.0`: Diametro del condotto centrale passante.
- `TOTAL_H = 20.0`: Altezza complessiva del pezzo.
- `BOTTOM_OUTER_D = 25.0`: Diametro esterno base (spessore parete 2.4 mm).
- `TOP_OUTER_D = 35.0`: Diametro esterno testa (spessore parete 2.4 mm).
- `CHAMFER_BED = 0.4`: Smusso anti zampa d'elefante a Z=0.

### Dettaglio Costruttivo (da Z=0 a Z=20 mm)
1. **Z = 0.0 → Z = 5.0 mm (Bicchiere Aspiratore)**:
   - Esterno: cilindro Ø 25.0 mm.
   - Interno: cavità cilindrica Ø 20.2 mm.
2. **Z = 5.0 → Z = 8.1 mm (Transizione Interna Autoportante)**:
   - Esterno: cono che sale da Ø 25.0 mm con pendenza 45°.
   - Interno: tronco di cono a 45° che converge da Ø 20.2 mm al foro centrale Ø 14.0 mm.
3. **Z = 8.1 → Z = 19.0 mm (Condotto Centrale e Cono Esterno)**:
   - Esterno: cono continuo che raggiunge Ø 35.0 mm a Z = 15.0 mm e prosegue cilindrico fino a Z = 20.0 mm.
   - Interno: foro verticale continuo Ø 14.0 mm.
4. **Z = 19.0 → Z = 20.0 mm (Campana Valvola eSUN)**:
   - Esterno: cilindro Ø 35.0 mm.
   - Interno: incavo cilindrico Ø 30.2 mm, fondo piano a Z = 19.0 mm formante la superficie di tenuta ad anello (larghezza radiale 8.1 mm).

## Struttura del Repository e File

```
~/development/hobbies/esun-vacuum-adapter/
├── CLAUDE.md                   # Istruzioni progetto, convenzioni e regole AGY
├── AGENTS.md -> CLAUDE.md      # Symlink relativo
├── README.md                   # Documentazione di sintesi e istruzioni
├── requirements.txt            # build123d>=0.11, pytest
├── build.sh                    # Pipeline automatica
├── .gitignore                  # Esclusioni git standard
├── src/
│   ├── config.py               # Parametri dimensionali e tolleranze
│   ├── generate_adapter.py     # Costruzione CAD build123d ed export STEP/STL
│   └── patch_3mf.py            # Patch parametri PLA (100% infill, wall loops)
├── checks/
│   └── check_fit.py            # Test geometrici con pytest
├── docs/
│   ├── hardware_context.md     # Specifiche fisiche aspiratore e busta eSUN
│   ├── measurements.md         # Registro quote calibro vs CAD
│   └── superpowers/specs/      # Specifiche di design
└── output/                     # File generati (.step, .stl, .3mf)
```

## Stampabilità e Parametri di Stampa (PLA)

- **Wall loops**: 5 perimetri per eliminare porosità radiale.
- **Top / Bottom shell layers**: 6 strati solidi.
- **Infill**: 100% rettilineo / allineato.
- **Layer height**: 0.16 mm.
- **Supporti**: Disattivati (0 supporti, geometria 100% autoportante).
- **Compensazione zampa d'elefante slicer**: Disattivata (sostituita dallo smusso geometrico CAD a 45° di 0.4 mm).

## Piano di Verifica

1. **Test automatici unitari (`pytest checks/check_fit.py`)**:
   - Spessore minimo parete $\ge 2.4\text{ mm}$ ovunque.
   - Diametri: `VALVE_RECESS_D > VACUUM_SOCKET_D > AIR_BORE_D`.
   - Altezza totale rigorosamente pari a 20.0 mm.
   - Angoli di sbalzo $\le 45^\circ$.
   - Geometria chiusa manifold.
2. **Pipeline di build (`./build.sh`)**:
   - Generazione priva di errori di `output/esun_adapter.step` e `output/esun_adapter.stl`.
   - Generazione di `output/esun_adapter.3mf` con Bambu Studio CLI e applicazione patch PLA.
3. **Verifica fisica**:
   - Inserimento a frizione sul beccuccio dell'aspiratore.
   - Accoppiamento con la valvola della busta eSUN.
   - Prova del vuoto ed estrazione dell'aria dalla busta fino al blocco completo della depressione.
