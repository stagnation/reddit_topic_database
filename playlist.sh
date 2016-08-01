#!/bin/bash
cat $1 | sed 's/".*"/d/' | awk -F ',' '{ print $4 ; }' | sed '/^\r/d' | sort | uniq

