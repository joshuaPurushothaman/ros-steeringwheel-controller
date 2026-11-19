# ROS Steeringwheel Controller

Takes in an HID gamepad / steering wheel (We're designing this around the Moza R5)
    and publishes that as teleop controls to a ROS node to control an F1Tenth / RoboRacer car.


Streams the video from the F1Tenth car back to here as well!

(May try to make it work cross-platform but testing on Linux and with ROS Humble for now)



## On the car, something like this:
```bash
sudo apt update
sudo apt install ros-$ROS_DISTRO-realsense2-camera

ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=false
# This would publish to /camera/camera/color/image_raw
```

## On the laptop:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh # install uv if you need to
uv run main.py
```