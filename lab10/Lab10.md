# Lab10: Nginx Configuration and proxy_pass Usage

There are 2 files attached here:
- `my_site` has to be located in /etc/nginx/sites-available/ and /etc/nginx/sites-enabled/
- `my_site.html` has to be located in /var/www/html/
To run the program you can open browser and tipe `http://localhost:8000` and `curl -i http://localhost:8000/api` or on the termunal tipe `curl -i http://localhost:8000` and `curl -i http://localhost:8000/api`

## What did I do?
I configured Nginx to serve static files and forwarded API requests using `proxy_pass`.

## Completed
- Installed and started Nginx.  
- Configured the server to serve an HTML file at `http://localhost:8000`.  
- Added a `location /api` block with `proxy_pass` to forward requests to a local API at `http://127.0.0.1:5000/`.  
- Added a `/api` route that returns the message **"hello!"**.  

## Result
Nginx successfully serves the website and forwards API requests.  
The `proxy_pass` parameter works correctly and the setup functions as expected.

