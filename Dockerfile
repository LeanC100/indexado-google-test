FROM python:3.8

RUN ln -fs /usr/share/zoneinfo/America/Buenos_Aires /etc/localtime 
RUN dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

ADD . .

COPY requirements.txt requirements.txt

RUN pip install  --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]

# BeautifulSoup.py

