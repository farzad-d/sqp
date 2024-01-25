import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import ttkthemes
import math
import os
import pandas
import csv

import save_last_win_pos
import tt_calculator


# ---------------------------- CONSTANT DATA ------------------------------- #
SMALL_SQUARE_COLOR = "#203239"
LARGE_SQUARE_COLOR = "#2B2B2B"
SIDES_COLOR = "#80ED99"
SETTINGS_SQUARE_COLOR = "Silver"
FONT_NAME = "Tahoma"

# ---------------------------- VARIABLE DATA ------------------------------- #
work_time = 30
short_break_time = 5
long_break_time = 20

title = "Timer Status"
color = "Gray90"
section = 0
timer = 0
counter = 0
last_recorded_time = 0
squares = 0
bottom_side_step = 0
right_side_step = 0
top_side_step = 0
left_side_step = 0
total_work_time = 0
skip = False
reset_question_enable = False

# ---------------------------- MODE SELECTOR ------------------------------- #


def start_pause_reset(e=None):
    if section == 0:
        start_timer()
    elif counter:
        pause_timer()
    elif not counter:
        resume_timer()


# ---------------------------- WINDOW ICONIFY/DEICONIFY ------------------------------- #
def popup_window():
    window.deiconify()
    window.attributes("-topmost", True)
    window.attributes("-topmost", False)


def minimize_window(e=None):
    window.iconify()


# ---------------------------- SAVE AND LOAD SETTINGS ------------------------------- #
def save_settings():
    data = {
        "work_time": default_work_num.get(),
        "short_break": default_short_break_num.get(),
        "long_break": default_long_break_num.get(),
    }
    df = pandas.DataFrame.from_dict(data, orient="index")
    df.to_csv("s_data.csv")


def load_settings():
    global work_time, short_break_time, long_break_time

    with open("s_data.csv") as file:
        csv_data = list(csv.reader(file))
        work_time = int(csv_data[1][1])
        short_break_time = int(csv_data[2][1])
        long_break_time = int(csv_data[3][1])


def save_button_commands():
    if work_time != int(default_work_num.get()):
        confirm_reset = tkinter.messagebox.askyesno(
            title="Save and Reset",
            message="By changing the work time all of "
            "your data will be reset, "
            "\nDo you continue?",
        )
        if confirm_reset:
            save_settings()
            load_settings()
            save_button["state"] = tk.DISABLED
            timer_reset()
        else:
            default_work_num.set(str(work_time))
            save_button_state()
    else:
        save_settings()
        load_settings()
        save_button["state"] = tk.DISABLED


def create_settings_file():
    open("s_data.csv", "w")
    data = {
        "work_time": work_time,
        "short_break": short_break_time,
        "long_break": long_break_time,
    }
    df = pandas.DataFrame.from_dict(data, orient="index")
    df.to_csv("s_data.csv")


# Check settings directory --------------------------------------------------
if os.path.exists("s_data.csv"):
    load_settings()
else:
    create_settings_file()
    load_settings()


# Save button disable/enable --------------------------------------------------
def save_button_state():
    load_settings()
    if (
        work_time != int(default_work_num.get())
        or short_break_time != int(default_short_break_num.get())
        or long_break_time != int(default_long_break_num.get())
    ):
        save_button["state"] = "normal"
    else:
        save_button["state"] = tk.DISABLED


# ---------------------------- SAVE AND LOAD TIMER ------------------------------- #
def save_timer():
    timer_data = {
        "last_recorded_time": last_recorded_time,
        "section": section,
        "title": title,
        "color": color,
        "counter": counter,
        "timer": timer,
        "squares": squares,
        "bottom_side_step": bottom_side_step,
        "right_side_step": right_side_step,
        "top_side_step": top_side_step,
        "left_side_step": left_side_step,
        "total_work_time": total_work_time,
    }
    df = pandas.DataFrame.from_dict(timer_data, orient="index")
    df.to_csv("t_data.csv")


def load_timer():
    global last_recorded_time, section, title, color, counter, timer, squares, bottom_side_step, right_side_step, top_side_step, left_side_step, total_work_time

    with open("t_data.csv") as file:
        csv_data = list(csv.reader(file))
        last_recorded_time = int(csv_data[1][1])
        section = int(csv_data[2][1])
        title = csv_data[3][1]
        color = csv_data[4][1]
        counter = int(csv_data[5][1])
        timer = csv_data[6][1]
        squares = int(csv_data[7][1])
        bottom_side_step = float(csv_data[8][1])
        right_side_step = float(csv_data[9][1])
        top_side_step = float(csv_data[10][1])
        left_side_step = float(csv_data[11][1])
        total_work_time = int(csv_data[12][1])

    canvas.coords(bottom_side, 388, 394, 388 - bottom_side_step, 394)
    canvas.coords(right_side, 394, 12, 394, right_side_step + 12)
    canvas.coords(top_side, 12, 6, top_side_step + 12, 6)
    canvas.coords(left_side, 6, 388, 6, 388 - left_side_step)

    timer_status.config(text=title, fg=color)
    squares_label.config(text=f"{squares} ⬜")

    if title == "Short Break" or title == "Long Break":
        enable_skip()
    if counter == 0:
        pause_timer()
        count_min = math.floor(last_recorded_time / 60)
        count_sec = last_recorded_time % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        if count_min < 10:
            count_min = f"0{count_min}"
        timer_text.config(text=f"{count_min}:{count_sec}")
    else:
        resume_timer()


# ---------------------------- TIMER RESET ------------------------------- #
def timer_reset(e=None):
    global timer, last_recorded_time, section, title, color, counter, squares, bottom_side_step, right_side_step, top_side_step, left_side_step, total_work_time
    window.after_cancel(str(timer))
    timer = 0
    last_recorded_time = int(work_time) * 60
    section = 0
    title = "Timer Status"
    color = "Gray90"
    counter = 0
    squares = 0
    bottom_side_step = 0
    right_side_step = 0
    top_side_step = 0
    left_side_step = 0
    total_work_time = 0
    save_timer()
    load_timer()
    cancel_reset()
    skip_label.place_forget()
    window.bind("<space>", start_pause_reset)


def cancel_reset(e=None):
    global reset_question_enable
    reset_question_enable = False
    reset_confirm_label.place_forget()

    window.unbind("y")
    window.unbind("n")

    if title == "Work Time" or title == "Timer Status":
        disable_skip()
    else:
        enable_skip()


def ask_for_reset(e=None):
    global reset_question_enable
    reset_question_enable = True

    disable_skip()
    reset_confirm_label.place(relx=0.5, rely=0.68, anchor="center")

    timer_text.bind("<Button-1>", timer_reset)
    reset_confirm_label.bind("<Button-1>", timer_reset)
    canvas.tag_bind(timer_frame, "<Button-1>", timer_reset)

    timer_text.bind("<Button-3>", cancel_reset)
    reset_confirm_label.bind("<Button-3>", cancel_reset)
    canvas.tag_bind(timer_frame, "<Button-3>", cancel_reset)

    window.bind("y", timer_reset)
    window.bind("n", cancel_reset)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer(e=None):
    global section, title, color, skip, counter, total_work_time
    if section == 0:
        counter = 1
    section += 1
    skip = False

    work_sec = math.floor(work_time * 60)
    short_break_sec = math.floor(short_break_time * 60)
    long_break_sec = math.floor(long_break_time * 60)

    canvas.itemconfig(timer_frame, outline="#2155CD")

    if section % 8 == 0:
        title = "Long Break"
        color = "#FF4C29"
        count_down(long_break_sec)
        timer_status.config(text=title, fg=color)
        enable_skip()
        total_work_time += work_time
    elif section % 2 == 0:
        title = "Short Break"
        color = "#FFB830"
        count_down(short_break_sec)
        timer_status.config(text=title, fg=color)
        enable_skip()
        total_work_time += work_time
    else:
        title = "Work Time"
        color = SIDES_COLOR
        timer_status.config(text=title, fg=color)
        count_down(work_sec)
        disable_skip()
        if section > 1:
            pause_timer()


# ---------------------------- PAUSE AND RESUME ------------------------------- #
def pause_timer(e=None):
    global counter
    counter = 0
    if title == "Work Time":
        timer_status.config(fg="Gray90")
    if title == "Timer Status":
        canvas.itemconfig(timer_frame, outline="Gray")
    else:
        canvas.itemconfig(timer_frame, outline="#C93838")
    window.bind("<space>", start_pause_reset)
    save_timer()


def resume_timer(e=None):
    global counter
    counter = 1
    if title == "Work Time":
        timer_status.config(fg=SIDES_COLOR)
    canvas.itemconfig(timer_frame, outline="#2155CD")
    window.bind("<space>", start_pause_reset)
    count_down(last_recorded_time)


# ---------------------------- SQUARES COMPLETE AND RESET ------------------------------- #
def square_complete(count):
    global squares
    # Entering section 8
    if long_break_time * 60 == count:
        squares += 1
        squares_label.config(text=f"{squares} ⬜")
    # End of section 8
    if count == 0:
        pause_timer()
        enable_skip()


def reset_square(e=None):
    global bottom_side_step, right_side_step, top_side_step, left_side_step, bottom_side, right_side, top_side, left_side, section, timer, last_recorded_time, section, title, color, counter

    bottom_side_step = 0
    right_side_step = 0
    top_side_step = 0
    left_side_step = 0
    canvas.coords(right_side, 0, 0, 0, 0)
    canvas.coords(left_side, 0, 0, 0, 0)
    canvas.coords(top_side, 0, 0, 0, 0)
    canvas.coords(bottom_side, 0, 0, 0, 0)

    section = 0
    disable_skip()
    timer = 0
    last_recorded_time = int(work_time) * 60
    section = 0
    title = "Timer Status"
    color = "Gray90"
    counter = 0
    canvas.itemconfig(timer_frame, outline="Gray")
    window.bind("<space>", start_pause_reset)
    save_timer()
    load_timer()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global last_recorded_time, timer, work_time, section, bottom_side_step, right_side_step, top_side_step, left_side_step, counter
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if skip:
        start_timer()
    elif counter:
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        if count_min < 10:
            count_min = f"0{count_min}"
        timer_text.config(text=f"{count_min}:{count_sec}")
        if count >= 0:
            timer = window.after(1000, count_down, count - 1)
            if work_time != count_min and int(count_sec) % 60 == 0:
                if section == 1:
                    save_timer()
                    top_side_step += 376 / int(work_time)
                    canvas.coords(top_side, 12, 6, top_side_step + 12, 6)
                elif section == 3:
                    save_timer()
                    right_side_step += 376 / int(work_time)
                    canvas.coords(right_side, 394, 12, 394, right_side_step + 12)
                elif section == 5:
                    save_timer()
                    bottom_side_step += 376 / int(work_time)
                    canvas.coords(bottom_side, 388, 394, 388 - bottom_side_step, 394)
                elif section == 7:
                    save_timer()
                    left_side_step += 376 / int(work_time)
                    canvas.coords(left_side, 6, 388, 6, 388 - left_side_step)

            last_recorded_time = count

            if section == 8:
                square_complete(count)

        else:
            popup_window()
            start_timer()


# ---------------------------- SKIP ------------------------------- #
def disable_skip():
    skip_label.place_forget()
    if reset_question_enable:
        command_shifter(timer_reset, cancel_reset)
    else:
        command_shifter(start_pause_reset, ask_for_reset)


def enable_skip():
    if section == 8 and last_recorded_time == 0:
        skip_and_next()
    else:
        normal_skip()


def command_shifter(btn1, btn2):
    skip_label.bind("<Button-1>", btn1)
    timer_text.bind("<Button-1>", btn1)
    canvas.tag_bind(timer_frame, "<Button-1>", btn1)

    skip_label.bind("<Button-3>", btn2)
    timer_text.bind("<Button-3>", btn2)
    canvas.tag_bind(timer_frame, "<Button-3>", btn2)


def normal_skip():
    if not reset_question_enable:
        window.bind("<space>", skip_timer)
        skip_label.place(relx=0.5, rely=0.68, anchor="center")
        skip_label.config(text=f"Left click or Space\nto skip the break")
        command_shifter(skip_timer, ask_for_reset)
    else:
        command_shifter(timer_reset, cancel_reset)


def skip_and_next():
    if not reset_question_enable:
        window.bind("<space>", skip_timer)
        skip_label.place(relx=0.5, rely=0.68, anchor="center")
        skip_label.config(text="Left click or Space\nto begin the next square")
        command_shifter(skip_timer, ask_for_reset)


def skip_timer(e=None):
    global skip
    if section == 8:
        reset_square()
    else:
        skip = True


# ---------------------------- TOTAL TIME CALCULATOR ------------------------------- #
def tt_calc(e=None):
    ttc = tt_calculator.TTCalculator(total_work_time)
    ttc.total_time_calculator()


# ---------------------------- SHOW HIDE SETTINGS ------------------------------- #
def show_settings(e=None):
    settings_label.place(relx=0.5, rely=0.28, anchor="center")
    work_time_input_label.place(relx=0.33, rely=0.42, anchor="center")
    short_break_input_label.place(relx=0.5, rely=0.42, anchor="center")
    long_break_input_label.place(relx=0.67, rely=0.42, anchor="center")
    work_time_input.place(relx=0.33, rely=0.52, anchor="center")
    short_break_input.place(relx=0.5, rely=0.52, anchor="center")
    long_break_input.place(relx=0.67, rely=0.52, anchor="center")
    save_button.place(relx=0.5, rely=0.68, anchor="center")
    settings_canvas.place(relx=0.5, rely=0.5, anchor="center")

    window.bind("<s>", hide_settings)


def hide_settings(e=None):
    settings_label.place_forget()
    work_time_input_label.place_forget()
    short_break_input_label.place_forget()
    long_break_input_label.place_forget()
    work_time_input.place_forget()
    long_break_input.place_forget()
    short_break_input.place_forget()
    save_button.place_forget()
    settings_canvas.place_forget()

    window.bind("<s>", show_settings)


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Square Pomodoro")
window.geometry("400x400")

style = ttkthemes.ThemedStyle(window)
style.set_theme("equilux")
style.map(
    "TButton", background=[("disabled", "Gray45")], foreground=[("disabled", "Gray75")]
)

canvas = tk.Canvas(width=400, height=400, bg=LARGE_SQUARE_COLOR, highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor="center")

# Square sides --------------------------------------------------
line1 = canvas.create_line(0, 394, 400, 394, fill="Gray25", width=12)
line2 = canvas.create_line(394, 400, 394, 0, fill="Gray25", width=12)
line3 = canvas.create_line(0, 6, 400, 6, fill="Gray25", width=12)
line4 = canvas.create_line(6, 400, 6, 0, fill="Gray25", width=12)

bottom_side = canvas.create_line(0, 0, 0, 0, fill=SIDES_COLOR, width=12)
right_side = canvas.create_line(0, 0, 0, 0, fill=SIDES_COLOR, width=12)
top_side = canvas.create_line(0, 0, 0, 0, fill=SIDES_COLOR, width=12)
left_side = canvas.create_line(0, 0, 0, 0, fill=SIDES_COLOR, width=12)

corner1 = canvas.create_rectangle(6, 394, 6, 394, fill="Black", width=12)
corner2 = canvas.create_rectangle(394, 394, 394, 394, fill="Black", width=12)
corner3 = canvas.create_rectangle(394, 6, 394, 6, fill="Black", width=12)
corner4 = canvas.create_rectangle(6, 6, 6, 6, fill="Black", width=12)

# Timer text and frame --------------------------------------------------
timer_frame = canvas.create_rectangle(
    80, 80, 320, 320, fill=SMALL_SQUARE_COLOR, width=2, outline="Gray"
)
canvas.tag_bind(timer_frame, "<Button-1>", start_pause_reset)
canvas.tag_bind(timer_frame, "<Button-3>", ask_for_reset)
canvas.tag_bind(timer_frame, "<Button-2>", show_settings)

timer_text = tk.Label(
    text="30:00", font=(FONT_NAME, 42, "bold"), bg=SMALL_SQUARE_COLOR, fg="Gray90"
)
timer_text.place(relx=0.5, rely=0.5, anchor="center")
timer_text.bind("<Button-1>", start_pause_reset)
timer_text.bind("<Button-3>", ask_for_reset)
timer_text.bind("<Button-2>", show_settings)

timer_status = tk.Label(
    text="Timer Status",
    bg=LARGE_SQUARE_COLOR,
    fg="Gray90",
    font=(FONT_NAME, 14, "bold"),
)
timer_status.place(relx=0.5, rely=0.11, anchor="center")

# Reset, skip and squares label --------------------------------------------------
reset_confirm_label = tk.Label(
    text="Do you confirm the reset? y/n\nLeft click Yes, Right click No",
    bg=SMALL_SQUARE_COLOR,
    fg="#D54C4C",
    font=(FONT_NAME, 11),
)
reset_confirm_label.bind("<Button-2>", show_settings)

skip_label = tk.Label(
    text=f"Left click or\nSpace for skip\nthe break",
    bg=SMALL_SQUARE_COLOR,
    fg="Gray50",
    font=(FONT_NAME, 11),
)
skip_label.bind("<Button-2>", show_settings)

squares_label = tk.Label(
    text=f"{squares} ⬜",
    bg=LARGE_SQUARE_COLOR,
    fg="Gray90",
    font=(FONT_NAME, 14, "bold"),
)


def squares_label_enter(e=None):
    squares_label.config(fg=SIDES_COLOR)


def squares_label_leave(e=None):
    squares_label.config(fg="Gray90")


squares_label.bind("<Enter>", squares_label_enter)
squares_label.bind("<Leave>", squares_label_leave)

squares_label.bind("<Button-1>", tt_calc)
squares_label.place(relx=0.5, rely=0.88, anchor="center")

# ---------------------------- SETTINGS UI ------------------------------- #
settings_canvas = tk.Canvas(
    width=243, height=243, bg=SETTINGS_SQUARE_COLOR, highlightthickness=0
)
settings_frame = settings_canvas.create_rectangle(
    0, 0, 243, 243, width=4, outline="Black"
)
settings_canvas.bind("<Button-2>", hide_settings)

work_time_input_label = tk.Label(text="Work\nTime", bg=SETTINGS_SQUARE_COLOR)
work_time_input_label.bind("<Button-2>", hide_settings)

short_break_input_label = tk.Label(text="Short\nBreak", bg=SETTINGS_SQUARE_COLOR)
short_break_input_label.bind("<Button-2>", hide_settings)

long_break_input_label = tk.Label(text="Long\nBreak", bg=SETTINGS_SQUARE_COLOR)
long_break_input_label.bind("<Button-2>", hide_settings)

settings_label = tk.Label(
    text="Settings", bg=SETTINGS_SQUARE_COLOR, font=(FONT_NAME, 12, "bold")
)
settings_label.bind("<Button-2>", hide_settings)

save_button = ttk.Button(text="Save", command=save_button_commands, takefocus=False)
save_button["state"] = tk.DISABLED

# Time inputs --------------------------------------------------
default_work_num = tk.StringVar(window)
work_time_tuple = (
    "10",
    "15",
    "20",
    "25",
    "30",
    "35",
    "40",
    "45",
    "50",
    "55",
    "60",
    "65",
    "70",
    "75",
    "80",
    "85",
    "90",
    "95",
    "100",
    "105",
    "110",
    "115",
    "120",
)
work_time_input = ttk.OptionMenu(
    window,
    default_work_num,
    str(work_time),
    *work_time_tuple,
    command=lambda _: save_button_state(),
)
work_time_input.config(width=3)

default_long_break_num = tk.StringVar(window)
long_break_tuple = (
    "10",
    "15",
    "20",
    "25",
    "30",
    "35",
    "40",
    "45",
    "50",
    "55",
    "60",
    "65",
    "70",
    "75",
    "80",
    "85",
    "90",
    "95",
    "100",
    "105",
    "110",
    "115",
    "120",
)
long_break_input = ttk.OptionMenu(
    window,
    default_long_break_num,
    str(long_break_time),
    *long_break_tuple,
    command=lambda _: save_button_state(),
)
long_break_input.config(width=3)

default_short_break_num = tk.StringVar(window)
short_break_tuple = (
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
)
short_break_input = ttk.OptionMenu(
    window,
    default_short_break_num,
    str(short_break_time),
    *short_break_tuple,
    command=lambda _: save_button_state(),
)
short_break_input.config(width=3)


# ---------------------------- HELP PAGE ------------------------------- #
def show_help(e=None):
    help_about_canvas.place(relx=0.5, rely=0.5, anchor="center")
    help_about_canvas.bind("<Button-1>", hide_help)
    window.bind("<Escape>", hide_help)
    window.bind("<F1>", hide_help)


def hide_help(e=None):
    help_about_canvas.place_forget()
    window.bind("<Escape>", minimize_window)
    window.bind("<F1>", show_help)


help_label = tk.Label(
    text="Help", bg=LARGE_SQUARE_COLOR, fg="Silver", font=(FONT_NAME, 10)
)
help_label.bind("<Button-1>", show_help)


def help_label_enter(e=None):
    help_label.config(fg="White")


def help_label_leave(e=None):
    help_label.config(fg="Silver")


help_label.bind("<Enter>", help_label_enter)
help_label.bind("<Leave>", help_label_leave)

# Help text --------------------------------------------------
help_about_canvas = tk.Canvas(
    width=376, height=376, bg=LARGE_SQUARE_COLOR, highlightthickness=0
)

name_title = help_about_canvas.create_text(
    30,
    20,
    text="Square Pomodoro",
    font=(FONT_NAME, 12, "bold"),
    fill="Gray80",
    anchor="nw",
)

help_title = help_about_canvas.create_text(
    30, 65, text="Shortcuts", font=(FONT_NAME, 10, "bold"), fill="Gray80", anchor="nw"
)

help_about_canvas.create_text(
    30,
    90,
    text="Left click or <Space> = Play/Pause\nRight click or <r> = Reset "
    "timer\nMiddle click or <s> = Show/Hide Settings\nMouse wheel or <Esc> = "
    "Minimize window\nClick on square counter or <t> = Show total work time",
    fill="Gray80",
    anchor="nw",
)

about_title = help_about_canvas.create_text(
    30, 220, text="About", font=(FONT_NAME, 10, "bold"), fill="Gray80", anchor="nw"
)

help_about_canvas.create_text(
    30,
    245,
    text="Square Pomodoro (Version 1.0)\n\nThis is a time management app based on\npomodoro technique\n\nCreated by Farzad Daneshpour",
    fill="Gray80",
    anchor="nw",
)

help_about_canvas.create_line(20, 196, 356, 196, fill="Gray80")
help_label.place(relx=0.045, rely=0.035)

# ---------------------------- KEYBOARD SHORTCUTS ------------------------------- #
window.bind("<F1>", show_help)
window.bind("<space>", start_pause_reset)
window.bind("<Escape>", minimize_window)
window.bind("<MouseWheel>", minimize_window)
window.bind("<r>", ask_for_reset)
window.bind("<s>", show_settings)
window.bind("<t>", tt_calc)
window.resizable(False, False)

# ---------------------------- SAVE LAST WINDOW POSITION ------------------------------- #
win_pos = save_last_win_pos.WinPos(window)

# ---------------------------- TIMER DATA DIR CHECK ------------------------------- #
if os.path.exists("t_data.csv"):
    load_timer()

# ----------------------------------------------------------- #
window.iconbitmap("sqp.ico")
window.mainloop()
