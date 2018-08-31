from __future__ import print_function
import os
import sys
import urllib2
import logging

log = logging.getLogger(__name__)


def from_win_path_to_container(_s):
    s = urllib2.unquote(_s).replace("\\", os.path.sep)
    while "\\" in s:
        s = s.replace("\\", os.path.sep)
    while os.path.sep+os.path.sep in s:
        s = s.replace("//", os.path.sep)
    if s.startswith("file:/"):
        s = s[6:]
    if sys.platform == "win32":
        log.debug("Running on windows")
        return s
    log.debug("Running on {}".format(sys.platform))
    container_drives_path = os.environ.get("EWS_DRIVES_PATH", None)
    drive_separator = os.environ.get("EWS_DRIVES_PATH_SEPARATOR", None)
    mounted_drive_letters = os.environ.get("MOUNTED_EWS_DRIVES", None)
    if mounted_drive_letters is None:
        mounted_drive_letters = []
    else:
        mounted_drive_letters = mounted_drive_letters.split(",")
    mounted_drive_letters = set(
        map(lambda p: p[0].lower(), mounted_drive_letters))
    if not container_drives_path:
        raise RuntimeError("EWS_DRIVES_PATH not set!")
    if not drive_separator:
        raise RuntimeError("EWS_DRIVES_PATH_SEPARATOR not set!")
    if s.startswith(container_drives_path):
        return s
    splits = s.split(os.path.sep)
    dirname = splits[:-1]
    if len(dirname) < 2:
        raise RuntimeError("You need at least 3 levels of nesting!")
    drive_letter = splits[0][0].lower()
    if drive_letter not in mounted_drive_letters:
        raise RuntimeError(
            "Drive '{}' is not mounted on container!".format(splits[0]))
    return os.path.join(
        container_drives_path,
        drive_separator.join((drive_letter, dirname[1])),
        *splits[2:]
    )


def from_container_path_to_win(s):
    if sys.platform == "win32":
        log.debug("Running on windows")
        return s
    container_drives_path = os.environ.get("EWS_DRIVES_PATH", None)
    drive_separator = os.environ.get("EWS_DRIVES_PATH_SEPARATOR", None)
    mounted_drive_letters = os.environ.get("MOUNTED_EWS_DRIVES", None)
    if mounted_drive_letters is None:
        mounted_drive_letters = []
    else:
        mounted_drive_letters = mounted_drive_letters.split(",")
    mounted_drive_letters = set(
        map(lambda p: p[0].lower(), mounted_drive_letters))
    if not container_drives_path:
        raise RuntimeError("EWS_DRIVES_PATH not set!")
    if not drive_separator:
        raise RuntimeError("EWS_DRIVES_PATH_SEPARATOR not set!")
    if not s.startswith(container_drives_path):
        raise RuntimeError("Not a valid docker path!")
    s = s[len(container_drives_path):]
    splits = s.split(os.path.sep)
    drive_letter, root_directory = splits[0].split(drive_separator, 1)
    res = ["{}://{}".format(drive_letter.upper(), root_directory)]
    for x in splits[1:]:
        res.append(x)
    return "//".join(res)


def replace_filepath(file_path, ews_drives_path=None):

    if ews_drives_path is None:
        ews_drives_path = os.environ.get("EWS_DRIVES", None)
    file_path = urllib2.unquote(file_path.decode("utf-8"))
    if file_path.startswith("file://"):
        file_path = file_path[7:]
    while "\\" in file_path:
        file_path = file_path.replace("\\", "/")
    if os.name != "posix":
        return file_path
    for drive_letter in map(chr, range(97, 123)):
        if file_path.lower().startswith(drive_letter+":/"):
            file_path = u'{ews_drives_path}/{drive_letter}/{file_path}'.format(
                ews_drives_path=ews_drives_path,
                drive_letter=drive_letter,
                file_path=file_path[3:]
            )
    return file_path


if __name__ == "__main__":

    windows_path = r"file://F:\wi_A\04_tb\seb_hr-II\15_lk_check\06_bericht\in_arbeit\20180713_pb_lkc_hrII-05_rev0%20-%20Kopie.docm"
    print(windows_path)
    docker_path = from_win_path_to_container(windows_path)
    print(docker_path)
    print(os.path.exists(docker_path))
    windows_path = from_container_path_to_win(docker_path)
    print(windows_path)
