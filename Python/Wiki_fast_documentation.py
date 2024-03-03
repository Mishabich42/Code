import requests
from bs4 import BeautifulSoup
from docx import Document



def parse():
    Choise = input("Enter language as en, uk:")
    url = f"https://{Choise}.wikipedia.org/wiki/"
    Input = input("Seach:")
    Input = Input.replace(" ", "_")
    print(url + Input)
    cite = requests.get(url + Input)
    if cite.status_code == 200:
        soup = BeautifulSoup(cite.text, features="html.parser")
        header = soup.find("header")
        footer = soup.find("footer")
        if header:
            header.extract()
        if footer:
            footer.extract()
        soup_list = soup.find_all("a")
        clean_text = soup_list[0].get_text().replace("\xa0", " ").replace("<i>", "").replace("</i>", "")
        for a in soup.find_all('div', href=True):
            if 'title' in a.attrs:
                p = soup.new_tag("p")
                p.string = a['title']
                soup.append(p)
        soup.append(clean_text)
        soup = soup.get_text()
        soup = str(soup)
        choise = input("File format:")
        if choise == "docx":
            document = Document()
            document.add_paragraph(str(soup))
            document.save(f"{Input}.docx")
        else:
            pdf = open(f"{Input}.{choise}", "w", encoding="utf-8")
            pdf.write(str(soup))
            pdf.close()
    else:
        print("Not found")

parse()
