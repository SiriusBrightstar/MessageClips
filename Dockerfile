FROM python:slim

LABEL maintainer="siriusbrightstar@protonmail.com"
LABEL author="SiriusBrightstar"
LABEL github="https://github.com/SiriusBrightstar"
LABEL project="MessageClips"

COPY messageclips/main.py /
COPY messageclips/.env /
COPY messageclips/customLogger.py /
COPY requirments.txt /

RUN pip3 install -r /requirments.txt

WORKDIR /

CMD ["python3", "main.py"]
