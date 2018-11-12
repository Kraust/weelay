import weechat
import re
import os
import errno

_name = "weelay"
_author = "Kraust"
_version = "0.0.1"
_license = "Unlicense"
_description = "automatically sort xddc downloads"
_shutdown_function = ""
_charset = ""

weechat.register(_name, _author, _version, _license, _description, _shutdown_function, _charset)

weechat.hook_signal("xfer_ended", "xfer_ended_cb", "")

def mkdirs(newdir, mode=0777):
    try: os.makedirs(newdir, mode)
    except OSError, err:
        if err.errno != errno.EEXIST or not os.path.isdir(newdir): 
            raise

def xfer_ended_cb(data, signal, signal_data):
    output_directory = weechat.config_get_plugin("output_directory")
    regex_list = weechat.config_get_plugin("regex_list").split(',')

    weechat.infolist_next(signal_data)
    status_string = weechat.infolist_string(signal_data, 'status_string')
    filename = weechat.infolist_string(signal_data, 'filename')
    local_filename =  weechat.infolist_string(signal_data, 'local_filename')

    if status_string == "done":
        for regex in regex_list:
            m = re.match(regex, filename)
            if m:
                folder = output_directory + os.sep + m.group(1)
                try:
                    weechat.prnt("", "weelay: mkdir {}".format(folder))
                    mkdirs(folder)
                    os.rename(local_filename, folder + os.sep + filename)
                except Exception as e:
                    weechat.prnt("", "weeelay: Failed to copy file {} - {}".format(local_filename, e))
                    return weechat.WEECHAT_RC_OK
                weechat.prnt("", "weelay: coppied {} to {}".format(filename, folder + os.sep + filename))
                break

    return weechat.WEECHAT_RC_OK

def init_plugin():
    if not weechat.config_is_set_plugin("output_directory"):
        weechat.config_set_plugin("output_directory", os.path.expanduser("~") + os.sep + "Video")
    if not weechat.config_is_set_plugin("regex_list"):
        weechat.config_set_plugin("regex_list", '([A-z].*)\.S([0-9].E[0-9].)\..*,\[[A-z].*\]_([A-z].*)_-_([0-9].*).*')


if __name__ == "__main__":
    init_plugin()
    ##regex_list = weechat.config_get_plugin("regex_list").split(',')
    ##for regex in regex_list:
        ##weechat.prnt("", "weelay: loaded regex - " + regex)

