""" Define an Event """

class Event:

    def __init__(self, handle, max_buf_size=None):
        """
        handle = event handle (such as returned by Query)
        max_buf_size = optionally set the max buffer size for returning things. Defaults to 8192
        """

        self.handle = handle
        self._max_buf_size = max_buf_size or 8192


    ##############
    # Properties #
    ##############

    @property
    def xml(self):
        """ Returns the full XML dump of the event. """

        # Create some vars
        ret = ffi.new("PDWORD")
        ret2 = ffi.new("PDWORD")
        buf = ffi.new("PVOID[{0}]".format(int(self._max_buf_size/8)))

        if not evtapi.EvtRender(ffi.NULL, self.handle, evtapi.EvtRenderEventXml, self._max_buf_size, buf, ret, ret2):
            raise Exception("Something failed when trying to render...")

        # Return the buf
        return ffi.string(ffi.cast("wchar_t *",buf))
    
    @property
    def handle(self):
        return self.__handle

    @handle.setter
    def handle(self, handle):
        
        if type(handle) is not ffi.CData:
            raise Exception("handle must be of type ffi.CData")

        self.__handle = handle


from _winevt import ffi, lib as evtapi
