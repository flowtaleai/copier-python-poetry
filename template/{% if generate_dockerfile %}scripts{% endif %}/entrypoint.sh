#!/bin/bash

poetry run {{ package_name.split('.')[-1] }} "$@"
