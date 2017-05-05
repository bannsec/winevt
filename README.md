# Overview
This is a library to interact with the Windows Event Logging system. The focus is to interact directly, rather than parsing evt files. This will allow you to use python to parse events as well as subscribe to providers.

# Install
`winevt` can be installed directly as a package from pypi. I recommend you install it into a python virtual environment.

```bash
$ mkvirtualenv --python=$(which python3) winevt # Optional
(winevt)$ pip install winevt
```

# Current Features
Currently, this library supports querying of event logs or parsing of event log files. Because this library uses the Windows API directly, you can query for any of the reigstered event providers.

# Example
The following is an example of querying and then enumerating through the returned events.

```python
from winevt import EventLog

query = EventLog.Query("System","Event/System[Level=2]")

for event in query:
    print(event.System.Provider['Name'])
```

