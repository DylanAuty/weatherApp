# weatherProj
A simple one-page weather app, written using Django and PostgreSQL.

## Dependencies

## Launch

## Stack overview
### Backend
The app backend is built using Django, with a PostgreSQL database.
For deployment, the server used is an AWS Micro Instance running Ubuntu Server 16.04. The web server chosen was NGINX, with uWSGI to interface with the Django app.

### Frontend
The frontend uses HTML/CSS, with Bootstrap v.3.3.7. Javascript and JQuery are used, and the search box makes use of AJAX. Bootstrap and JQuery are not hosted locally, to decrease overhead.

## Testing and Optimisation

### Function Testing
Function testing was performed manually, due to the small scale of the application.

### Performance Testing.
To test performance, the Chrome Dev Tools, ApacheBench, and EXPLAIN commands issued directly to the PostgreSQL command prompt were used.

- ApacheBench: `ab -n 1000 -c 10 http://127.0.0.1:8000/` Issues 1000 requests with a maximum concurrency of 10 requests at once.
- Developer tools: Used to get a cursory, high-level overview of page bottlenecks (esp. TTFB and AJAX queries).
- EXPLAIN: The costs returned provide performance overviews of a given query, and allow detection of inefficient commands.

#### Landing page, no optimisation: ApacheBench Results
```
Concurrency Level:      10
Time taken for tests:   33.198 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      12085000 bytes
HTML transferred:       11743000 bytes
Requests per second:    30.12 [#/sec] (mean)
Time per request:       331.976 [ms] (mean)
Time per request:       33.198 [ms] (mean, across all concurrent requests)
Transfer rate:          355.50 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.6      0       7
Processing:   171  331  68.4    322    1022
Waiting:      169  299  71.9    291     989
Total:        171  332  68.8    322    1028

Percentage of the requests served within a certain time (ms)
  50%    322
  66%    336
  75%    344
  80%    351
  90%    369
  95%    392
  98%    446
  99%    625
 100%   1028 (longest request)
```

### Database Optimisation
With no caching or optimisation, the PostgreSQL logs show that each load of the front page performs at best 5 SELECT queries (location and forecast known and present in DB), and at worst 2 SELECTs, 5 INSERTs, and a further 5 SELECTs (location and forecast both missing from DB). By reducing the amount of queries overall, and optimising those that do get executed, performance can be improved.

The number of queries could be reduced by condensing the 4 database queries for the forecasts into a single, more complex query.

#### Forecast selection
PostgreSQL's EXPLAIN command was used to evaluate the search strategy for the forecast SELECTion commands. It revealed that an index scan was used for the location, but date filtering was performed using a full table scan, with an estimated total cost of 12.91.


##### Before:
Sequential scan for date, index scan for location with filter on api\_ref\_string. 

```
 Limit  (cost=12.91..12.92 rows=1 width=411) (actual time=0.085..0.086 rows=1 loops=1)
   ->  Sort  (cost=12.91..12.92 rows=1 width=411) (actual time=0.084..0.084 rows=1 loops=1)
         Sort Key: "weatherApp_forecast".retrieved DESC
         Sort Method: quicksort  Memory: 25kB
         ->  Nested Loop  (cost=0.14..12.90 rows=1 width=411) (actual time=0.066..0.068 rows=1 loops=1)
               ->  Seq Scan on "weatherApp_forecast"  (cost=0.00..4.74 rows=1 width=411) (actual time=0.033..0.038 rows=3 loops=1)
                     Filter: (date = '2017-04-02'::date)
                     Rows Removed by Filter: 61
               ->  Index Scan using "weatherApp_location_pkey" on "weatherApp_location"  (cost=0.14..8.16 rows=1 width=4) (actual time=0.007..0.007 rows=0 loops=3)
                     Index Cond: (id = "weatherApp_forecast".location_id)
                     Filter: ((api_ref_string)::text = '/q/zmw:00000.1.54511'::text)
                     Rows Removed by Filter: 1
 Planning time: 0.320 ms
 Execution time: 0.185 ms
(14 rows)

```
To remedy the sequential scanning and the slow filtering over what should be a unique value, I altered the database so that:
- forecast.date and forecast.retrieved were indexed.
- location.api\_ref\_string became a primary key.

##### After:
As a result of the above operation, performance of this query was improved. Multiple scans were condensed into one which was able to filter by multiple conditions at once due to addition of indexing and the primary key setting of the location api\_ref\_string.

```
 Limit  (cost=4.97..4.97 rows=1 width=822) (actual time=0.053..0.053 rows=1 loops=1)
   ->  Sort  (cost=4.97..4.97 rows=1 width=822) (actual time=0.052..0.052 rows=1 loops=1)
         Sort Key: retrieved DESC
         Sort Method: quicksort  Memory: 25kB
         ->  Seq Scan on "weatherApp_forecast"  (cost=0.00..4.96 rows=1 width=822) (actual time=0.040..0.040 rows=1 loops=1)
               Filter: ((date = '2017-04-02'::date) AND ((location_id)::text = '/q/zmw:00000.1.03772'::text))
               Rows Removed by Filter: 67
 Planning time: 0.210 ms
 Execution time: 0.102 ms
(9 rows)

```

### Caching
The landing page was cached using Memcached via the Django view. The performance improvement was significant. Expiry was set at 15 minutes, as this is the frequency of updates from Wunderground.

#### Django and Memcached - Application level caching
In this case, a request must reach the Django server in order for the cached copy to be recalled, which adds overhead. However, it is very swift to implement and yields good results.

##### Before:
No caching. ApacheBench used - 1000 requests with 10 max. concurrent connections.

```
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   1.1      0      12
Processing:   107  326  57.8    318     833
Waiting:      105  293  60.1    286     762
Total:        107  326  58.6    318     845

```

##### After:
Basic caching at application level using Memcached. For landing page only. 15 minute timeout.

```
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.6      0       7
Processing:     4   24  37.0     19     404
Waiting:        2   19  36.6     15     396
Total:          4   24  37.6     19     411

```
This has caused a more than tenfold mean improvement in server response time, from a mean total of 326ms down to 24ms.

In addition, the 15 minute timeout on the cache means it is no longer necessary to check for the existence of forecasts and locations in the database before fetching them - they can be fetched naively and will be up to date, with no additional overhead.

#### NGINX and Memcached - Server level caching
NGINX could be used to speed up the delivery of static files, eliminating unnecessary calls to the Django app. This has not been implemented yet, but the performance increase would be minimal since the session-level caching must reach the Django app anyway, and the site is static resource light.





