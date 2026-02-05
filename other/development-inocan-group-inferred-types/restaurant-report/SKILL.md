---
name: restaurant-report
description: Create report how many guests there where each day
---

# Restaurant report

## Instructions

### Google sheet
* Generate the report from the Google sheet specified in environment variable $LUNCH_GOOGLE_SHEET.
* Download the sheet as a CSV.

### Generate the report
* Summarize the number of guests per day for all dates that exist in the data.
* Make a list of dates and number of guests.

### Number of guests
* Count the number of guests, it is specified on the row marked "Total".

### Additional guests
* In the same column on the rows below there is freeform text about additional guests. These should be added to the total.

### Additional guests parsing rules
* If specified as "Person + n", it counts as n + 1.
* If specified as "n (Person)", it counts as n.

### Save the report to database
* Write the complete report in a database table in the chinook database.
* Connection info is specified in multiple environment variables on the format $CHINOOK*.
* If the table restaurant_report do not exist, then create it.
