#!/bin/bash
mv binfiles/dict_news_info.p .
rm -rf binfiles/*.p
mv dict_news_info.p binfiles
python na_analysis.py "$@"
