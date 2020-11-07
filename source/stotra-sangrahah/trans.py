#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import glob
import sys
import xsanscript
import re
syllable = "(?:[अ-औॐ\uA8F3\uA8F4]|(?:[क-ह](?:\u094D|\u094D\u200D|\u200D\u094D))*[क-ह][\u093E-\u094D]?)\u0901?"
anudatta = "\u0952"
anusvaraVisarga = "\u0902?\u0903?"
prefix = sys.argv[1]

LipiSwapTable = {
    'grantha': {'font': 'Noto Serif Grantha', 'script': 'Grantha', 'scale': 0.5},
    'tamil': {'font': 'Noto Serif Tamil', 'script': 'Tamil', 'scale': 0.8},
    'telugu': {'font': 'Mandali', 'script': 'Telugu', 'scale': 0.9},
    'kannada': {'font': 'Noto Serif Kannada', 'script': 'Kannada', 'scale': 0.9},
    'tamilgrantha': {'font': 'Agastya Serif', 'script': 'Malayalam', 'scale': 0.5},
}

for out_script in ['tamil', 'telugu', 'grantha', 'kannada', 'tamilgrantha']:
    for ext in ['tex', 'sty', 'sh']:
        for fname in glob.iglob('%s/' % prefix + '**/*.%s' % ext, recursive=True):
            orig_folder_name = os.path.dirname(fname)
            folder_name = os.path.dirname(fname).replace('devanagari', out_script)
            os.makedirs(folder_name, exist_ok=True)
            print(folder_name, os.path.basename(fname))

            with open('%s/%s' % (folder_name, os.path.basename(fname)), 'w') as outfile:
                with open('%s/%s' % (orig_folder_name, os.path.basename(fname)), 'r', errors='replace') as f:
                    for line in f.readlines():
                        z = re.sub(f"({syllable}){anudatta}({anusvaraVisarga})", "\\\\ul{\\1\\2}", line.strip('\n'))
                        z = re.sub(f"({syllable})({anusvaraVisarga}){anudatta}", "\\\\ul{\\1\\2}", z)
                        z = z.replace('Script=Devanagari', 'Scale=%f,Script=%s' % (LipiSwapTable[out_script]['scale'], LipiSwapTable[out_script]['script']))
                        z = z.replace('Sanskrit 2003', '%s' % LipiSwapTable[out_script]['font'])
                        z = z.replace('Siddhanta', '%s' % LipiSwapTable[out_script]['font'])
                        z = z.replace('॰', '.')  # Replace dng abbr with dot in all other scripts
                        z = xsanscript.transliterate(z, 'devanagari', out_script)
                        z = z.replace('', ':').replace('', ':').replace("ʼ", "'")
                        z = z.replace('\\dng', '\\%s' % out_script)
                        specials = ['', '', '', '', 'ꣳ', 'ꣴ', '', '१॒॑']
                        swaraas = ["॒", "॑", "", "", "", '᳚']
                        if out_script == 'telugu':
                            specials.extend(['', ''])
                        for s in specials:
                            z = z.replace(s, '\\dng{%s}' % s)
                        if out_script == 'tamil':

                            maatraas = ["ா", "ி", "ீ", "ு", "ூ", "்ரு'", "்ரூ'", "்லு'", "்லூ'", "ெ", "ே", "ை", "ொ", "ோ", "ௌ", "்"]
                            z = z.replace('ँ', 'ன்')
                            z = z.replace('1॒॑', '\\dng{१॒॑}')
                            # z = z.replace('।', '\\danda{}')
                            # z = z.replace('॥', '\\ddanda{}')
                            for m in maatraas:
                                for sup in "²³⁴":
                                    src = '%s%s' % (sup, m)
                                    dest = '%s%s' % (m, sup)
                                    z = z.replace(src, dest)
                            for s in swaraas:
                                for sup in "²³⁴":
                                    src = '%s%s' % (sup, s)
                                    dest = '%s%s' % (s, sup)
                                    z = z.replace(src, dest)
                                for mod in "':":
                                    src = '%s%s' % (mod, s)
                                    dest = '%s%s' % (s, mod)
                                    z = z.replace(src, dest)
                                for sup in "²³⁴":
                                    src = '%s%s' % (sup, s)
                                    dest = '%s%s' % (s, sup)
                                    z = z.replace(src, dest)
                            # z = z.replace(s, '\\dng{%s}' % s)
                        print(z, file=outfile)
