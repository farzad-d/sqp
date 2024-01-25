import os


class WinPos:
    def __init__(self, window):
        window = window

        if os.path.isfile("g_data.conf"):
            with open("g_data.conf", "r") as file_r:
                window.geometry(file_r.read())
        else:
            window.geometry("400x400")

        def on_close():
            with open("g_data.conf", "w") as file_w:
                file_w.write(window.geometry())
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_close)
