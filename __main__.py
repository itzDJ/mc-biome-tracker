"""
Program to track visited biomes in a 1.8.9 or 1.12.2 Minecraft Java Edition world

Used for visiting every biome achievement/advancement
"""

from pathlib import Path
from platform import system
from sys import exit

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from json import load


def get_version():
    ver = input('World version (1.8.9 / 1.12.2): ')
    if ver == '1.8.9':
        version = '1.8.9'
        with open(f'{file_dir}/data.txt', 'w') as f:
            f.write(f'{version}\n')

        print('1.8.9 local world location: minecraft/saves/[world]/stats/')
        return version
    elif ver == '1.12.2':
        version = '1.12.2'
        with open(f'{file_dir}/data.txt', 'w') as f:
            f.write(f'{version}\n')

        print('1.12.2 local world location: minecraft/saves/[world]/advancements/')
        return version
    else:
        print('Please enter "1.8.9" or "1.12.2"')
        exit()


def get_json():
    print('Select the json file containing biome data.')

    Tk().withdraw()
    json_file = askopenfilename(initialdir=mc_file)
    with open(f'{file_dir}/data.txt', 'a') as f:
        f.write(json_file)

    return json_file


def main():
    print('MC Biome Tracker\n')

    with open(f'{file_dir}/data.txt') as f:
        lines = f.readlines()
        # if data.txt has two lines
        if len(lines) == 2:
            reuse = input('Reuse last file (yn): ')
            if reuse == 'y':
                # first line is the version minus the new line character
                version = lines[0][:-1]

                # second line is the json_file
                json_file = lines[1]
            else:
                version = get_version()
                json_file = get_json()
        else:
            version = get_version()
            json_file = get_json()

    if version == '1.8.9':
        with open(json_file) as f:
            file = load(f)
            explored_biomes = file['achievement.exploreAllBiomes']['progress']

        with open(f'{file_dir}/1.8.9_biomes.txt') as f:
            print('\nBiome list:')
            biomes = f.readlines()
            for biome in biomes:
                biome = biome[:-1]
                if biome in explored_biomes:
                    # print in green
                    print(f'\033[32m{biome}\033[0m')
                else:
                    print(biome)
    elif version == '1.12.2':
        with open(json_file) as f:
            file = load(f)
            explored_biomes = [key for key in file['minecraft:adventure/adventuring_time']['criteria']]

        with open(f'{file_dir}/1.12.2_biomes.txt') as f:
            print('\nBiome list:')
            biomes = f.readlines()
            for biome in biomes:
                biome = biome[:-1]
                if biome in explored_biomes:
                    # print in green
                    print(f'\033[32m{biome}\033[0m')
                else:
                    print(biome)


if __name__ == '__main__':
    # Set location of mc-biome-tracker directory
    file_dir = Path(__file__).absolute().parent

    # Set home path for macOS
    home = str(Path.home())

    # Set OS
    os = system()
    if os == 'Darwin':
        mc_file = f'{home}/Library/Application Support/minecraft/'
    elif os == 'Windows':
        mc_file = '%APPDATA%\\.minecraft'
    else:
        print('OS detection error.\n')
        mc_file = ''

    # Run the main script
    main()
