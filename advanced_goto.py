import time
from base_functions import *
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from advanced_goto_param import *


def advanced_goto(wp_list_name):
    home_location = get_home_location()
    for i in range(0, len(wp_list_name)):
        while True:
            currentLocation = vehicle.location.global_relative_frame

            if i == 0:
                vehicle.simple_goto(wp_list_name[i])
                distance_metres = get_distance_metres(currentLocation, wp_list_name[i])
                break

            if i == 1:
                distance_metres = get_distance_metres(currentLocation, wp_list_name[i - 1])
                angle = get_angle_between_points(home_location, wp_list_name[i - 1], wp_list_name[i])

                if angle >= 0 and angle < 10:
                    if distance_metres < ANGLE_0_TO_10_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 10 and angle < 20:
                    if distance_metres < ANGLE_10_TO_20_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 20 and angle < 30:
                    if distance_metres < ANGLE_20_TO_30_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 30 and angle < 40:
                    if distance_metres < ANGLE_30_TO_40_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 40 and angle < 50:
                    if distance_metres < ANGLE_40_TO_50_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 50 and angle < 60:
                    if distance_metres < ANGLE_50_TO_60_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 60 and angle < 70:
                    if distance_metres < ANGLE_60_TO_70_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 70 and angle < 80:
                    if distance_metres < ANGLE_70_TO_80_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 80 and angle < 90:
                    if distance_metres < ANGLE_80_TO_90_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 90 and angle < 100:
                    if distance_metres < ANGLE_90_TO_100_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 100:
                    if distance_metres < ANGLE_100_TO_FOREVER:
                        vehicle.simple_goto(wp_list_name[i])
                        break

            if i > 1:
                distance_metres = get_distance_metres(currentLocation, wp_list_name[i - 1])
                angle = get_angle_between_points(wp_list_name[i - 2], wp_list_name[i - 1], wp_list_name[i])
                if angle >= 0 and angle < 10:
                    if distance_metres < ANGLE_0_TO_10_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 10 and angle < 20:
                    if distance_metres < ANGLE_10_TO_20_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 20 and angle < 30:
                    if distance_metres < ANGLE_20_TO_30_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 30 and angle < 40:
                    if distance_metres < ANGLE_30_TO_40_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 40 and angle < 50:
                    if distance_metres < ANGLE_40_TO_50_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 50 and angle < 60:
                    if distance_metres < ANGLE_50_TO_60_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 60 and angle < 70:
                    if distance_metres < ANGLE_60_TO_70_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 70 and angle < 80:
                    if distance_metres < ANGLE_70_TO_80_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 80 and angle < 90:
                    if distance_metres < ANGLE_80_TO_90_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 90 and angle < 100:
                    if distance_metres < ANGLE_90_TO_100_DST:
                        vehicle.simple_goto(wp_list_name[i])
                        break
                elif angle >= 100:
                    if distance_metres < ANGLE_100_TO_FOREVER:
                        vehicle.simple_goto(wp_list_name[i])
                        break

            time.sleep(0.2)
