from utils import WINDOW_ELEMENTS

def file_open():
    print("This is what file_open function does ...")

def file_close():
    print("This is what file_close function does ...")

def file_save():
    print("This is what file_save function does ...")

def file_quit():
    print("This is what file_quit function does ...")

def sound_load():
    print("This is what sound_load function does ...")

def text_properites():
    print("This is what text_properites function does ...")

def text_pointer():
    print("This is what text_pointer function does ...")

def test_aaa():
    print("This is what test_aaa function does ...")

def test_bbb():
    print("This is what test_bbb function does ...")

def test_ccc_xxx():
    print("This is what test_ccc_xxx function does ...")

def test_ccc_yyy_ttt():
    print("This is what test_ccc_yyy_ttt function does ...")

def test_ccc_yyy_jjj():
    print("This is what test_ccc_yyy_jjj function does ...")

def test_ccc_yyy_mmm():
    print("This is what test_ccc_yyy_mmm function does ...")

def test_bbb_lzlzlz():
    print("This is what test_bbb_lzlzlz function does")
def test_bbb_popopo():
    print("This is what test_bbb_popopo function does")

def test_empty():
    print("This is what test_empty function does ...")


def color_picker():
    print("This is what color_picker function does ...")
    WINDOW_ELEMENTS["cp_win"].is_open = True


MENU_STRUCTURE = {
    "File": {"function": None},
    "File/Open": {"function": file_open},
    "File/Close": {"function": file_close},
    "File/Save": {"function": file_save},
    "File/Quit": {"function": file_quit},
    "Sound": {"function": None},
    "Sound/Load": {"function": sound_load},
    "Text": {"function": None},
    "Text/Properties": {"function": text_properites},
    "Text/Pointer": {"function": text_pointer},
    "test": {"function": None},
    "test/aaa": {"function": test_aaa},
    "test/bbb": {"function": None},
    "test/bbb/lzlzlz": {"function": test_bbb_lzlzlz},
    "test/bbb/popopo": {"function": test_bbb_popopo},
    "test/cccccc": {"function": None},
    "test/cccccc/XXX": {"function": test_ccc_xxx},
    "test/cccccc/YYYYYY": {"function": None},
    "test/cccccc/YYYYYY/ttt": {"function": test_ccc_yyy_ttt},
    "test/cccccc/YYYYYY/jl": {"function": test_ccc_yyy_jjj},
    "test/cccccc/YYYYYY/mmmmmm": {"function": test_ccc_yyy_mmm},
    "color picker": {"function": color_picker},
}
