# Request1
Request1 is a developer testing tool meant for Probing &amp; Testing Websites.
## Commands

```
-n  <num>        requests to send
-c  <num>        concurrency level
-k               keep-alive
-data <str|file> body & formdata
```

### HTTP methods
```
-get   -post   -put   -delete   -patch   -head   -options
-postform       POST with application/x-www-form-urlencoded
```

### Other protocols
```
-tcp            raw TCP
-udp            raw UDP
```

### Port scanner
```
-portscan -any                    scans as much ports as possible
-portscan -select,80,443,22       scan specific ports
```

---

## Examples

```
-n 1   -c 1  -get     http://example.com
-n 100 -c 10 -k -get  http://example.com
-n 1   -c 1  -post    -data payload.txt      http://example.com/api
-n 1   -c 1  -postform -data "user=a&pass=b" http://example.com/login
-n 1   -c 1  -put     -data update.txt       http://example.com/items/1
-n 1   -c 1  -delete  http://example.com/items/1
-portscan -any                    http://example.com
-portscan -select,80,443,8080     http://example.com
-n 5   -c 5  -tcp     http://example.com:9000
-n 1   -c 1  -udp     http://example.com:5353
```

---
