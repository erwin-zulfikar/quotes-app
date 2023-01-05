import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# simpan alamat situs dalam variabel url
url: str = "https://quotes.toscrape.com"


class Crawler(object):
    def __init__(self, url: str):
        self.url = url
        self.headers: dict = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
        }

# buat fungsi untuk request url (ekstraksi data) dan scraping
    def get_quotes(self, url: str):
        res = requests.get(url, headers=self.headers)
        # cetak kode status request ke url apakah berhasil atau tidak
        # print(res.status_code)
        # cek apakah koneksi ke situs berhasil (kode status = 200)
        if res.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")

        # proses scraping data
        contents = soup.find_all("div", attrs={"class": "quote"})
        quotes_list: list = []

        # looping isi konten quotes dan ditampilkan dalam bentuk yang lebih rapi
        for content in contents:
            quote = content.find("span", attrs={"class": "text"}).text.strip()
            author = content.find("small", attrs={"class": "author"}).text.strip()

            # ambil url detail
            author_detail = content.find("a")['href']

            # buat data dictionary untuk menampung hasil tadi
            data_dict: dict = {
                "quote": quote,
                "quotes by": author,
                "author detail": url + author_detail,
            }

            quotes_list.append(data_dict)

        # proses pengolahan data dan tampilkan dalam bentuk file json
        with open("quotes.json", "w+") as f:
            json.dump(quotes_list, f)

        print("Data Berhasil di Generate")
        return quotes_list

    def get_detail(self, detail_url: str):
        res = requests.get(detail_url, headers=self.headers)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")

            # proses scraping
            author_title = soup.find("h3", attrs={"class": "author-title"}).text.strip()
            born = soup.find("span", attrs={"class": "author-born-date"}).text.strip()
            location = soup.find("span", attrs={"class": "author-born-location"}).text.strip()
            description = soup.find("div", attrs={"class": "author-description"}).text.strip()

            # proses mapping
            data_dict = {
                "author": author_title,
                "born": born,
                "born location": location,
                "description": description,
            }

            return data_dict

    def generate_format(self, filename: str, results: list):
        df = pd.DataFrame(results)
        if ".csv" or ".xlsx" not in filename:
            df.to_csv(filename + ".csv", index=False)
            df.to_excel(filename + ".xlsx", index=False)

        print("Data Generated ke file CSV dan Excel")

    def crawling(self):
        results: list[dict[str, str]] = []

        quotes: list = self.get_quotes(url=url)
        for quote in quotes:
            detail = self.get_detail(detail_url=quote['author detail'])
            final_result: dict = {**quote, **detail}
            results.append(final_result)

        # olah data
        self.generate_format(results=results, filename="reports")


if __name__ == '__main__':
    scraper: Crawler = Crawler(url=url)
    scraper.crawling()
