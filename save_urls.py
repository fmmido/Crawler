import datetime

visited_urls = set()

def save_urls():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crawled_urls_{timestamp}.txt"
    with open(filename, 'w') as file:
        for url in sorted(visited_urls):
            file.write(f"{url}\n")
    print(f"URLs saved to {filename}")
