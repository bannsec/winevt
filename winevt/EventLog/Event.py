""" Define an Event """

LogLevels = {
        0: 'Undefined',
        1: 'Critical',
        2: 'Error',
        3: 'Warning',
        4: 'Information',
        5: 'Verbose'
}

class Event:

    def __init__(self, handle, max_buf_size=None):
        """
        handle = event handle (such as returned by Query)
        max_buf_size = optionally set the max buffer size for returning things. Defaults to 65536
        """

        self.__xml = None
        self.handle = handle
        self._max_buf_size = max_buf_size or 65536

        self.xml # Populate the event

    def __repr__(self):
        return "<Event EventID={0} Level={1}>".format(self.EventID, self.LevelStr)

    ##############
    # Properties #
    ##############

    @property
    def xml(self):
        """ Returns the full XML dump of the event. """

        # Basically cache it
        if self.__xml != None:
            return self.__xml

        # Create some vars
        ret = ffi.new("PDWORD")
        ret2 = ffi.new("PDWORD")
        buf = ffi.new("PVOID[{0}]".format(int(self._max_buf_size/8)))

        if not evtapi.EvtRender(ffi.NULL, self.handle, evtapi.EvtRenderEventXml, self._max_buf_size, buf, ret, ret2):
            raise Exception("Something failed when trying to render...")

        # Save the buf
        self.__xml = ffi.string(ffi.cast("wchar_t *",buf))

        # Untangle and save as attributes
        dom = untangle.parse(self.__xml)
        for child in dom.Event.children:
            if not hasattr(self, child._name):
                setattr(self, child._name, child)

        # Return the buf
        return self.__xml
    
    @property
    def handle(self):
        return self.__handle

    @handle.setter
    def handle(self, handle):
        
        if type(handle) is not ffi.CData:
            raise Exception("handle must be of type ffi.CData")

        self.__handle = handle

    @property
    def EventID(self):
        # Helper function. Not strictly necessary as you can parse the dom or XML
        return int(self.System.EventID.cdata)

    @property
    def Level(self):
        return int(self.System.Level.cdata)

    @property
    def LevelStr(self):
        return LogLevels[self.Level]


#from _winevt import ffi, lib as evtapi
from .. import ffi, evtapi
import untangle
