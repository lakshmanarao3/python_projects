import requests
from bs4 import BeautifulSoup

queries = ["Lakshmanarao Pokuri", "Lakshmana Rao Pokuri", "Lakshmana Rao", "LakshmanaRao"]

for query in queries:
    print(f"Results for query: {query}\n")
    
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
            
            print("Title:", title)
            print("Link:", link)
            print("Description:", description)
            print("\n")

    print("\n")



