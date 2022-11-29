FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

USER vscode

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PYTHONUNBUFFERED 1

COPY --chown=vscode . .
