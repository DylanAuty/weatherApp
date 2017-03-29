# weatherProj
A simple one-page weather app, written using Django and PostgreSQL.

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
* ApacheBench: `ab -n 1000 -c 10 http://127.0.0.1:8000/` Issues 1000 requests with a maximum concurrency of 10 requests at once.
* Developer tools: Used to get a cursory, high-level overview of page bottlenecks (esp. TTFB and AJAX queries).
* EXPLAIN: The costs returned provide performance overviews of a given query, and allow detection of inefficient commands.

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

### Caching


