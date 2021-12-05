# https://aws.amazon.com/jp/blogs/aws/new-for-aws-lambda-container-image-support/
ARG FUNCTION_DIR="/home/app"
ARG RUNTIME_VERSION="3.9"
ARG DISTRO_VERSION="3.14"
ARG GROUP_NAME="appgroup"
ARG USER_NAME="app"

# Stage 1 - bundle base image + runtime
FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine
# Install GCC (Alpine uses musl but we compile and link dependencies with GCC)
RUN apk add --no-cache \
    libstdc++

# Stage 2 - build function and dependencies
FROM python-alpine AS build-image
RUN apk add --no-cache \
    build-base \
    libtool \
    autoconf \
    automake \
    libexecinfo-dev \
    make \
    cmake \
    libcurl \
    curl
ARG FUNCTION_DIR
ARG RUNTIME_VERSION
RUN mkdir -p ${FUNCTION_DIR}
COPY app/ ${FUNCTION_DIR}/app
ENV PATH="${PATH}:/root/.poetry/bin"
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > tmpfile && mv tmpfile requirements.txt
RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}

# Stage 3 - final
FROM python-alpine
ARG GROUP_NAME
ARG USER_NAME
RUN addgroup ${GROUP_NAME} \
    && adduser --disabled-password --ingroup ${GROUP_NAME} ${USER_NAME}
USER ${USER_NAME}
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY --from=build-image --chown=${USER_NAME}:${GROUP_NAME} ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["app/main.handler" ]
