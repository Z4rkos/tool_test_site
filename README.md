# tool_test_site
A simple flask app for testing web enumeration tools i've made.
It has 0 security as that was the point of making it.

I originally made this for a school project to "Explain, Examine, and Exploit" some basic web vulnerabilities, but now I just use it to test tools.


## How to use:
Clone the repo:
```
git clone https://github.com/Z4rkos/tool_test_site
```

Cd into the repo:
```
cd tool_test_site
```

Use docker-compose to build and start:
```
docker-compose up
```
NOTE: It will restart a number of times when it initially get's built as MySQL uses alot longer time to start compared to the website.


## Vulnerabilities:
- Username enumeration
- Password enumeration
- SQLi (all over the place)
- XSS


Im not really doing anything with this atm, just wanted to put it up here, but at some point I'll add some more vulnerabilities.
