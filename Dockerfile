FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt requirements.lock ./
RUN python -m pip install --no-cache-dir -c requirements.lock -r requirements.txt
COPY cli.py contract.py ./
COPY examples ./examples/
USER 10001:10001
CMD ["python","cli.py","validate","--contract","SampleContract","--file","examples/valid.json"]
