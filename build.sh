#!/bin/bash

# Install system dependencies for WeasyPrint
apt-get update
apt-get install -y \
  libpango-1.0-0 \
  libcairo2 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  libjpeg-dev \
  libxml2-dev \
  libxslt1-dev

# Install WeasyPrint Python dependencies
pip install weasyprint
