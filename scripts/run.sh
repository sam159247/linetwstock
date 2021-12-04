#!/bin/sh

exec uvicorn app.main:app --reload 
