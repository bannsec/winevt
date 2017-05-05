import logging

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("winevt")

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
    logger.warn("Looks like you didn't successfully compile your own out-of-line pyd. Falling back to in-ine mode. This is going to be less efficient and it's recommended you compile your own. To fix this, do the following:\n\t1) Check this page and install the correct compiler for your version of python: https://blogs.msdn.microsoft.com/pythonengineering/2016/04/11/unable-to-find-vcvarsall-bat/\n\t2) Re-install winevt (pip install -U winevt)")
    # In-line mode
    from .winevt_build import ffibuilder
    ffi = ffibuilder()
    evtapi = ffi.dlopen("Wevtapi.dll")
    kernel32 = ffi.dlopen("Kernel32.dll")
