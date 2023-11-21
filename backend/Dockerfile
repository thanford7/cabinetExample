# syntax=docker/dockerfile:1

# using ubuntu LTS version
FROM ubuntu:22.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3.10-venv python3.10-dev python3-pip python3-wheel build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.10 -m venv /cabinet/venv
ENV PATH="/cabinet/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:22.04 AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3.10-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder-image /cabinet/venv /cabinet/venv

RUN mkdir /cabinet/code
WORKDIR /cabinet/code
COPY . .

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/cabinet/venv
ENV PATH="/cabinet/venv/bin:$PATH"