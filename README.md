# CCLR Code Test
## Part One
### Convert XML to JSON
Using Python Version 3.12.0 and a basic Flask installation, created a function implementing the [requests](https://pypi.org/project/requests/) module to submit an http request to provided URL.
The function, called "pullparcel(pn)" accepts one input and performs a basic verification with regular expressions to match the expected format before calling the request.
Using [xmltodict](https://pypi.org/project/xmltodict/) and [json](https://docs.python.org/3/library/json.html) modules, convert the XML data to a native Python dictionary that then can be converted by the json module to json format.
The ***requests*** and ***xlmtodict*** should be the only two pip libraries that would need to be installed.

## Part Two - (A)
*Using fetch() to pull in JSON from Part One*
### Front-End Presentation *with Bootstrap and Vanilla JS*
The Google API Key will need to be inserted at the bottom of the page around line 184. Look for `[APIKEY]` in the URL.
Using Bootstrap and Vanilla JavaScript, I pulled in the JSON data with fetch and then populated the relevent elements of the HTML page. This was a rework of what I created initially using Flask to host the pages.
The page is named `index.html` and is in the root directory of the repo. The page has navigation buttons at the top for each of the respective parcels from Part One. The buttons call the `pullParcel()` function which then loads the JSON, then populates out to the Google Map and their respective HTML elements. I added a "spinner" that runs every time a new parcel is loaded. 

## Part Two - (B)
*Using Flask to render the HTML pages, was not part of Code Test*
### Front-End Presentation as a *Python Application*
The location to insert the Google Maps API KEY is line 9 of the `app.py` file in the root directory.
Using the initial Flask installation from part one, developed public facing html pages. The home page has two sets of links configured as buttons. The left side takes you to the parcel detail page, the ones on the right take you to a page that displays the converted XML to JSON data, displayed with `<pre></pre>` tags for ease of reading. The detail page pulls in the property image provided for the test. Google maps are also pulled in and the marker indicating the location of the property displays list the address and the year built. Other data could be included as needed. 

## Part Three
### 1. Unique Name and Phone Number of inspectors who inspected 812-12-027
Answer: Emma Johnson, (216) 555-1234
Joined Parcels to Inspection_Parcel join table
```sql
select unique(inspectors.name), phone from parcels
join inspection_parcel on parcels.id = inspection_parcel.parcel_id 
join inspections on inspection_parcel.inspection_id = inspections.inspector
join inspectors on inspections.inspector = inspectors.id
where ppn = "812-12-027"
```
### 2. Total cost of all inspections in East Cleveland.
Answer: $23,300.00
```sql
select sum(inspections.cost_per_parcel) from parcels
join inspection_parcel on parcels.id = inspection_parcel.parcel_id 
join inspections on inspection_parcel.inspection_id = inspections.inspector
where address like "%East Cleveland%"
```
### 3. All addresses of parcels not inspected since January 1, 2023
When I wrote the query, I found all properties and used max() to find the most recent inspection date. If the property had no inspections performed, the result was NULL so I added that as well. 
Answer:
- "3134 W 18 St Cleveland, OH"
- "13908 Potomac Ave East Cleveland, OH"
- "10213 Union Ave Cleveland, OH"
- "1767 Elberon Ave East Cleveland, OH"
- "18104 Garden Blvd Warrensville Heights, OH"
- "3314 Tullamore Cleveland Heights, OH"
- "1209 E 125th St East Cleveland, OH"


```sql
select inspection_report.address
from
(select parcels.id, address, max(inspections.date) as last_inspection_date 
from parcels
left join inspection_parcel on parcels.id = inspection_parcel.parcel_id 
left join inspections on inspection_parcel.inspection_id = inspections.id
group by parcels.id
) inspection_report
where last_inspection_date < '2023-01-01' or last_inspection_date is null
```
