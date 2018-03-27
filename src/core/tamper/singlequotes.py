#!/usr/bin/env python
# encoding: UTF-8

"""
This file is part of Commix Project (http://commixproject.com).
Copyright (c) 2014-2018 Anastasios Stasinopoulos (@ancst).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

For more see the file 'readme/COPYING' for copying permission.
"""
import re
import sys
from src.utils import settings

"""
Adds single quotes (') between the characters of the generated payloads.
Notes:
  * This tamper script works against *nix targets.
"""

script_name = "singlequotes"
print settings.SUB_CONTENT_SIGN + script_name

if not settings.TAMPER_SCRIPTS[script_name]:
  settings.TAMPER_SCRIPTS[script_name] = True

def transform(payload):
  def add_single_quotes(payload):
    settings.TAMPER_SCRIPTS[script_name] = True
    rep = {
            "''i''f": "if", 
            "''t''h''e''n": "then",
            "''e''l''s''e": "else",
            "''f''i": "fi",
            "''s''t''r": "str",
            "''c''m''d": "cmd",
            "''c''ha''r": "char"
          }
    payload = re.sub(r'([b-zD-Z])', r"''\1", payload)
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    payload = pattern.sub(lambda m: rep[re.escape(m.group(0))], payload)
    return payload

  if settings.TARGET_OS != "win":
    if settings.EVAL_BASED_STATE != False:
      if settings.TRANFROM_PAYLOAD == None:
        settings.TRANFROM_PAYLOAD = False
        warn_msg = "The dynamic code evaluation technique, does not support the '"+ script_name  +".py' tamper script."
        sys.stdout.write("\r" + settings.print_warning_msg(warn_msg))
        sys.stdout.flush() 
        print
    else:
      settings.TRANFROM_PAYLOAD = True
      if settings.TRANFROM_PAYLOAD:
        payload = add_single_quotes(payload)

  else:
    if settings.TRANFROM_PAYLOAD == None:
      settings.TRANFROM_PAYLOAD = False
      warn_msg = "Windows target host(s), does not support the '"+ script_name  +".py' tamper script."
      sys.stdout.write("\r" + settings.print_warning_msg(warn_msg))
      sys.stdout.flush() 
      print

  return payload
  
# eof 