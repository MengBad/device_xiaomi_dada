#!/usr/bin/env python3
import os

files_to_patch = [
    'bootable/recovery/libtar/append.c',
    'bootable/recovery/libtar/block.c'
]

for filepath in files_to_patch:
    if os.path.exists(filepath):
        print(f"Patching {filepath}...")
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace `#ifdef USE_FSCRYPT` with `#if defined(USE_FSCRYPT) && 0`
        # to disable all fscrypt v1 code blocks which are incompatible with vold v2.
        new_content = content.replace('#ifdef USE_FSCRYPT', '#if defined(USE_FSCRYPT) && 0')
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Successfully patched {filepath}")
    else:
        print(f"File not found: {filepath}")
