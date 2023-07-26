#!/bin/sh
shopt -s extglob

while [ $# -gt 0 ]; do
  case "$1" in
    --port*|-p*)
      if [[ "$1" != *=* ]]; then shift; fi
      port="${1#*=}"
      ;;
    --baud*|-b*)
      if [[ "$1" != *=* ]]; then shift; fi
      baud="${1#*=}"
      ;;
    --net*|-n*)
      if [[ "$1" != *=* ]]; then shift; fi
      net="${1#*=}"
      ;;
    --led*|-l*)
      if [[ "$1" != *=* ]]; then shift; fi
      led="${1#*=}"
      ;;
    *)
      >&2 printf "Unrecognised argument '${1}'\n"
      >&2 printf "Usage: upload.sh --port <dir> --baud <int> --net <*.py> --led <*.py>\n"
      exit 1
      ;;
  esac
  shift
done

if [ -z ${port} ]; then
  >&2 printf "Missing required argument 'port'\n"
elif [ -z ${baud} ]; then
  >&2 printf "Missing required argument 'baud'\n"
elif [ -z ${net} ]; then
  >&2 printf "Missing required argument 'net'\n"
elif [ -z ${led} ]; then
  >&2 printf "Missing required argument 'led'\n"

else
  for file in src/*.py; do
      printf "Uploading $(basename $file)\n"
      ampy --port $port --baud $baud put $file $(basename $file)
  done

  printf "Uploading ${net} as 'setup_net.py'\n"
  ampy --port $port --baud $baud put $net setup_net.py

  printf "Uploading ${led} as 'setup_led.py'\n"
  ampy --port $port --baud $baud put $led setup_led.py

  exit 0
fi

>&2 printf "Usage: upload.sh --port <dir> --baud <int> --net <*.py> --led <*.py>\n"
exit 1
