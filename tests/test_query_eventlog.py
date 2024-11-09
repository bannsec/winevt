import pytest
from winevt import EventLog, Query

def test_query_application_log():
    query = EventLog.Query("Application", "Event/System/Provider[@Name='Windows Error Reporting']")
    events = [event for event in query]
    assert len(events) > 0
    for event in events:
        assert event.System.Provider['Name'] == 'Windows Error Reporting'

def test_query_system_log():
    query = EventLog.Query("System", "Event/System[Level<=2]")
    events = [event for event in query]
    assert len(events) > 0
    for event in events:
        assert event.System.Level.cdata in ['1', '2']
