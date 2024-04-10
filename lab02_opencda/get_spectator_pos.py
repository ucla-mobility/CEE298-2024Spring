# -*- coding: utf-8 -*-
"""
This module provides functions to interact with the CARLA 
simulation environment to get the spectator's position in
CARLA maps.
"""
# Author: Zhaoliang Zheng <zhz03@g.ucla.edu>
# License: TDG-Attribution-NonCommercial-NoDistrib
import carla 
import time 
import os
from datetime import datetime

def get_file_name_use_datetime():
    """
    Generates a file name using the current date and time.

    Returns:
        str: A string representing the file name in the format 
            'data_%Y-%m-%d_%H-%M-%S.txt'.
    """
    # Get current date and time
    current_time = datetime.now()

    # Format the date and time as a string
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")  # You can adjust the format as needed

    # Create a file name with the formatted date and time
    file_name = f"data_{formatted_time}.txt"
    return file_name

def get_spectator_pos(carla_world):
    """
    Retrieves the position of the spectator in the CARLA world.

    Args:
        carla_world (carla.World): The CARLA world instance.

    Returns:
        carla.Transform: The transform representing the position and 
                orientation of the spectator.
    """
    # get the spectator in carla world 
    spectator = carla_world.get_spectator()
    transform = spectator.get_transform()
    print("transform:",transform)
    return transform

def get_map_name(carla_world):
    """
    Retrieves the name of the map in the CARLA world.

    Args:
        carla_world (carla.World): The CARLA world instance.

    Returns:
        str: The name of the map.
    """
    map_name = carla_world.get_map().name
    print("map_name:",map_name)
    return map_name

def save_spectator_pos(file_path,map_name,transform):
    """
    Saves the map name and spectator position to a file.

    Args:
        file_path (str): The path to the file to save the data.
        map_name (str): The name of the map.
        transform (carla.Transform): The transform representing 
            the position and orientation of the spectator.
    """
    with open(file_path, "w") as f:
        f.write(str(map_name))
        f.write("\n")
        f.write(str(transform))

def main():
    # Generate a file name using the current date and time
    file_name = get_file_name_use_datetime()
    
    # Specify the directory path where the file will be saved
    # Note: Please specify your own file_path
    file_path = "/home/zzl/zhaoliang/mobility_lab/CEE298-2024Spring/lab02_opencda/spectator_pos"
    
    # Check if the specified directory exists
    if os.path.exists(file_path):
        pass
    else:
        # If the directory doesn't exist, create it
        os.makedirs(file_path)
        print("{} has been created!".format(file_path))

    # Construct the full file path by joining the directory path and file name
    file_full_path = os.path.join(file_path, file_name)
    
    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    carla_world = client.get_world()
    
    # Get the position of the spectator in the CARLA world
    transform = get_spectator_pos(carla_world)
    
    # Get the name of the map being used in the CARLA world
    map_name = get_map_name(carla_world)
    
    # Save the map name and spectator position to the specified file
    save_spectator_pos(file_full_path, map_name, transform)

def test1():
    """
    This is the test code to place spawn a vehicle on the spectator's position.
    Note:
        If there is any collision on that position, then it will returns errors. 
    """
    # get spectator pos and place a vehicle there
    client = carla.Client('localhost', 2000)
    carla_world = client.get_world()
    # get the spectator in carla world 
    spectator = carla_world.get_spectator()
    transform = spectator.get_transform()
    print("transform:",transform)

    # create a vehicle
    blueprint_library = carla_world.get_blueprint_library().filter('vehicle.*')[0]
    ego = carla_world.spawn_actor(blueprint_library, transform)
    try:
        # Let the ego vehicle exist for 30 seconds
        time.sleep(30)

        # Destroy the ego vehicle
        ego.destroy()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        ego.destroy()


if __name__ == "__main__":
    main()
    # uncomment the test1 and see if you can place 
    # the vehicle without any collision
    # test1()
