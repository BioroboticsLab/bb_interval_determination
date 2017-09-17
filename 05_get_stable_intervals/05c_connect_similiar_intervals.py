"""Used for manual checking of intervals.

It is used to manually check whether the camera setup has changed during intervals.
"""
import json
import os
import tkinter as tk

from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.switch_image()

    def create_widgets(self):

        # Display info text (warnings, etc.)
        self.info_text = tk.Label(self, fg='red', text=3)
        self.info_text["text"] = ''
        self.info_text.pack(side="top")

        # Display the path of the current image
        self.curr_img_txt = tk.Label(self, fg='green', text=0)
        self.curr_img_txt["text"] = json_intervals[curr_interval_disp]['first_frame']
        self.curr_img_txt.pack(side="top")

        # Display the first or the last frame of the inerval
        im = Image.open(json_intervals[curr_interval_disp]['first_frame'])
        im.thumbnail((1200, 800), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(im)
        self.panel = tk.Label(self, image=self.img)
        self.panel.pack(side="top", expand="yes")

        # Display intervall type safe or unsafe interval
        self.curr_interval_type_txt = tk.Label(self, fg='black', text=0)
        self.curr_interval_type_txt["text"] = json_intervals[curr_interval_disp]['info']
        self.curr_interval_type_txt.pack(side="top")

        # Grading to say if camera moved in interval or not
        self.grading_frame = tk.Frame(self)
        self.grading_frame.pack(side="top")

        self.unstable = tk.Button(self.grading_frame, text="unstable",
                                  fg="red", command=self.mark_unstable)
        self.unstable.pack(side="left")

        self.stable = tk.Button(self.grading_frame, text="stable",
                                fg="green", command=self.mark_stable)
        self.stable.pack(side="right")

        # Grade info text, if interval is graded.
        self.curr_grading = tk.Label(self, fg='black', text=0)
        self.curr_grading["text"] = ''
        self.curr_grading.pack(side="top")

        # Exit buttons
        self.exit = tk.Frame(self)
        self.exit.pack(side="right")

        self.quit = tk.Button(self.exit, text="Exit",
                              command=self.exit_wo_save)
        self.quit.pack(side="left")

        self.quit = tk.Button(self.exit, fg='red', text="Exit and save",
                              command=self.exit_save)
        self.quit.pack(side="right")

    def switch_image(self):
        global json_intervals

        global start_interval
        global curr_interval

        global curr_interval_disp

        if curr_interval_disp == start_interval:
            curr_interval_disp = curr_interval
            curr_interval_type = 'curr_interval'
            frame_type = 'last_frame'
            color = "blue"
        else:
            curr_interval_disp = start_interval
            curr_interval_type = 'start_interval'
            frame_type = 'first_frame'
            color = "green"

        im = Image.open(json_intervals[curr_interval_disp][frame_type])
        im.thumbnail((1200, 800), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(im)
        self.panel['image'] = self.img

        self.curr_img_txt["text"] = 'ID: {id} {curr_interval_type} {path_img}'.format(
            id=json_intervals[curr_interval_disp]['id'],
            curr_interval_type=curr_interval_type,
            path_img=json_intervals[curr_interval_disp][frame_type]
        )
        self.curr_img_txt["fg"] = color

        self.panel.after(1000, self.switch_image)

    def go_right_curr(self):
        global curr_interval

        if curr_interval+1 == count_interval:
            self.info_text["text"] = 'This is already the last pair of frames.'
        else:
            curr_interval += 1
            self.info_text["text"] = ''

    def go_right_start(self):
        global start_interval

        if start_interval+1 >= curr_interval:
            self.info_text["text"] = 'The start interval must be before the current interval.'
        else:
            start_interval += 1
            self.info_text["text"] = ''

    def go_left_curr(self):
        global curr_interval

        if curr_interval - 1 <= start_interval:
            self.info_text["text"] = 'The current interval must be behind the start interval.'
        else:
            curr_interval -= 1
            self.info_text["text"] = ''

    def go_left_start(self):
        global start_interval

        if start_interval == 0:
            self.info_text["text"] = 'This is already the first frame.'
        else:
            start_interval -= 1
            self.info_text["text"] = ''

    def mark_unstable(self):
        global json_intervals
        global curr_interval
        global start_interval
        global previous_stable_interval
        global connected_intervals

        print('start: {start}, end: {end}'.format(start=start_interval,
                                                  end=previous_stable_interval))

        # save index of start end interval to build a connected interval
        interval_group = (start_interval, previous_stable_interval)
        connected_intervals.append(interval_group)

        start_interval = curr_interval
        previous_stable_interval = start_interval
        self.go_right_curr()

    def mark_stable(self):
        global curr_interval
        global previous_stable_interval
        previous_stable_interval = curr_interval

        self.go_right_curr()

    def exit_wo_save(self):
        global save
        save = False
        root.destroy()

    def exit_save(self):
        global save
        save = True
        root.destroy()

CAM_ID = 3
path = "05b_Cam_{CAM_ID}_intervals_ecc_stable_join.json".format(CAM_ID=CAM_ID)

basename_json = os.path.splitext(os.path.basename(path))[0]
output_path = '05c_{basename}_man.json'.format(basename=basename_json[4:])


save = False
# if os.path.exists(output_path):
#     with open(output_path, 'r') as jsonfile:
#         json_intervals = json.load(jsonfile)
# else:
with open(path, 'r') as jsonfile:
    json_intervals = json.load(jsonfile)

start_interval = 0
previous_stable_interval = 0
curr_interval = 1

curr_interval_disp = curr_interval

count_interval = len(json_intervals)

connected_intervals = []

root = tk.Tk()
app = Application(master=root)
app.mainloop()

intervals = []
for i, (start, end) in enumerate(connected_intervals):
    interval = {}
    interval["id"] = i
    interval["start_video_name"] = json_intervals[start]["start_video_name"]
    interval["end_video_name"] = json_intervals[end]["end_video_name"]
    if start != end:
        interval["info"] = 'manuell connected'
        interval["stable"] = True
    else:
        interval["info"] = json_intervals[end]["info"]
        interval["stable"] = json_intervals[end]["stable"]
    intervals.append(interval)

print(intervals)

if save:
    with open(output_path, 'w') as fp:
            json.dump(intervals, fp)
    print('File was saved to {output_path}'.format(output_path=output_path))
    with open(os.path.join('../docs', output_path), 'w') as fp:
        json.dump(intervals, fp)
