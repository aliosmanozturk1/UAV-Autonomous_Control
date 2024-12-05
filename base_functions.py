from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
from pymavlink import mavutil


connection_string = "tcp:10.211.55.22:5762"
print("Connecting to vehicle on: ", connection_string)
vehicle = connect(connection_string, wait_ready=True)
altitude = vehicle.location.global_relative_frame.alt


def arm_and_takeoff(targetAltitude):
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(targetAltitude)  # Take off to target altitude
    """
    Wait until the vehicle reaches a safe height before processing the goto
    (otherwise the command after Vehicle.simple_takeoff will execute immediately).
    """
    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= targetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def get_bearing(aLocation1, aLocation2):
    """
    Returns the bearing between the two LocationGlobal objects passed as parameters.

    This method is an approximation, and may not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    off_x = aLocation2.lon - aLocation1.lon
    off_y = aLocation2.lat - aLocation1.lat
    bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
    if bearing < 0:
        bearing += 360.00
    return bearing;


def get_angle_between_points(start_point, point1, point2):
    line_1 = int(get_bearing(start_point, point1))
    line_2 = int(get_bearing(point1, point2))

    #print("1. doğrunun Bearing'i: ", line_1)
    #print("2. doğrunun Bearing'i: ", line_2)

    while True:
        if (line_1 - 90) > 0:
            line_1 = line_1 - 90

        if (line_1 - 90) < 0:
            break

    line_1_angle = 90 - line_1

    while True:
        if (line_2 - 90) > 0:
            line_2 = line_2 - 90

        if (line_2 - 90) < 0:
            break

    line_2_angle = line_2

    angle_between_points = 90 - line_1_angle - line_2_angle
    if angle_between_points < 0:
        angle_between_points = angle_between_points + 90


    #print("1. Doğrunun açısı: ", line_1_angle)
    #print("2. Doğrunun açısı: ", line_2_angle)

    #print("Doğrular arasındaki açı: ", angle_between_points)

    return angle_between_points


def get_home_location():
    return vehicle.location.global_relative_frame


def get_current_location():
    return vehicle.location.global_relative_frame

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def goto_position_target_local_ned(north, east, down):
    """
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified
    location in the North, East, Down frame.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down,
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    # send command to vehicle
    vehicle.send_mavlink(msg)


def pixels_per_meter_x(alt):
    return ((alt * math.tan(math.radians(62.2 / 2))) / (640 / 2))

def pixels_per_meter_y(alt):
    return ((alt * math.tan(math.radians(48.8 / 2))) / (480 / 2))

