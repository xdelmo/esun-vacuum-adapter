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
FIT_CLEARANCE = 0.2             # Gioco diametrale per accoppiamenti FDM (+0.2 mm su Ø)
BOTTOM_OUTER_D = 25.0           # Diametro esterno base (lato piatto/aspiratore)
TOP_OUTER_D = 35.0              # Diametro esterno testa (lato campana eSUN)
CHAMFER_BED = 0.4               # Smusso anti zampa d'elefante sul piatto (Z=0)
