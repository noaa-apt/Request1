# Request1 1.0.11.0 ~ Minor bug fixes
# Request1 1.0.13.0 is Released as Experimental! https://github.com/noaa-apt/Request1/releases
Request1 is a developer testing tool meant for Probing &amp; Testing Websites.

> [!CAUTION]
> **This tool is meant for Authorized use only.**
>
> This project is intended for security testing of websites and systems that you own or have explicit permission to assess. Do not use it against third-party systems without authorization, to disrupt services, to access data, or in violation of applicable laws or terms of service.
>
> You are responsible for confirming authorization, defining permitted targets and test scope, and complying with applicable requirements. Use conservative request rates, and stop testing if you observe service degradation or unexpected access to sensitive data.
>
> This project is provided “as is,” without warranties. The maintainers do not authorize or endorse unauthorized use and are not responsible for users’ actions or any resulting damage.



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

# Are you using version 1.0.13.0?

If so, & using ``-ubrute`` or ``-brute``, We give out wordlists for free!

Usernames starting in ``admin``: https://ssb.surf/admin.txt
Usernames starting in ``root``: http://ssb.surf/root.txt

---
1.0.13.0 is entirely experimental! Meaning it is partially released!
Common Mistakes with 1.0.13.0:

Are you using -brute and not getting a password in return? Use -ubrute for unofficial browser (native) popups.

Difference Between Official & Unofficial listed below as images.


<img width="257" height="205" alt="image" src="https://github.com/user-attachments/assets/ae09133d-7915-453d-9f59-c9418a87c22f" />

<img width="383" height="298" alt="image" src="https://github.com/user-attachments/assets/12ce5311-6cf0-472b-881f-cf0ce4d8a4a0" />

