#!/bin/bash
celery -A api.celery worker --loglevel=DEBUG
