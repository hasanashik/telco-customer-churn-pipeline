#!/bin/bash

# Create directory structure
mkdir -p config \
         data/raw \
         data/processed \
         data/final \
         logs \
         models \
         notebooks \
         src/data \
         src/models \
         src/utils

# Create empty Python files
touch src/data/__init__.py \
      src/data/data_ingestion.py \
      src/data/preprocessing.py \
      src/models/__init__.py \
      src/models/train.py \
      src/models/predict.py \
      src/utils/__init__.py \
      src/utils/logger.py \
      src/utils/config.py \
      main.py
