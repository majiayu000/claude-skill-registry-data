---
name: evo-seismic-data-io
description: Loads MiniSEED waveform data and CSV station metadata, groups traces by station for 3-component processing, and provides station coordinate lookups.
---

# evo-seismic-data-io

Loads seismic waveform and station data using ObsPy and Pandas.

## Functions

- `load_waveforms(mseed_path)` - Returns ObsPy Stream
- `load_stations(csv_path)` - Returns pandas DataFrame
- `group_traces_by_station(stream)` - Returns dict of {net.sta: Stream}
- `get_station_dict(stations_df)` - Returns dict of {net.sta: {lat, lon, elev}}

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-seismic-data-io/scripts')
from utils import load_waveforms, load_stations, group_traces_by_station, get_station_dict

stream = load_waveforms('/root/data/wave.mseed')
stations_df = load_stations('/root/data/stations.csv')
station_streams = group_traces_by_station(stream)
station_dict = get_station_dict(stations_df)
```
