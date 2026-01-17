import json
import math
import numpy as np

with open("JSONNAME.json", "r", encoding="utf-8") as f:
    data = json.load(f)

tally = []
index = 0

for i in range(len(data)):

    if len(data[i]["battles"]) != 2:
        data[i]["time"] = float("nan")
        continue

    index += 1

    detection_plane = 0
    detection_noplane = 0
    dogfight_single = 0
    dogfight_double = 0
    AACI = 0
    otorp = 0
    single = 0
    DA = 0
    cvshell = 0
    ctorp = 0
    yasen = 0
    nzci = 0
    gunci = 0

    for j in range(2):
        battle = data[i]["battles"][j]["data"]

        detection = battle["api_search"][0]
        if 1 <= detection <= 4:
            detection_plane += 1
        elif detection == 5:
            detection_noplane += 1

        if sum(battle["api_stage_flag"][1:3]) != 0:
            stage1 = battle["api_kouku"]["api_stage1"]
            if stage1["api_f_count"] != 0 and stage1["api_e_count"] != 0:
                dogfight_double += 1
            else:
                dogfight_single += 1

            if battle["api_stage_flag"][1] == 1:
                if "api_air_fire" in battle["api_kouku"].get("api_stage2", {}):
                    AACI += 1

        if battle["api_opening_flag"] == 1:
            otorp += 1

        # First shelling
        hougeki1 = battle["api_hougeki1"]
        single += len(hougeki1["api_at_list"])

        for k in range(len(hougeki1["api_at_list"])):
            if hougeki1["api_at_eflag"][k] == 1:
                ship_id = battle["api_ship_ke"][hougeki1["api_at_list"][k]]
                if ship_id == 1528:
                    cvshell += 1
                    single -= 1

            if hougeki1["api_at_type"][k] == 2:
                DA += 1
                single -= 1

        # Second shelling
        if battle["api_hourai_flag"][1] == 1:
            hougeki2 = battle["api_hougeki2"]
            single += len(hougeki2["api_at_list"])

            for k in range(len(hougeki2["api_at_list"])):
                if hougeki2["api_at_eflag"][k] == 1:
                    ship_id = battle["api_ship_ke"][hougeki2["api_at_list"][k]]
                    if ship_id == 1528:
                        cvshell += 1
                        single -= 1

                if hougeki2["api_at_type"][k] == 2:
                    DA += 1
                    single -= 1

        if battle["api_hourai_flag"][3] == 1:
            ctorp += 1

        # Night battle
        yasen_data = data[i]["battles"][j].get("yasen", {})
        if yasen_data:
            yasen += 1
            hougeki_y = yasen_data["api_hougeki"]
            single += len(hougeki_y["api_at_list"])

            for k in range(len(hougeki_y["api_at_list"])):
                if hougeki_y["api_at_eflag"][k] == 1:
                    ship_id = battle["api_ship_ke"][hougeki_y["api_at_list"][k]]
                    if ship_id == 1528:
                        cvshell += 1
                        single -= 1

                sp = hougeki_y["api_sp_list"][k]
                if sp == 1:
                    DA += 1
                    single -= 1
                elif sp == 200:
                    nzci += 1
                    single -= 1
                elif sp == 5:
                    gunci += 1
                    single -= 1

    baseline = 0

    animations = np.array([
        detection_plane,
        detection_noplane,
        dogfight_single,
        dogfight_double,
        AACI,
        single,
        DA,
        otorp,
        ctorp,
        cvshell,
        yasen,
        nzci,
        gunci
    ])

    time = baseline + np.dot(
        np.array([5.1, 4.0, 8.4, 11.5, 3.2, 1.7, 2.8,
                  3.5, 5.3, 3.7, 6.0, 8.3, 3.8]),
        animations
    )

    tally.append({
        "datano": i + 1,
        "detection_plane": detection_plane,
        "detection_noplane": detection_noplane,
        "dogfight_single": dogfight_single,
        "dogfight_double": dogfight_double,
        "AACI": AACI,
        "single": single,
        "DA": DA,
        "otorp": otorp,
        "ctorp": ctorp,
        "cvshell": cvshell,
        "yasen": yasen,
        "nzci": nzci,
        "gunci": gunci,
        "time": time
    })

# Statistics
times = np.array([t["time"] for t in tally])

avgtime = np.mean(times)
time_std = np.std(times)

avg_detection_plane = np.mean([t["detection_plane"] for t in tally])
avg_detection_noplane = np.mean([t["detection_noplane"] for t in tally])
avg_dogfight_single = np.mean([t["dogfight_single"] for t in tally])
avg_dogfight_double = np.mean([t["dogfight_double"] for t in tally])
avg_AACI = np.mean([t["AACI"] for t in tally])
avg_single = np.mean([t["single"] for t in tally])
avg_DA = np.mean([t["DA"] for t in tally])
avg_otorp = np.mean([t["otorp"] for t in tally])
avg_ctorp = np.mean([t["ctorp"] for t in tally])
avg_cvshell = np.mean([t["cvshell"] for t in tally])
avg_yasen = np.mean([t["yasen"] for t in tally])
avg_nzci = np.mean([t["nzci"] for t in tally])
avg_gunci = np.mean([t["gunci"] for t in tally])

print("Average time:", avgtime)
print("Time std:", time_std)

print("Average counts:")
print("detection_plane:", avg_detection_plane)
print("detection_noplane:", avg_detection_noplane)
print("dogfight_single:", avg_dogfight_single)
print("dogfight_double:", avg_dogfight_double)
print("AACI:", avg_AACI)
print("single:", avg_single)
print("DA:", avg_DA)
print("otorp:", avg_otorp)
print("ctorp:", avg_ctorp)
print("cvshell:", avg_cvshell)
print("yasen:", avg_yasen)
print("nzci:", avg_nzci)

print("gunci:", avg_gunci)
