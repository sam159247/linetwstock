# https://github.com/microsoft/vscode-dev-containers/tree/main/containers/python-3
ARG VARIANT="3.9-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
RUN apt-get update \
    && apt-get -y install --no-install-recommends fish jq\
    && rm -rf /var/lib/apt/lists/*

ENV TZ="Asia/Tokyo"

ARG USER_NAME="vscode"
ARG GROUP_NAME="vscode"
COPY --chown=${USER_NAME}:${GROUP_NAME} ./.config/fish/config.fish ./home/vscode/.config/fish/config.fish

USER vscode
SHELL ["/usr/bin/fish", "-c"]

# Install fisher, bobthefish theme and poetry.
RUN curl -sL https://git.io/fisher | source \
    && fisher install jorgebucaran/fisher \
    && fisher install oh-my-fish/theme-bobthefish \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

CMD ["fish"]
