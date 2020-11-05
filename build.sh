#!/bin/bash
pip install kfp
dsl-compile --py train-pipeline.py --output train-pipeline.py.yaml