import math
import tkinter.messagebox


class TTCalculator:
    def __init__(self, total_work_time):
        self.twt = total_work_time

    def total_time_calculator(self):
        total_hours = math.floor(self.twt / 60)
        total_minutes = self.twt % 60
        hour_s = "hours"
        if total_hours == 1:
            hour_s = "hour"
        tkinter.messagebox.showinfo(
            "Total Time",
            f"Your total work time is:\n\n{total_hours} {hour_s} and {total_minutes} minutes\n\n( {self.twt} m )",
        )
