import json
import os
import random

#json stuff
def write_color_prefs(dir_path, prefs_file_name, app):
    """writes the color prefs. The file is saved ito the same folder as the
    sound fle."""
    """From app we should be able to grab all info necessary to fill the prefs in"""

    prefs_file_name = prefs_file_name + ".json"
    prefs_file_path = os.path.join(dir_path, prefs_file_name)
    print(prefs_file_path)

    marker_template = {"name": None,
                       "position_audio": None,
                       "position_text": None,
                       "color": [],
                       }
    prefs_template = {"audio_file": None,
                      "markers": None,
                      "text": {"font": None,
                               "size": None,
                               "text": ""
                               },
                      "color_samples": {
                          "00": (0, 0, 0),
                          "01": (0, 0, 0),
                          "02": (0, 0, 0),
                          "03": (0, 0, 0),
                          "04": (0, 0, 0),
                          "10": (0, 0, 0),
                          "11": (0, 0, 0),
                          "12": (0, 0, 0),
                          "13": (0, 0, 0),
                          "14": (0, 0, 0),
                          "20": (0, 0, 0),
                          "21": (0, 0, 0),
                          "22": (0, 0, 0),
                          "23": (0, 0, 0),
                          "24": (0, 0, 0),
                          "30": (0, 0, 0),
                          "31": (0, 0, 0),
                          "32": (0, 0, 0),
                          "33": (0, 0, 0),
                          "34": (0, 0, 0),
                          "40": (0, 0, 0),
                          "41": (0, 0, 0),
                          "42": (0, 0, 0),
                          "43": (0, 0, 0),
                          "44": (0, 0, 0)
                      }
}

    with open(prefs_file_path, "w") as file:
        json.dump(color_samples, file, indent=4)

def read_project_file(file_path):
    with open(file_path, "r") as project:
        project = json.load(project)
        return project

#sample json file:
color_samples = {
    "00": (126,141,12),
    "01": (242,85,207),
    "02": (47,92,123),
    "03": (120,57,164),
    "04": (250,50,73),
    "10": (150,104,220),
    "11": (249,125,197),
    "12": (186,122,160),
    "13": (125,1,176),
    "14": (2,55,227),
    "20": (15,2,132),
    "21": (22,152,137),
    "22": (8,40,106),
    "23": (22,182,125),
    "24": (70,249,111),
    "30": (253,255,203),
    "31": (137,195,96),
    "32": (240,128,16),
    "33": (57,100,234),
    "34": (123,84,97),
    "40": (106,141,173),
    "41": (123,36,166),
    "42": (17,152,160),
    "43": (139,83,64),
    "44": (235,195,35)
}
project_prefs = {
    "audio_file": "/home/fuku/PycharmProjects/Karaoke/misc_files/curt.mp3",
    "markers": {
        0 : {"name" : "marker_name",
            "position_audio" : "marker pos in samples",
            "position_text" : "pos in absolute pixels (before scaling)",
            "color": [0, 100, 0],
            },
        1 : {"name" : "marker_name",
            "position" : "marker pos in samples",
            "position_text" : "pos in absolute pixels (before scaling)",
            "color": [100, 0, 0],
            },
        2 : {"name" : "marker_name",
            "position" : "marker pos in samples",
            "position_text" : "pos in absolute pixels (before scaling)",
            "color": [0, 0, 100],
            }
    },
    "text": {
        "font": "text font",
        "size": 33
    },
    "color_samples": {
        "00": (0, 0, 0),
        "01": (0, 0, 0),
        "02": (0, 0, 0),
        "03": (0, 0, 0),
        "04": (0, 0, 0),
        "10": (0, 0, 0),
        "11": (0, 0, 0),
        "12": (0, 0, 0),
        "13": (0, 0, 0),
        "14": (0, 0, 0),
        "20": (0, 0, 0),
        "21": (0, 0, 0),
        "22": (0, 0, 0),
        "23": (0, 0, 0),
        "24": (0, 0, 0),
        "30": (0, 0, 0),
        "31": (0, 0, 0),
        "32": (0, 0, 0),
        "33": (0, 0, 0),
        "34": (0, 0, 0),
        "40": (0, 0, 0),
        "41": (0, 0, 0),
        "42": (0, 0, 0),
        "43": (0, 0, 0),
        "44": (0, 0, 0)
    }
}

read_project_file("/home/fuku/PycharmProjects/Karaoke/misc_files/project_file_sample_01.json")
# write_color_prefs("/home/fuku/PycharmProjects/Karaoke/misc_files/", "prefs_file", color_samples)

# for i in range(5):
#     for a in range(5):
#         print("{}{} : ({},{},{})".format(i, a, random.randint(0,255),
#                                          random.randint(0,255),
#                                          random.randint(0,255)))