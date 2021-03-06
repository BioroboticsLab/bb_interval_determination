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
        self.curr_img_txt["text"] = tupels[curr_tupel][curr_frame]
        self.curr_img_txt.pack(side="top")

        # Display the first or the last frame of the inerval
        im = Image.open(tupels[curr_tupel][curr_frame])
        im.thumbnail((1200, 800), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(im)
        self.panel = tk.Label(self, image=self.img)
        self.panel.pack(side="top", expand="yes")

        # Display intervall type safe or unsafe interval
        self.curr_interval_type_txt = tk.Label(self, fg='black', text=0)
        self.curr_interval_type_txt["text"] = tupels[curr_tupel]['info']
        self.curr_interval_type_txt.pack(side="top")

        # Navigation Buttons left ad right
        self.navigation_frame = tk.Frame(self)
        self.navigation_frame.pack(side="top")

        self.left = tk.Button(self.navigation_frame)
        self.left["text"] = "<left"
        self.left["command"] = self.go_left
        self.left.pack(side="left")

        self.right = tk.Button(self.navigation_frame)
        self.right["text"] = "right>"
        self.right["command"] = self.go_right
        self.right.pack(side="left")

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

        global curr_tupel
        global curr_frame

        if curr_frame == 'last_frame':
            curr_frame = 'first_frame'
            color = "blue"
        else:
            curr_frame = 'last_frame'
            color = "green"

        self.curr_interval_type_txt["text"] = 'Interval tpye: ' + tupels[curr_tupel]['info']
        if tupels[curr_tupel]['info'] == "ecc stable":
            self.curr_interval_type_txt["fg"] = 'light green'
            self.curr_interval_type_txt["bg"] = 'dark green'
        else:
            self.curr_interval_type_txt["fg"] = 'black'
            self.curr_interval_type_txt["bg"] = 'light grey'
        self.curr_img_txt["text"] = 'ID: {id} {curr_frame} {path_img}'.format(
            id=tupels[curr_tupel]['id'],
            curr_frame=curr_frame,
            path_img=tupels[curr_tupel][curr_frame]
        )
        self.curr_img_txt["fg"] = color

        im = Image.open(tupels[curr_tupel][curr_frame])
        im.thumbnail((1200, 800), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(im)
        self.panel['image'] = self.img

        if 'stable' in json_intervals[curr_tupel].keys():
            self.curr_grading["text"] = str(json_intervals[curr_tupel]['stable'])
            if not json_intervals[curr_tupel]['stable']:
                self.curr_grading["fg"] = 'red'
                self.curr_grading["bg"] = "dark red"
            else:
                self.curr_grading["fg"] = 'light green'
                self.curr_grading["bg"] = "dark green"
        else:
            self.curr_grading["text"] = ''
            self.curr_grading["bg"] = 'light grey'

        self.panel.after(1000, self.switch_image)

    def go_right(self):
        global curr_tupel

        if curr_tupel+1 == count_pairs:
            self.info_text["text"] = 'This is already the last pair of frames.'
        else:
            curr_tupel += 1
            self.info_text["text"] = ''

    def go_left(self):
        global curr_tupel

        if curr_tupel == 0:
            self.info_text["text"] = 'This is already the first pair of frames.'
        else:
            curr_tupel -= 1
            self.info_text["text"] = ''

    def mark_unstable(self):
        global json_intervals
        global curr_tupel

        assert json_intervals[curr_tupel]['id'] == curr_tupel

        json_intervals[curr_tupel]['stable'] = False

        self.go_right()

    def mark_stable(self):
        global json_intervals
        global curr_tupel

        assert json_intervals[curr_tupel]['id'] == curr_tupel

        json_intervals[curr_tupel]['stable'] = True

        self.go_right()

    def exit_wo_save(self):
        global save
        save = False
        root.destroy()

    def exit_save(self):
        global save
        save = True
        root.destroy()

CAM_ID = 3
path = "Cam_{CAM_ID}_intervals_ecc.json".format(CAM_ID=CAM_ID)
path_images = './Cam_{CAM_ID}'.format(CAM_ID=CAM_ID)

basename_json = os.path.splitext(os.path.basename(path))[0]
output_path = '05a_{basename}_stable.json'.format(basename=basename_json)

save = False
if os.path.exists(output_path):
    with open(output_path, 'r') as jsonfile:
        json_intervals = json.load(jsonfile)
else:
    with open(path, 'r') as jsonfile:
        json_intervals = json.load(jsonfile)

tupels = []
#  iterate through intervals
for row in json_intervals:
    display = row
    fst_frame_name_save = '{num:02}_fst_{basename}.jpg'.format(
        num=row['id'], basename=os.path.splitext(row['start_video_name'])[0])
    display["first_frame"] = os.path.join(path_images, fst_frame_name_save)

    last_fram_name_save = '{num:02}_lst_{basename}.jpg'.format(
        num=row['id'],
        basename=os.path.splitext(row['end_video_name'])[0])
    display["last_frame"] = os.path.join(path_images, last_fram_name_save)
    tupels.append(display)

curr_tupel = 0
curr_frame = 'first_frame'
count_pairs = len(tupels)
root = tk.Tk()
app = Application(master=root)
app.mainloop()
if save:
    with open(output_path, 'w') as fp:
            json.dump(json_intervals, fp)
    print('File was saved to {output_path}'.format(output_path=output_path))
    with open(os.path.join('../docs', output_path), 'w') as fp:
        json.dump(json_intervals, fp)
