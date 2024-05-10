#!/bin/sh
git init --initial-branch=main
git add .
git remote add origin {{ cookiecutter.repo_url }}