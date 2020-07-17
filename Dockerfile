FROM python:3
ADD sendsms.py /
RUN pip3 install flask
RUN pip3 install kavenegar
CMD [ "python3", "-u","./sendsms.py" ]
