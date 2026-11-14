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
