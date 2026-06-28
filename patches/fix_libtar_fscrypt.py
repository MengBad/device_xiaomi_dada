#!/usr/bin/env python3
import os

# 1. Patch append.c, block.c, and extract.c to disable v1 fscrypt function calls
files_to_disable = [
    'bootable/recovery/libtar/append.c',
    'bootable/recovery/libtar/block.c',
    'bootable/recovery/libtar/extract.c'
]
for filepath in files_to_disable:
    if os.path.exists(filepath):
        print(f"Disabling fscrypt in {filepath}...")
        with open(filepath, 'r') as f:
            content = f.read()
        new_content = content.replace('#ifdef USE_FSCRYPT', '#if defined(USE_FSCRYPT) && 0')
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Successfully patched {filepath}")
    else:
        print(f"File not found: {filepath}")

# 2. Patch libtar.h to fix the struct fscrypt_policy tag issue
libtar_h = 'bootable/recovery/libtar/libtar.h'
if os.path.exists(libtar_h):
    print(f"Fixing fscrypt struct tag in {libtar_h}...")
    with open(libtar_h, 'r') as f:
        content = f.read()
    
    # Replace the fscrypt_policy type reference with 'struct fscrypt_policy'
    # using different possible spacings (two spaces, one space, tab) to be robust.
    new_content = content.replace('fscrypt_policy  *fep;', 'struct fscrypt_policy  *fep;')
    new_content = new_content.replace('fscrypt_policy *fep;', 'struct fscrypt_policy *fep;')
    new_content = new_content.replace('fscrypt_policy\t*fep;', 'struct fscrypt_policy\t*fep;')
    
    with open(libtar_h, 'w') as f:
        f.write(new_content)
    print(f"Successfully patched {libtar_h}")
else:
    print(f"File not found: {libtar_h}")
