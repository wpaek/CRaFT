#!/bin/bash
export SAGE_PATH="/home/pk/miniforge3/envs/sage/bin/sage"
uvicorn app:app --port 8000
