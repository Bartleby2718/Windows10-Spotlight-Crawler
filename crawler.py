import getpass
import json
import os
import platform
import shutil
import sys

import PIL.Image


drive_letter = os.environ['systemdrive']

# Check if the user is on Windows.
is_Windows = platform.system() == 'Windows'
if not is_Windows:
    print('We detected your operating system is not Windows. '
          'This program is designed to only work with Windows operating system.')
    input('Press any key to continue.')
    sys.exit()

# Load settings.
with open('setting.json') as s:
    setting = json.load(s)

# Check for username.
your_username = getpass.getuser()
if not setting['silent']:
    prompt = 'Script detected "{}" is your username. Type "n" if incorrect. Press any key to continue...: '.format(
        your_username)
    raw_is_correct_username = input(prompt)
    if raw_is_correct_username == 'n':
        your_username = input('Please enter your username under C://Users/ directory: ')

# Set destination and source.
file_dir = '{}/Users/{}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager' \
           '_cw5n1h2txyewy/LocalState/Assets'.format(drive_letter, your_username)
os.chdir(file_dir)
name_list = os.listdir(file_dir)
src_common = os.getcwd()
dst_common = '{}/Users/{}/Documents/Windows_spotlight/'.format(drive_letter, your_username)

# Ask for orientation.
save_option = 0
if setting['silent']:
    save_option = setting['orientation']
else:
    while save_option not in ['1', '2', '3']:
        # Wallpapers are generally 1920*1080 and 1080*1920
        save_option = input('Which resolution would you save? \n1: Landscape (1920 * 1080)'
                            '\n2: Portrait (1080*1920)\n3: Both\n')

# Iterate over the files in the target folder and copy any possible images.
for file in name_list:
    src = file_dir + '/' + file
    stat_info = os.stat(src)
    file_size = stat_info.st_size

    # Filter out small files (<50KB).
    if file_size > 50000:
        new_image = file + '.jpg'
        src = os.path.join(src_common, file)
        src_ext = os.path.join(src_common, new_image)
        dst = os.path.join(dst_common, new_image)
        im = PIL.Image.open(src)
        width, height = im.size

        # Filter out icons. Icons are normally square.
        if width == height:
            continue

        # Save only the files with desired orientation.
        if save_option == '1':
            if width < height:
                continue
        elif save_option == '2':
            if width > height:
                continue

        if not os.path.exists(dst_common):
            os.makedirs(dst_common)

        shutil.copyfile(src, dst)

# Open the destination directory, and terminate the program.
path = os.path.realpath(dst_common)
if setting['silent']:
    os.startfile(path)

sys.exit()
