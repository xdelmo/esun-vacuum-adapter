"""
src/generate_adapter.py
Modellazione CAD procedurale dell'adattatore per aspiratore e buste eSUN con build123d.
"""

import sys
from pathlib import Path

# Assicura che la root del progetto sia in sys.path se eseguito direttamente come script
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from build123d import (
    Align,
    BuildPart,
    BuildSketch,
    Circle,
    Cone,
    Location,
    Locations,
    Mode,
    Plane,
    chamfer,
    export_step,
    export_stl,
    extrude,
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

        # Transizione tronco-conica da Z=5.0 a Z=10.0 (sale da 25mm a 35mm di diametro esterno)
        cone_h = (config.TOP_OUTER_D - config.BOTTOM_OUTER_D) / 2.0  # 5.0 mm di altezza a 45 gradi
        cone_z = config.VACUUM_NOZZLE_H
        with Locations(Location((0, 0, cone_z))):
            Cone(
                bottom_radius=config.BOTTOM_OUTER_D / 2.0,
                top_radius=config.TOP_OUTER_D / 2.0,
                height=cone_h,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )

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
        extrude(amount=config.VACUUM_NOZZLE_H, mode=Mode.SUBTRACT)

        # b) Raccordo conico interno a 45 gradi da Z=5.0 a Z=5.0 + taper_h (da vacuum_socket_d a AIR_BORE_D)
        with Locations(Location((0, 0, config.VACUUM_NOZZLE_H))):
            Cone(
                bottom_radius=vacuum_socket_d / 2.0,
                top_radius=config.AIR_BORE_D / 2.0,
                height=taper_h,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )

        # c) Condotto centrale passante Ø 14mm continuo da Z=5.0 + taper_h fino a Z=19.0
        with BuildSketch(Plane.XY.offset(config.VACUUM_NOZZLE_H + taper_h)):
            Circle(radius=config.AIR_BORE_D / 2.0)
        extrude(
            amount=config.TOTAL_H - (config.VACUUM_NOZZLE_H + taper_h),
            mode=Mode.SUBTRACT,
        )

        # d) Campana femmina valvola eSUN a Z=19.0 fino a Z=20.0
        recess_z = config.TOTAL_H - config.VALVE_RECESS_DEPTH
        with BuildSketch(Plane.XY.offset(recess_z)):
            Circle(radius=valve_recess_d / 2.0)
        extrude(amount=config.VALVE_RECESS_DEPTH, mode=Mode.SUBTRACT)

        # 3. Smusso anti zampa d'elefante sul bordo a contatto piatto (Z=0)
        bottom_edges = adapter.edges()
        outer_bottom_edge = [
            e
            for e in bottom_edges
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
