#!/bin/bash
pushd "$(dirname "$0")"
. .../venv/bin/activate
gunicorn blog.wsgi
popd