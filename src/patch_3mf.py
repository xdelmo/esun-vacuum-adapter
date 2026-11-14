"""
src/patch_3mf.py
Modifica le impostazioni di processo contenute nel 3MF generato da Bambu Studio CLI
per impostare perimetri e riempimento ottimali per tenuta stagna in PLA.
"""

import json
import sys
import zipfile
from pathlib import Path


def patch_3mf_settings(input_3mf: Path, output_3mf: Path):
    """
    Scompatta il 3MF, modifica Metadata/project_settings.config e ricompatta.
    Supporta sia il formato JSON (Bambu Studio moderno) sia key-value / INI.
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

    temp_zip = output_3mf.with_suffix(".tmp.zip")

    with zipfile.ZipFile(input_3mf, "r") as zin:
        with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == settings_key:
                    content = data.decode("utf-8")
                    try:
                        # Bambu Studio project_settings.config usa formato JSON
                        config_dict = json.loads(content)
                        for k, v in settings_override.items():
                            config_dict[k] = v
                        data = json.dumps(config_dict, indent=4).encode("utf-8")
                    except Exception:
                        # Fallback per formato key = value (INI)
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
