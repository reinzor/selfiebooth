from time import strftime
import os


class Logger():
    def __init__(self, raw_output_dir):
        # create self._file
        filename = "%s/%s.log" % (raw_output_dir, strftime("%Y_%m_%d_%H_%M_%S"))
        self._file = open(filename, 'w', 0)
        self._seq = 0

    def _log(self, msg, prefix="INFO"):
        msg = "%d\t%s\t%s\t%s" % (self._seq, prefix, strftime("%Y_%m_%d_%H_%M_%S"), msg)
        print msg
        self._file.write("%s\n" % msg)
        os.fsync(self._file)
        self._seq += 1

    def info(self, msg):
        self._log(msg, "INFO")

    def error(self, msg):
        self._log(msg, "ERROR")

    def debug(self, msg):
        self._log(msg, "DEBUG")
