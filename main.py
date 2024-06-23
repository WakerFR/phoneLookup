import colorama
import requests
from bs4 import BeautifulSoup
import threading
import os

class ReverseLookup:
    def __init__(self):
        self.url = "https://www.comfi.com/abook/reverse"
        self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        self.working_proxy = None

    def get_organisation(self, number):
        proxies = {"http": f"http://{self.working_proxy}", "https": f"https://{self.working_proxy}"} if self.working_proxy else None
        try:
            response = requests.post(self.url, data={"phone_number": number}, headers={"User-Agent": self.userAgent}, proxies=proxies, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                data = {}
                for row in soup.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        key = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)
                        if key == "Country or destination":
                            value = cells[1].find('a').get_text(strip=True)
                        elif key == "City or exchange location":
                            link = cells[1].find('a')
                            value = link.get_text(strip=True) if link else ""
                        data[key] = value
                return data
            else:
                return {"Error": f"Request failed with status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"Error": f"Request error: {e}"}

    def process_numbers(self, numbers, proxies, output_dir):
        for number in numbers:
            while True:
                if not proxies:
                    self.working_proxy = None
                    break
                proxy = proxies.pop(0)
                if self.get_proxy(proxy):
                    break
            data = self.get_organisation(number)
            if "Country or destination" in data and "Original network provider" in data:
                print(colorama.Fore.LIGHTGREEN_EX, number, " >> ", data['Original network provider'], colorama.Fore.RESET)
                country_dir = os.path.join(output_dir, data["Country or destination"])
                os.makedirs(country_dir, exist_ok=True)
                operator_file = os.path.join(country_dir, f"{data['Original network provider']}.txt")
                with open(operator_file, "a") as f:
                    f.write(number + "\n")
            else:
                print(colorama.Fore.LIGHTRED_EX, number, " >> ", "No data found" if "Error" in data else "Data not available", colorama.Fore.RESET)

    def get_proxy(self, proxy) -> bool:
        proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
        try:
            response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
            if response.status_code == 200:
                self.working_proxy = proxy
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def start_threads(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(colorama.Fore.LIGHTMAGENTA_EX, r"""
 ___________.__                        __  .____                  __                 
 \_   _____/|  |  __ __   ____   _____/  |_|    |    ____   ____ |  | ____ ________  
  |    __)  |  | |  |  \_/ __ \ /    \   __\    |   /  _ \ /  _ \|  |/ /  |  \____ \ 
  |     \   |  |_|  |  /\  ___/|   |  \  | |    |__(  <_> |  <_> )    <|  |  /  |_> >
  \___  /   |____/____/  \___  >___|  /__| |_______ \____/ \____/|__|_ \____/|   __/ 
      \/                     \/     \/             \/                 \/     |__|    \n\n
""", colorama.Fore.RESET)
        input_file = input(colorama.Fore.LIGHTYELLOW_EX+"$ Enter numbers file path: " + colorama.Fore.RESET)
        numbers = [line.strip() for line in open(input_file, 'r').readlines()]

        self.proxies = input(colorama.Fore.LIGHTYELLOW_EX+"$ Enter proxies file path (optional): "+ colorama.Fore.RESET)
        proxies = [line.strip() for line in open(self.proxies, 'r').readlines()] if self.proxies else [None] * len(numbers)

        threads_num = int(input(colorama.Fore.LIGHTYELLOW_EX+"$ Enter number of threads: "+ colorama.Fore.RESET))
        output_dir = "results"  
        os.makedirs(output_dir, exist_ok=True)

        num_per_thread = len(numbers) // threads_num
        threads = []
        for i in range(threads_num):
            start = i * num_per_thread
            end = start + num_per_thread if i < threads_num - 1 else len(numbers)
            t = threading.Thread(target=self.process_numbers, args=(numbers[start:end], proxies[start:end], output_dir))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print(f"[+] Reverse Lookup Finished. Results saved to {output_dir}")

if __name__ == "__main__":
    reversed_lookup = ReverseLookup()
    reversed_lookup.start_threads()
