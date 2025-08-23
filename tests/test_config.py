from sid.config_loader import load_config

def test_load():
    cfg = load_config("configs/sid.yaml")
    assert "modules" in cfg
