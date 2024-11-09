from winevt import EventLog
import win32evtlogutil
import win32evtlog

def test_query_system_log():
    query = EventLog.Query("System", "Event/System[Level<=2]")
    events = [event for event in query]
    assert len(events) > 0
    for event in events:
        assert event.System.Level.cdata in ['1', '2']

def test_create_error_event():
    APP_NAME = "My Python App"
    EVENT_ID = 1000
    EVENT_CATEGORY = 1
    EVENT_DESCRIPTION = ["This is a test error event"]
    EVENT_DATA = b"Additional binary data"

    win32evtlogutil.ReportEvent(
        APP_NAME,
        EVENT_ID,
        eventCategory=EVENT_CATEGORY,
        eventType=win32evtlog.EVENTLOG_ERROR_TYPE,
        strings=EVENT_DESCRIPTION,
        data=EVENT_DATA
    )

    query = EventLog.Query("Application", "*[System[Provider[@Name='My Python App'] and EventID=1000]]")
    events = [event for event in query]
    assert len(events) > 0
    for event in events:
        assert event.System.Provider['Name'] == APP_NAME
        assert event.System.EventID.cdata == str(EVENT_ID)
        assert event.EventData.Data[0].cdata == EVENT_DESCRIPTION[0]
