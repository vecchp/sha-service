FROM pypy:3-5.10.1

ARG TEST_MODE
RUN if [ "${TEST_MODE}x" != "x" ] ; then pip install pytest==3.5.0; fi

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD pypy3 -m shaservice.main

