import csv
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

        im = Image.open(paths[curr])
        im.thumbnail((1800, 1800), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(im)

        # Navigation Buttons
        self.navigation_frame = tk.Frame(self)
        self.navigation_frame.pack()

        self.left = tk.Button(self.navigation_frame)
        self.left["text"] = "<left"
        self.left["command"] = self.go_left
        self.left.pack(side="left")

        self.right = tk.Button(self.navigation_frame)
        self.right["text"] = "right>"
        self.right["command"] = self.go_right
        self.right.pack(side="left")

        # Display Image
        self.current_img = tk.Label(self, fg='green', text=0)
        self.current_img["text"] = os.path.basename(paths[0])
        self.current_img.pack(side="top")

        # Display Day
        self.day_of_move = tk.Label(self, fg='red', text=0)
        self.day_of_move["text"] = os.path.basename(paths[curr]).split('--')[1][:10]
        self.day_of_move.pack(side="top")

        # grading
        self.grading_frame = tk.Frame(self)
        self.grading_frame.pack(side="bottom")

        self.moved = tk.Button(self.grading_frame, text="Moved",
                               fg="red", command=self.save_as_moved)
        self.moved.pack(side="left")
        self.not_moved = tk.Button(self.grading_frame, text="Not Moved",
                                   fg="green", command=self.save_as_not_moved)
        self.not_moved.pack(side="left")

        self.exit = tk.Frame(self)
        self.exit.pack(side="bottom")

        self.quit = tk.Button(self.exit, text="Exit",
                              command=self.exit_wo_save)
        self.quit.pack(side="left")

        self.quit = tk.Button(self.exit, fg='red', text="Exit and save",
                              command=self.exit_save)
        self.quit.pack(side="right")

        self.panel = tk.Label(self, image=self.img)
        self.panel.pack(side="top", expand="yes")

    def go_right(self):
        global curr
        global succ
        global len_images
        if succ + 1 == len_images:
            print('Last videos.')
        else:
            curr = (curr + 1) % len_images
            succ = (succ + 1) % len_images
        self.day_of_move["text"] = os.path.basename(paths[curr]).split('--')[1][:10]

    def go_left(self):
        global curr
        global succ
        global len_images
        if curr == 0:
            print('First videos.')
        else:
            curr = (curr - 1) % len_images
            succ = (succ - 1) % len_images
        self.day_of_move["text"] = os.path.basename(paths[curr]).split('--')[1][:10]

    def switch_image(self):
        global curr
        global succ
        global shown
        if shown == curr:
            shown = succ
            desc = "2. succ: "
            color = "blue"
        else:
            shown = curr
            desc = "1. curr: "
            color = "green"
        self.current_img["text"] = desc + os.path.basename(paths[shown])
        self.current_img["fg"] = color
        im = Image.open(paths[shown])
        im.thumbnail((1200, 800), Image.ANTIALIAS)

        self.img = ImageTk.PhotoImage(im)
        self.panel['image'] = self.img
        self.panel.after(1000, self.switch_image)

    def save_as_moved(self):
        data.append([os.path.basename(paths[curr]), os.path.basename(paths[succ]), 1])
        print(data[-1:])
        self.go_right()

    def save_as_not_moved(self):
        data.append([os.path.basename(paths[curr]), os.path.basename(paths[succ]), 0])
        print(data[-1:])
        self.go_right()

    def exit_wo_save(self):
        global save
        save = False
        root.destroy()

    def exit_save(self):
        global save
        save = True
        root.destroy()


path = 'raw_data/02_frames_per_day/2016/cam_0'
csv_out_path = 'derived_data/02_man_marked_moved_frames/manuel_Cam_0.csv'

# path = 'raw_data/02_frames_per_day/2016/cam_1'
# csv_out_path = 'derived_data/02_man_marked_moved_frames/manuel_Cam_1.csv'

# path = 'raw_data/02_frames_per_day/2016/cam_2'
# csv_out_path = 'derived_data/02_man_marked_moved_frames/manuel_Cam_2.csv'

# path = 'raw_data/02_frames_per_day/2016/cam_3'
# csv_out_path = 'derived_data/02_man_marked_moved_frames/manuel_Cam_3.csv'
save = False
shown = 0
curr = 0
succ = 1
names = os.listdir(path)
names.sort()
paths = []
for name in names:
    paths.append(os.path.join(path, name))
len_images = len(paths)
data = []
root = tk.Tk()
app = Application(master=root)
app.mainloop()
if save:
    with open(csv_out_path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        row = ["first_frame", "second_frame", "moved"]
        writer.writerow(row)
        for line in data:
            writer.writerow(line)
    print('Written to {path}'.format(path=csv_out_path))
else:
    print('Exit without save')
