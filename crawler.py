import getpass
import json
import os
import platform
import shutil
import sys

import PIL.Image

# Check if the user is on Windows.
is_windows = platform.system() == 'Windows'
if not is_windows:
    print('We detected your operating system is not Windows. '
          'This program is designed to only work with Windows operating system.')
    input('Press any key to continue.')
    sys.exit()

# Load settings.
with open('setting.json') as json_file:
    setting = json.load(json_file)
is_silent = setting['silent']

# Check for username.
username = getpass.getuser()
if not is_silent:
    prompt = 'Script detected "{}" is your username. Type "n" if incorrect. Press any key to continue...: '.format(
        username)
    raw_is_correct_username = input(prompt)
    if raw_is_correct_username == 'n':
        username = input('Please enter your username under C://Users/ directory: ')

# Set destination and source.
drive_letter = os.environ['systemdrive']
file_dir = '{}/Users/{}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager' \
           '_cw5n1h2txyewy/LocalState/Assets'.format(drive_letter, username)
os.chdir(file_dir)
file_names = os.listdir(file_dir)
source_directory = os.getcwd()
destination_directory = '{}/Users/{}/Documents/Windows_spotlight/'.format(drive_letter, username)
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Ask for orientation.
if is_silent:
    save_option = setting['orientation']
else:
    save_option = None
    while save_option not in ('1', '2', '3'):
        # Wallpapers are generally 1920*1080 and 1080*1920
        save_option = input('Which resolution would you save? \n1: Landscape (1920*1080)'
                            '\n2: Portrait (1080*1920)\n3: Both\n')

# Iterate over the files in the target folder and copy any possible images.
for file_name in file_names:
    source_file_name = os.path.join(file_dir, file_name)
    stat_info = os.stat(source_file_name)
    file_size = stat_info.st_size

    # Filter out small files (<50KB).
    if file_size < 50000:
        continue

    new_image = file_name + '.jpg'
    source_file_name = os.path.join(source_directory, file_name)
    destination_file_name = os.path.join(destination_directory, new_image)
    image = PIL.Image.open(source_file_name)
    width, height = image.size

    # Filter out icons. Icons are normally square.
    if width == height:
        continue

    # Save only the files with desired orientation.
    if save_option == '1' and width < height:
        continue
    elif save_option == '2' and width > height:
        continue

    shutil.copyfile(source_file_name, destination_file_name)

# Open the destination directory, and terminate the program.
path = os.path.realpath(destination_directory)
if is_silent:
    os.startfile(path)

sys.exit()
