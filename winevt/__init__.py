import logging

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("winevt")

import winevt.settings as settings

#
# Load up whichever way we can
#

# Assume it's in-line unless we get otherwise
out_of_line = False

try:
    from ._winevt import ffi, lib as evtapi
    # Loading inline, these will be the same
    kernel32 = evtapi
    logger.info("Loaded in-line, user compiled evtapi")
    out_of_line = True

except ModuleNotFoundError:
    logger.warn("Looks like you didn't successfully compile your own out-of-line pyd. Falling back to in-ine mode. This is going to be less efficient and it's recommended you compile your own. To fix this, do the following:\n    1) Check this page and install the correct compiler for your version of python: https://blogs.msdn.microsoft.com/pythonengineering/2016/04/11/unable-to-find-vcvarsall-bat/\n    2) Re-install winevt (pip install -U winevt)")
    # In-line mode
    from .winevt_build import ffibuilder
    ffi = ffibuilder()
    evtapi = ffi.dlopen("Wevtapi.dll")
    kernel32 = ffi.dlopen("Kernel32.dll")

# Init settings if we haven't yet
if settings.callbacks == None:
    settings.init()

#
# Some Enums
#

FORMAT_MESSAGE_ALLOCATE_BUFFER  = 0x00000100
FORMAT_MESSAGE_ARGUMENT_ARRAY   = 0x00002000
FORMAT_MESSAGE_FROM_HMODULE     = 0x00000800
FORMAT_MESSAGE_FROM_STRING      = 0x00000400
FORMAT_MESSAGE_FROM_SYSTEM      = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS   = 0x00000200
FORMAT_MESSAGE_MAX_WIDTH_MASK   = 0x000000FF

#
# Helper functions
#

def get_last_error():
    """ Get the last error value, then turn it into a nice string. Return the string. """
    error_id = kernel32.GetLastError()
    
    # No actual error
    if error_id == 0:
        return None

    # Gonna need a string pointer
    buf = ffi.new("LPWSTR")

    chars = kernel32.FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS, ffi.NULL, error_id , 0, buf, 0, ffi.NULL)

    return ffi.string(ffi.cast("char **",buf)[0][0:chars]).decode('utf-8').strip("\r\n")
