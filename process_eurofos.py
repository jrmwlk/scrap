
import json
from collections import defaultdict

with open("eurofos.json") as f:
    data = json.load(f)

shifts = ["S1", "S2", "S3", "JV"]
parc = {shift: {"renfort": 0, "total": 0} for shift in shifts}
latest_entries = {}

for entry in data:
    shift = entry["shift"]
    zone = entry["zone"]
    parc[shift]["total"] += 1
    key = (entry["date"], shift, zone)
    latest_entries[key] = entry

for (_, shift, _), _ in latest_entries.items():
    parc[shift]["renfort"] += 1

output = {
    "date": data[0]["date"] if data else "",
    "parc": parc
}

with open("eurofos.json", "w") as f:
    json.dump(output, f, indent=2)
