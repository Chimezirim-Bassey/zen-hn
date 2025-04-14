FROM python:3.12-alpine

LABEL author="Ichinga Samuel"

ARG USERNAME=zen_hacker
ARG GROUPNAME=zen_hackers
ARG USERID=1000
ARG GROUPID=$USERID

RUN addgroup -S $GROUPNAME && adduser -D -S $USERNAME -G $GROUPNAME -u $USERID

USER $USERNAME

WORKDIR /web/zen_hn

COPY requirements.txt /web/zen_hn

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt

COPY . /web/zen_hn

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
