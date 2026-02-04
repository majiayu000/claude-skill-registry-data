---
name: identity
description: Query identity change logs to explore profile creation and merging
---

# Identity

This skill is used when the user asks about identity stitching, id stitching or wants to explore real time profiles. It involves querying a table called id_changes which is a log updated by the application when id changes occur.

Treasure Data's real time service includes creation and management of real time profiles. Profiles are updated based on a stream of event records that contain one or more "id stitching key" properties. The identity of a profile consists of both an internal Rid (real time Id) and one or more stitching keys. The system creates new profiles when the keys are all unique. It updates a profile when a new key is found that was not previously associated with other keys in the record. It can also stitch multiple profiles together when we find that keys in the record exist in two or more existing profiles. We combine the profiles together and the rid with the earliest date is the kept whilst the other profiles are merged and deleted. 

# Description

## Requirements

In order to query the id changes log we must know the parent segment the customer is interested in. A customer may have a number of parent segments so we must ask them to provide the one they are interested in before making a query. A segment ID will be a numeric value like 411671.

The user must also have a correctly configured tdx-skill or the Treasure Data mcp server (@treasuredata/mcp-server) to enable the database lookup.

In addition the api key with appropriate access to the database table should be available and configured.

## Database

The database name contains the parent segment ID and has this format cdp_audience_394649_rt. This is where you can plug in the parent segment the user gives in the request.

## id_changes table

The id_changes log table is always called id_changes and is in the Parent Segment real time database.

## Schema

The id_changes table has the following schema. The format of the schema below is:

column name, type, description
time, int, unix timestamp of when the record was logged
event_type, string, always "id". It is not informative.
key_values, string, always "NA" or null. It has no information.
reactor_instance_id, string, for customer support assistance this can be useful for the engineering team
profile_change_type, string, "profile_added" or "profile_updated_by_stitching" or "profile_deleted_by_stitching" that determines what caused the change
current_id_attributes, string, A json array of key value colon separated strings showing the known id keys for the profile. For example ["customer_id:3001"] This is only valid when profile_change_type is profile_added
current_rid, string, internal unique identifier for this realtime profile in UUID v7 string format for example 0199f0ad-13b8-7c3d-9fab-b5fb14ebe7cc
merged_rids, string, json string showing which rids were merged during a stitching process as a json array for example ["019a9e30-8407-76ff-a67b-b1576b72cf12"]


## Understanding stitching

### New profiles

When you see profile_change_type is profile_added that means a new profile is created and the new rid will be in current_rid. This log entry is the only one where the current_id_attributes is populated. You can determine the attributes of merged profiles by taking the union of their initial attributes when the profile was created. 

### Updated profiles

Sometimes you may see profile_change_type is profile_updated_by_stitching and merged_rids is just an empty array. This means a profile was updated but it is not useful information for identity purposes.

### Merged profiles

In this case it means multiple profiles were merged. 

There will be a row for each identity deleted and one for the oldest profile. They have the following properties.

For each deleted profile the profile_change_type is profile_deleted_by_stitching.
For the oldest profile the others are merged into the profile_change_type is profile_updated_by_stitching and the merged_rids column will have the json array of the rids. 

## Query tips

If the user does not specify a time range assume the last 24 hours. Use a where clause like `TD_INTERVAL(time, '-1d/now')`

Rather than show the time as a timestamp it is useful to convert it to a human friendly string using TD_TIME_FORMAT(time, 'yyyy-MM-dd HH:mm:ss', 'GMT'). The user may specify a different time zone.
Sample trino/presto query to get 8 hours of logs.

```
select TD_TIME_FORMAT(time, 'yyyy-MM-dd HH:mm:ss', 'PST'), *
from id_changes
where 
TD_INTERVAL(time, '-8h/now')
order by time desc;
```

When you need to access the key value pairs in current_id_attributes the following query helps extract it.

```
WITH data AS (
    SELECT '["customer_id:customer test 4","cookie_id:abcdei"]' AS raw_col
)
SELECT 
    -- This creates: {customer_id=customer test 4, cookie_id=abcdei}
    map(
        transform(parsed_arr, x -> split_part(x, ':', 1)), -- Extract keys
        transform(parsed_arr, x -> split_part(x, ':', 2))  -- Extract values
    ) AS kv_map
FROM (
    SELECT CAST(json_parse(raw_col) AS ARRAY(VARCHAR)) AS parsed_arr 
    FROM data
)
```

Some likely queries the customer may want:

How many new profiles did we get in a time period? Search and count the rows where add_profile occurs in profile_change_type.
You can discover the number merged profiles by counting where profile_change_type is profile_updated_by_stitching.
Similarly you can determine the number of deleted profiles by counting profile_deleted_by_stitching in the time period.

Customers can query by identifier to ask for the history of a profile, in which case you should search the current_id_attributes as above to identify the rid and then the merge history.
