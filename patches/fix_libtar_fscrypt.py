#!/usr/bin/env python3
import os

# 1. Recursively find and patch all .c and .h files in libtar to disable USE_FSCRYPT blocks
libtar_dir = 'bootable/recovery/libtar'
if os.path.exists(libtar_dir):
    print(f"Scanning {libtar_dir} to disable USE_FSCRYPT blocks...")
    for root, dirs, files in os.walk(libtar_dir):
        for file in files:
            if file.endswith(('.c', '.h')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                if '#ifdef USE_FSCRYPT' in content:
                    print(f"Disabling fscrypt in {filepath}...")
                    new_content = content.replace('#ifdef USE_FSCRYPT', '#if defined(USE_FSCRYPT) && 0')
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Successfully patched {filepath}")
else:
    print(f"Directory not found: {libtar_dir}")

# 2. Patch libtar.h to fix the struct fscrypt_policy tag issue and define TAR_STORE_FSCRYPT_POL unconditionally
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
    
    # Unconditionally define TAR_STORE_FSCRYPT_POL to prevent compilation failures in twrpTar.cpp
    new_content += "\n#ifndef TAR_STORE_FSCRYPT_POL\n#define TAR_STORE_FSCRYPT_POL 512\n#endif\n"
    
    with open(libtar_h, 'w') as f:
        f.write(new_content)
    print(f"Successfully patched {libtar_h}")
else:
    print(f"File not found: {libtar_h}")

# 3. Scan all .cpp and .c files in bootable/recovery/ and add weak stubs for missing legacy FDE functions if referenced.
recovery_dir = 'bootable/recovery'
if os.path.exists(recovery_dir):
    print(f"Scanning {recovery_dir} for legacy FDE functions...")
    fde_funcs = [
        'cryptfs_get_password_type',
        'cryptfs_check_passwd',
        'cryptfs_check_footer',
        'delete_crypto_blk_dev',
        'set_partition_data'
    ]
    
    stubs = """
#ifdef __cplusplus
extern "C" {
#endif
    int __attribute__((weak)) cryptfs_get_password_type(void) { return -1; }
    int __attribute__((weak)) cryptfs_check_passwd(const char* password) { return -1; }
    int __attribute__((weak)) cryptfs_check_footer(void) { return -1; }
    int __attribute__((weak)) delete_crypto_blk_dev(const char* name) { return -1; }
    void __attribute__((weak)) set_partition_data(const char* path, const char* key_loc) {}
#ifdef __cplusplus
}
#endif
"""
    for root, dirs, files in os.walk(recovery_dir):
        # Exclude libtar to avoid patching library files
        if 'libtar' in root:
            continue
        for file in files:
            if file.endswith(('.cpp', '.c')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Check if file references any of the legacy FDE functions
                needs_stubs = False
                for func in fde_funcs:
                    if func in content:
                        # Make sure it's not already defined or our own stub
                        if f"__attribute__((weak)) {func}" not in content:
                            needs_stubs = True
                            break
                
                if needs_stubs:
                    print(f"Adding legacy FDE stubs to {filepath}...")
                    with open(filepath, 'w') as f:
                        f.write(stubs + content)
                    print(f"Successfully patched {filepath}")
else:
    print(f"Directory not found: {recovery_dir}")
