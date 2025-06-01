
import json

with open("eurofos_raw.json") as f:
    data = json.load(f)

# Structure de sortie
result = {
    "date": data[0]["date"] if data else "",
    "parc": {
        "S1": {"renfort": 0, "total": 0},
        "S2": {"renfort": 0, "total": 0},
        "S3": {"renfort": 0, "total": 0},
        "JV": {"renfort": 0, "total": 0},
        "JD": {"renfort": 0, "total": 0}
    }
}

for entry in data:
    zone = entry.get("zone", "").upper()
    shift = entry.get("shift", "").upper()
    type_ = entry.get("type", "").upper()
    lignes = entry.get("lignes", [])

    # On ne garde que les zones PARC ou CAVALIER (ou les 2 ensemble)
    if "PARC" in zone and "CAVALIER" in zone and shift in result["parc"] and type_ == "STR":
        if len(lignes) >= 3:
            total = int(lignes[0])  # première ligne = total
            renfort = int(lignes[2])  # troisième ligne = renfort
            result["parc"][shift]["total"] += total
            result["parc"][shift]["renfort"] += renfort

with open("eurofos.json", "w") as f:
    json.dump(result, f, indent=2)
