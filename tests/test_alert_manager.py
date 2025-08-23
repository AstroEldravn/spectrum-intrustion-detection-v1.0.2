from sid.alert_manager import AlertManager

def test_emit():
    am = AlertManager([{"type":"console"}])
    am.emit("INFO","test","hello",{"k":1})
