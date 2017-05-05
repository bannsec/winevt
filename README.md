# Overview
This is a library to interact with the Windows Event Logging system. The focus is to interact directly with the Windows API, rather than parsing evt files. This will allow you to use python to parse events as well as subscribe to providers.

# Install
`winevt` can be installed directly as a package from pypi. I recommend you install it into a python virtual environment.

```bash
$ mkvirtualenv --python=$(which python3) winevt # Optional
(winevt)$ pip install winevt
```

# Current Features
Currently, this library supports querying and subscribing to event logs or parsing of event log files. Because this library uses the Windows API directly, you can query for any of the reigstered event providers.

# Example
## Query

Let's say you want to review the error report alerts that are in your Application event log. To print out all the times you dropped a dump file, you could do the following:

```python
In [1]: from winevt import EventLog

In [2]: query = EventLog.Query("Application","Event/System/Provider[@Name='Windows Error Reporting']")

In [3]: for event in query:
   ...:     for item in event.EventData.Data:
   ...:         if "dmp" in item.cdata:
   ...:             print(item.cdata)
```

If you were interested in seeing every time you had an error or critical event from the System, you could do:

```python
In [1]: from winevt import EventLog

In [2]: query = EventLog.Query("System","Event/System[Level>=2]")

In [3]: for event in query:
   ...:     print(event.System.Provider['Name'])
```

