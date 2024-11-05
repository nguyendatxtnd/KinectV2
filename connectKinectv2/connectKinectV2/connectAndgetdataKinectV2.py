import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
import os
import csv
import time


# # set up VA-API if you encounter VA-API related errors then process with GPU
# os.environ["LIBVA_DRIVER_NAME"] = "nvidia"

# Select pipeline to process data received from kinect V2, OpenGLP and OpenCLP process with GPU
try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()

# set logger
logger = createConsoleLogger(LoggerLevel.Debug)
setGlobalLogger(logger)

# initialize and connect kinect V2
fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)
serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

# Set RGB frame and depth frame
listener = SyncMultiFrameListener(FrameType.Color | FrameType.Depth)
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)
device.start()

# declare variables
#folder = "data/data_test"   # folder to save data
folder = "data/data_train" # folder to save data
a = 0                       # counter variable of the order of the data stored
b = 5                       # The time variable is set so that after b seconds the data set will be saved to the folder
t_1 = time.time()           # start time
# Variables are used to ensure that data is stored at the correct size.
height = 424
width = 512

# # create an object that performs alignment between two RGB and Depth frames
# # to combine the two types of data (color and depth) from Kinect v2, making sure they match
# # must be called after device.start()
# registration = Registration(device.getIrCameraParams(),
#                             device.getColorCameraParams())
# undistorted = Frame(512, 424, 4)
# registered = Frame(512, 424, 4)

# receive, save and display depth and RGB data obtained from kinect V2
while True:
    # Wait for new frames (color and depth)
    frames = listener.waitForNewFrame()

    # Get color frame and depth frame
    color = frames["color"]     # size: 1920x1080
    depth = frames["depth"]     # size: 512x424

    # save data after b seconds
    t_2 = time.time()
    if t_2 - t_1 >= b:
        # save data depth
        depth_data = depth.asarray()
        depth_data = depth_data.reshape((height, width))
        depth_data = depth_data.astype(np.uint16)
        path_depth = os.path.join(folder, f"{a}_depth_image.png")
        cv2.imwrite(path_depth, depth_data)
        
        # save iamge rgb
        rgb_image = color.asarray()  
        path_rgb = os.path.join(folder, f'{a}_rgb_image.png')
        cv2.imwrite(path_rgb , rgb_image)  

        # save data path to file csv
        # with open("data/data_test.csv",mode = "a",newline = "") as file:
        with open("data/data_train.csv",mode = "a",newline = "") as file:
            writer = csv.writer(file)
            writer.writerow([path_rgb,path_depth])
        print(f"save data {a+1} time")
        a += 1
        t_1 = time.time() 

    # # Apply registration (depth + rgb alignment), return undistored and registered
    # registration.apply(color, depth, undistorted, registered)

    # # Display the depth frame and RGB frame
    depth_image = depth.asarray()/4500.  
    color_image = color.asarray()
    color_image = cv2.resize(color.asarray(), (int(1920 / 2), int(1080 / 2)))  
    cv2.imshow("depth", depth_image)
    cv2.imshow("color", color_image)

    #cv2.imshow("registered", registered.asarray(np.uint8))
    #cv2.imshow("undistorted", undistorted.asarray(np.uint8))

    # free the frames
    listener.release(frames)

    # enter q to end the program
    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break

# Stop and close device
device.stop()
device.close()
sys.exit(0)





