""" Defines an Event Log Query """

class Query:

    def __init__(self, path, query = None, direction = None):
        """
        path = The name of the channel or the full path to a log file that contains the events that you want to query. You can specify an .evt, .evtx, or.etl log file. The path is required if the Query parameter contains an XPath query; the path is ignored if the Query parameter contains a structured XML query and the query specifies the path.
        query = A query that specifies the types of events that you want to retrieve. You can specify an XPath 1.0 query or structured XML query. If your XPath contains more than 20 expressions, use a structured XML query. To receive all events, set this parameter to None or "*".
        direction = query "forward" or "backward" from your search.
        """

        # TODO: Allow credential passing
        # TODO: Allow remote querying

        self.path = path
        self.query = query or "*"
        self.direction = direction

        # Grab a handle to this query
        self.handle = evtapi.EvtQuery(ffi.NULL, self.path, self.query, self.flags)

    def __del__(self):
        # Be sure to clean up our query
        try:
            evtapi.EvtClose(self.handle)
        except:
            pass

    def __repr__(self):
        return "<Query path={0} query={1}>".format(self.path, self.query)

    # We'll handle the iterator ourself
    def __iter__(self):
        return self

    def __next__(self):
        # Loop until we get no more events
        # TODO: Check for errors on fail

        # Creating new objects each time
        evt_array = ffi.new("EVT_HANDLE *")
        ret = ffi.new("PDWORD")

        if not evtapi.EvtNext(self.handle, 1, evt_array, 60, 0, ret):
            # TODO: Check for errors (GetLastError())
            raise StopIteration

        return Event(ffi.unpack(evt_array, 1)[0])


    ##############
    # Properties #
    ##############

    @property
    def flags(self):
        """ Flags to be used for this query. """
        flags = 0
        
        # Add forward and back
        if self.direction == "forward":
            flags |= evtapi.EvtQueryForwardDirection

        else:
            flags |= evtapi.EvtQueryReverseDirection

        # Determine if we're talking about a file
        if os.path.isfile(self.path):
            flags |= evtapi.EvtQueryFilePath

        else:
            flags |= evtapi.EvtQueryChannelPath

        return flags


    @property
    def path(self):
        """The name of the channel or the full path to a log file that contains the events that you want to query. You can specify an .evt, .evtx, or.etl log file. The path is required if the Query parameter contains an XPath query; the path is ignored if the Query parameter contains a structured XML query and the query specifies the path."""

        return self.__path

    @path.setter
    def path(self, path):
        # TODO: Error and type checking
        self.__path = path

    @property
    def query(self):
        """A query that specifies the types of events that you want to retrieve. You can specify an XPath 1.0 query or structured XML query. If your XPath contains more than 20 expressions, use a structured XML query. To receive all events, set this parameter to NULL or "*" """
        return self.__query

    @query.setter
    def query(self, query):
        # TODO: Error and type checking
        self.__query = query

    @property
    def direction(self):
        """The direction to move from your search. Options are "forward" (default) and "backward"."""
        return self.__direction

    @direction.setter
    def direction(self, direction):

        if type(direction) not in [type(None), str]:
            raise Exception("Invalid direction of type {0}".format(type(direction)))
        
        # Normalize it
        if direction is None:
            direction = "forward"

        else:
            direction = direction.lower()

        if direction not in ["forward","backward"]:
            raise Exception("Invalid direction recieved. Valid options are \"forward\" and \"backward\"")

        self.__direction = direction

import os
from .. import ffi, evtapi
from winevt.EventLog.Event import Event
