from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from pymavlink import mavutil
import math
import time
from base_functions import *
from object_detection import *
from advanced_goto import *
from wp_list import *


arm_and_takeoff(10)
advanced_goto(wp_list_before_red_pool_route)

advanced_goto(wp_list_end_red_pool_route)
while True:
    objectDetection()
    if objectDetection() == "AREA-FOUND":
        vehicle.mode = VehicleMode("BRAKE")
        break
time.sleep(2)
vehicle.mode = VehicleMode("GUIDED")
time.sleep(2)
while True:
    objectDetection()
    if objectDetection() == "AREA-FOUND":
        if len(listX) > 30:
            averageXValue = int(sum(listX) / 30)
            ppm_x = pixels_per_meter_x(1)
            velocity_x = round((averageXValue * ppm_x), 3)
            listX.clear()

            if len(listY) > 30:
                averageYValue = int(sum(listY) / 30)
                ppm_y = pixels_per_meter_y(1)
                velocity_y = round((averageYValue * ppm_y), 3)
                listY.clear()

                print("Average X: ", averageXValue)
                print("Average Y: ", averageYValue)

                if averageXValue > 50 or averageYValue > 50:
                    print("Hız komutu veriliyor.")
                    send_ned_velocity(velocity_x, velocity_y, 0, 1)
                    time.sleep(1)
                    print("Hız komutu bitti.")
                elif averageXValue < -50 or averageYValue < -50:
                    print("Hız komutu veriliyor.")
                    send_ned_velocity(velocity_x, velocity_y, 0, 1)
                    time.sleep(1)
                    print("Hız komutu bitti.")
                elif averageXValue < -50 or averageYValue > 50:
                    print("Hız komutu veriliyor.")
                    send_ned_velocity(velocity_x, velocity_y, 0, 1)
                    time.sleep(1)
                    print("Hız komutu bitti.")
                elif averageXValue > 50 or averageYValue < -50:
                    print("Hız komutu veriliyor.")
                    send_ned_velocity(velocity_x, velocity_y, 0, 1)
                    time.sleep(1)
                    print("Hız komutu bitti.")
                else:
                    print("Merkez noktaya yeterince yakınız, RTK GPS ile konum alınmaya başlanabilir.")
                    break
red_pool_location = get_current_location()

advanced_goto(wp_list_red_to_blue)
goto_position_target_local_ned(0,0,8)
while True:
    if vehicle.location.global_relative_frame.alt <= 8 * 0.95:
        print("Reached target altitude")
        break


advanced_goto(wp_list_blue_to_red)
while True:
    if vehicle.location.global_relative_frame.alt <= 8 * 0.95:
        print("Reached target altitude")
        break

advanced_goto(wp_list_complete_tour)

print("Mission Completed!")