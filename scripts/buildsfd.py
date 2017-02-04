#!/usr/bin/env fontforge
#
# Copyright (c) 2016, Sungsit Sawaiwan (https://sungsit.com | gibbozer [at] gmail [dot] com).
#
# This Font Software is licensed under the SIL Open Font License, Version 1.1 (OFL).
# You should have received a copy of the OFL License along with this file.
# If not, see http://scripts.sil.org/OFL
#

# This script will create SFD files from multi-layers source to prepare for later build process
# and it will only work with FontForge's Python extension.
import fontforge
import os
import subprocess
import shutil
import time
import datetime

# Predifined vars
family = 'Vain'
version = '1.2'
foundry = 'FontUni'
copyright =  'Copyright 2015-2017, Sungsit Sawaiwan (https://fontuni.com | uni@fontuni.com). This Font Software is licensed under the SIL Open Font License, Version 1.1 (http://scripts.sil.org/OFL).'
os2_vendor = 'FUni'
foundry_url = 'https://fontuni.com/'
designer = 'Sungsit Sawaiwan'
designer_url = 'https://sungsit.com/'
license_url = 'http://scripts.sil.org/OFL'

sources = ['sources/vain-roman.sfd','sources/vain-italic.sfd']
layers = ['Vain', 'Vain Mon']
features = ['vain-roman', 'vain-italic']
feature_dir = 'sources/'

build_dir = 'fonts/'
if os.path.exists(build_dir):
  shutil.rmtree(build_dir)

sfd_dir = 'sfd/'
if os.path.exists(sfd_dir):
  shutil.rmtree(sfd_dir)

unhinted_dir = build_dir + 'unhinted/'
if not os.path.exists(unhinted_dir):
  os.makedirs(unhinted_dir)

def fontPath(ext,name):
  path = build_dir + ext
  if not os.path.exists(path):
    os.makedirs(path)
  fontfile = path + '/' + name + '.' + ext
  return fontfile

def weights2Strings(weight):
  switcher = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black"
  }
  return switcher.get(weight)

# Microsoft compat
def msFamilyName(weight):
  switcher = {
    100: family + " Thin",
    200: family + " ExtraLight",
    300: family + " Light",
    400: family,
    500: family + " Medium",
    600: family + " SemiBold",
    700: family,
    800: family + " ExtraBold",
    900: family + " Black"
  }
  return switcher.get(weight, family)

def msStyleName(weight):
  switcher = {
    100: "Regular",
    200: "Regular",
    300: "Regular",
    400: "Regular",
    500: "Regular",
    600: "Regular",
    700: "Bold",
    800: "Regular",
    900: "Regular"
  }
  return switcher.get(weight)

def msStyleItalicName(weight):
  switcher = {
    100: "Italic",
    200: "Italic",
    300: "Italic",
    400: "Italic",
    500: "Italic",
    600: "Italic",
    700: "Bold Italic",
    800: "Italic",
    900: "Italic"
  }
  return switcher.get(weight)

def BlueValues(weight):
  switcher = {
    300: (-17, 0, 600, 617, 780, 797, 810, 827),
    400: (-18, 0, 600, 618, 780, 798, 810, 828),
    500: (-19, 0, 600, 619, 780, 799, 810, 829),
    600: (-20, 0, 600, 620, 780, 800, 810, 830),
    700: (-21, 0, 600, 621, 780, 801, 810, 831)
  }
  return switcher.get(weight)

def OtherBlues(weight):
  switcher = {
    300: (-222, -210),
    400: (-223, -210),
    500: (-224, -210),
    600: (-225, -210),
    700: (-226, -210)
  }
  return switcher.get(weight)

def StdHW(weight):
  switcher = {
    300: (52,),
    400: (64,),
    500: (79,),
    600: (98,),
    700: (110,)
  }
  return switcher.get(weight)

def StdVW(weight):
  switcher = {
    300: (67,),
    400: (85,),
    500: (113,),
    600: (137,),
    700: (160,)
  }
  return switcher.get(weight)

def otf2Sfd(otf,sfd_dir):

  font = fontforge.open(otf)
  sfd = sfd_dir + font.fontname + '.sfd'
  if not os.path.exists(sfd_dir):
    os.makedirs(sfd_dir)

  # Reset UniqueID
  font.appendSFNTName('English (US)', 'UniqueID', '')

  weight = font.os2_weight

  font.private['BlueValues'] = BlueValues(weight)
  font.private['OtherBlues'] = OtherBlues(weight)
  font.private['StdHW'] = StdHW(weight)
  font.private['StdVW'] = StdHW(weight)
  font.selection.all()
  font.autoHint()
  font.save(sfd)
  font.private.guess('StdHW')
  font.private.guess('StdVW')
  font.private.guess('StemSnapH')
  font.private.guess('StemSnapV')
  font.selection.all()
  font.autoHint()
  font.save(sfd)

  print(sfd, 'file saved.')
  font.close()

def buildSFD(source,family):

  font = fontforge.open(source)

  # prepare master
  font.familyname = family
  font.version = version
  font.copyright = copyright
  font.os2_vendor = os2_vendor
  font.weight = '400'
  font.os2_weight = 400
  font.appendSFNTName('English (US)', 'Manufacturer', foundry)
  font.appendSFNTName('English (US)', 'Designer', designer)
  font.appendSFNTName('English (US)', 'Vendor URL', foundry_url)
  font.appendSFNTName('English (US)', 'Designer URL', designer_url)
  font.appendSFNTName('English (US)', 'License URL', license_url)
  font.appendSFNTName('English (US)', 'Preferred Family', family)

  font.save()

  if source.endswith('-italic.sfd'):
    font.mergeFeature(feature_dir + features[1] + '.fea')
  else:
    font.mergeFeature(feature_dir + features[0] + '.fea')

  # loop through each layer & save it as sfd files
  for layer in layers:

    layername = font.layers[layer].name
    font.familyname = layername
    font.appendSFNTName('English (US)', 'Preferred Family', layername)

    # Roman style
    if source.endswith('-roman.sfd'):
      font.italicangle = 0.0
      font.fullname = layername + ' Regular'
      font.fontname = layername.replace(' ','') + '-Regular'
      font.appendSFNTName('English (US)', 'Preferred Styles', 'Regular')
      font.appendSFNTName('English (US)', 'SubFamily', 'Regular')
      font.os2_stylemap = 64 # 0x0040

    # Italic style
    if source.endswith('-italic.sfd'):
      font.italicangle = -9.0
      font.fullname = layername + ' Italic'
      font.fontname = layername.replace(' ','') + '-Italic'
      font.appendSFNTName('English (US)', 'Preferred Styles', 'Italic')
      font.appendSFNTName('English (US)', 'SubFamily', 'Italic')
      font.os2_stylemap = 1 # 0x0001

    # generate otf
    if font.os2_weight == 400:
      genname = layername.replace(' ','')
    else:
      genname = layername.replace(' ','-').replace('-Italic','Italic')

    otf = fontPath('otf',genname)

    otfgenflags  = ('opentype', 'PfEd-lookups')
    font.generate(otf, flags=otfgenflags, layer = layername)
    print(otf, 'instance generated.')

    # save sfd
    otf2Sfd(otf,sfd_dir)

  font.close()

for source in sources:
  buildSFD(source,family)
