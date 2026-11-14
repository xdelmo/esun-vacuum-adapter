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

---

## Metriche Geometriche e Fisiche del Pezzo (CAD)

- **Volume CAD solido**: 10.920 mm³ (10,92 cm³)
- **Massa stimata PLA (100% infill / densità 1,24 g/cm³)**: ~11,6 g – 13,5 g
- **Tempo stimato di stampa**: ~25 – 30 min (Bambu Lab A1 mini, profilo 0.16mm Optimal)
- **Supporti di stampa**: 0 (geometria 100% autoportante con sbalzi ≤ 45°)
- **Spessore parete minimo**: 2,40 mm continuo (superiore alla soglia di sicurezza di 2,0 mm)

---

## Verifica Artefatti di Build (Release)

I seguenti file sono generati tramite la pipeline automatica `./build.sh`:

| File | Dimensione | SHA-256 Checksum | Descrizione / Formato |
| :--- | :--- | :--- | :--- |
| `output/esun_adapter.step` | 26,5 KB (26.546 byte) | `45770c5422c30004ed6ebcf7ccd15414a221ad9b94924269e9f1253a9e34b8f6` | Modello CAD B-Rep conforme ISO 10303-21 |
| `output/esun_adapter.stl` | 162 KB (165.884 byte) | `3f186b91e3b00fa9b768e5e9db121c88a7423e0bae55da542b1607bb539c32f5` | Mesh triangolare binaria (3.316 facce, manifold) |
| `output/esun_adapter.3mf` | 54,5 KB (55.808 byte) | `b57869ce7a45832b3a385534b208f08cda5e478ecc23c6f6fb38a405eec6ec63` | Archivio Bambu Studio pronto per la stampa su A1 mini |

---

## Parametri di Stampa Verificati nel Profilo 3MF

Verifica effettuata tramite ispezione di `Metadata/project_settings.config` all'interno dell'archivio `.3mf`:

- `wall_loops = 5`: Perimetri multipli per eliminare porosità radiale sotto vuoto spinto.
- `sparse_infill_density = 100%`: Riempimento pieno continuo per solidità monolitica.
- `sparse_infill_pattern = rectilinear`: Infill rettilineo/allineato per fusione isotropa.
- `top_shell_layers = 6`, `bottom_shell_layers = 6`: Chiusura solida alle estremità.
- `elefant_foot_compensation = 0`: Compensazione slicer disabilitata; zampa d'elefante prevenuta mediante smusso geometrico CAD a 45° (0,4 mm) sul bordo inferiore.
- `seam_position = aligned`: Cucitura allineata per evitare disallineamenti superficiali.

---

## Esito Verifiche Geometriche FDM

- **Suite pytest (`checks/check_fit.py`)**: 2/2 test superati (100% pass rate).
- **Controllo interferenze e accoppiamenti**:
  - Innesto beccuccio aspiratore: femmina Ø 20,2 mm (+0,2 mm gioco) × 5,0 mm di profondità con transizione conica a 45°.
  - Campana eSUN: femmina Ø 30,2 mm (+0,2 mm gioco) × 1,0 mm con battuta piana anulare di larghezza 8,1 mm.
  - Foro centrale: Ø 14,0 mm passante liscio senza ostruzioni.
