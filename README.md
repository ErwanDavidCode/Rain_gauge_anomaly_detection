# Rain_gauge_anomaly_detection
The purpose of these programs, written in Python, is to detect
anomalies in the rainfall totals of a network of rain gauges.
rain gauges.
The cumulative rainfall period chosen is monthly. It
regular checks (12 times a year) and avoids local high intensity phenomena
and avoids phenomena of high local intensity by smoothing observa>ons over a month.
over a month.

Potential anomalies in the rain gauges observed are detected by
by comparing their accumulations :
- between neighbouring rain gauges
- between rain gauges and precipitation radars.

The processing results in a list of rain gauges for which the monthly
for which the monthly totals appear abnormal. These are the
These are the rain gauges that need to be checked and repaired on site.