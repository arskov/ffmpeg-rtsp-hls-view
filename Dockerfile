FROM linuxserver/ffmpeg:version-4.3-cli
ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.8.5
WORKDIR /opt/ffmpeg-rtsp-hls
COPY . .
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev
RUN git clone https://github.com/pyenv/pyenv.git /opt/pyenv
ENV PYENV_ROOT="/opt/pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"
ENV PYENV_VERSION=${PYTHON_VERSION}
RUN pyenv install -v ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}
ENV PATH="/opt/pyenv/versions/${PYTHON_VERSION}/bin:$PATH"
RUN python -m pip install --upgrade pip && python -m pip install pipenv && pipenv sync
EXPOSE 8080
ENTRYPOINT ["pipenv", "run"]
CMD ["python", "-m", "webserver"]
