FROM python

WORKDIR /opt

COPY . /opt

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run_app.py"]