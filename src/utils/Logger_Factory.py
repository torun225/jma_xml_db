import json
from logging import getLogger, config

def create(name):
  with open('./utils/log_config.json', 'r') as f:
      log_conf = json.load(f)

  config.dictConfig(log_conf)

  f.close()

  return getLogger(name)