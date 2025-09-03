import hashlib

def heuristic_analysis(content: bytes, filename: str) -> dict:
    sha256 = hashlib.sha256(content).hexdigest()
    result = {
        "sha256": sha256,
        "classification": "limpio",
        "confidence": 90,
        "rules_triggered": []
    }

    # Heurística 1: extensiones sospechosas
    if filename.lower().endswith((".exe", ".bat", ".vbs", ".scr")):
        result["classification"] = "sospechoso"
        result["confidence"] = 65
        result["rules_triggered"].append("extension_sospechosa")

    # Heurística 2: tamaño del archivo
    if len(content) > 10 * 1024 * 1024:  # >10MB
        result["classification"] = "sospechoso"
        result["confidence"] = max(result["confidence"], 70)
        result["rules_triggered"].append("archivo_demasiado_grande")

    # Heurística 3: cadenas sospechosas
    suspicious_patterns = [b"powershell", b"eval(", b"base64", b"cmd.exe"]
    for pattern in suspicious_patterns:
        if pattern in content.lower():
            result["classification"] = "malware"
            result["confidence"] = 95
            result["rules_triggered"].append(f"patron_{pattern.decode('latin1')}")

    return result
