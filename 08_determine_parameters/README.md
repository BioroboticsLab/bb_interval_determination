# Determine Parameters

At this step, we have to determine the parameter for stitching, which we will use for the mapping of the `bb_binary`-data to hive coordinates. For this we are taking the first frames of every _'shared'_ interval and stitch them with the `bb_stitcher`. (See [get_finished_intervals_fst_frame.py](./get_finished_intervals_fst_frame.py))

Sometimes the stitching process is not possible with the first frame and so we use some other frames from the same interval. (See [get_single_images.py](./get_single_images.py))
