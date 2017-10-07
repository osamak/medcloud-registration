import os
import random
import string
import subprocess


def generate_password():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(6))

def createuser(user, password, group):
    os.environ['OC_PASS'] = password
    command = "/usr/local/bin/php70 /home/medcloud/webapps/ownphp70/occ user:add {} --password-from-env -g {} -n".format(user, group)
    output = subprocess.call(command, shell=True)
    if output == 0:
        return True
    else:
        return False

def reset_password(user, password):
    os.environ['OC_PASS'] = password
    command = "/usr/local/bin/php70 /home/medcloud/webapps/ownphp70/occ user:resetpassword {} --password-from-env -n".format(user)
    output = subprocess.call(command, shell=True)
    if output == 0:
        return True
    else:
        return False
