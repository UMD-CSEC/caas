FROM python:3.12

RUN apt update -y
RUN apt install cowsay -y

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY static ./static
COPY templates ./templates
COPY readflag .
COPY flag.txt .

RUN mkdir uploads
RUN chown 1000:1000 uploads
RUN chown 1000:1000 static/cow_pics
RUN chmod =x+s readflag
RUN chmod 600 flag.txt
RUN ln -s /usr/games/cowsay /usr/bin/cowsay

EXPOSE 5000

CMD [ "python", "./main.py" ]
