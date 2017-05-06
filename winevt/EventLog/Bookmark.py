""" Abstract a Windows Event Bookmark """

import logging
logger = logging.getLogger("winevt.EventLog.Bookmark")

BOOKMARK_SIZE = 512

class Bookmark:

    def __init__(self, xml = None):
        """
        xml = optional, instantiate this bookmark with saved xml (string)
        """

        self.__set_xml = xml
        self.handle = None

    def update(self, event):
        """ Update this bookmark from an Event or EventID. Returns bool successful or not."""
        if type(event) not in [Event, ffi.CData]:
            raise Exception("Attempting to update bookmark from invalid type {0}".format(type(event)))

        # Grab the Event ID if needed
        if type(event) is Event:
            event = event.handle

        if not evtapi.EvtUpdateBookmark(self.handle, event):
            logger.error(get_last_error())
            return False

        return True

    def __repr__(self):
        return "<Bookmark>"

    ##############
    # Properties #
    ##############

    @property
    def xml(self):
        """ Return this bookmark as an xml. """

        buf = ffi.new("PVOID[{0}]".format(int(BOOKMARK_SIZE/8)))
        ret = ffi.new("PDWORD")
        ret2 = ffi.new("PDWORD")

        if not evtapi.EvtRender(ffi.NULL, self.handle, evtapi.EvtRenderBookmark, BOOKMARK_SIZE, buf, ret, ret2):
            logger.error(get_last_error())

        return ffi.string(ffi.cast("wchar_t *",buf))

    @xml.setter
    def xml(self, xml):
        # Set the local XML value to be used when handle is called

        if type(xml) not in [type(None), str]:
            raise Exception("Invalid type for xml of {0}".format(type(xml)))

        self.__xml = xml


    @property
    def handle(self):
        """ EVT_HANDLE for this bookmark. """

        if self.__handle is not None:
            return self.__handle

        inp = ffi.new("wchar_t[{0}]".format(len(self.__set_xml)),self.__set_xml) if self.__set_xml is not None else ffi.NULL
        handle = evtapi.EvtCreateBookmark(inp)

        if handle == ffi.NULL:
            logger.error(get_last_error())
            return

        self.__handle = handle

        return handle

    @handle.setter
    def handle(self, handle):

        if type(handle) not in [type(None), ffi.CData]:
            raise Exception("Invalid type for handle of {0}".format(type(handle)))

        self.__handle = handle



from .. import ffi, evtapi, get_last_error
from .Event import Event
