import requests
from bs4 import BeautifulSoup
import http.server
import socketserver
import webbrowser
import os

queries = ["Lakshmanarao Pokuri", "Lakshmana Rao Pokuri", "Lakshmana Rao", "LakshmanaRao"]

# Open an HTML file for writing
with open("search_results.html", "w", encoding="utf-8") as html_file:
    # Write HTML header
    html_file.write("<html><head><title>Search Results</title></head><body>")
    
    for query in queries:
        html_file.write(f"<h2>Results for query: {query}</h2><br>")
        
        # Perform a Google search
        url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract website information
        search_results = soup.find_all("div", {"class": "g"})

        for result in search_results:
            link = result.find('a')['href']
            if link.startswith('http'):
                title = result.find('h3', {"class": "LC20lb MBeuO DKV0Md"}).text if result.find('h3', {"class": "LC20lb MBeuO DKV0Md"}) else None
                description = result.find('span', {"class": "aCOpRe"}).text if result.find('span', {"class": "aCOpRe"}) else None
                
                # Write result to HTML file
                html_file.write(f"<p><b>Title:</b> {title}</p>")
                html_file.write(f"<p><b>Link:</b> {link}</p>")
                html_file.write(f"<p><b>Description:</b> {description}</p><br>")

    # Write HTML footer
    html_file.write("</body></html>")

print("Search results written to search_results.html")

# Open a simple HTTP server to serve the HTML file
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

os.chdir(os.path.dirname(__file__))
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"HTTP server running on port {PORT}")
    httpd.serve_forever()
