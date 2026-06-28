#!/usr/bin/env python3
"""
Fix libtar fscrypt v1/v2 API incompatibility in TWRP 14.1 bootable/recovery.

TWRP's libtar/append.c uses old fscrypt v1 API functions (fscrypt_policy_get_struct,
lookup_ref_key with fscrypt_policy_v1 *), but the newer system/vold fscrypt_policy.h
has updated these functions to use fscrypt_policy_v2 *. Additionally, get_policy_size()
and get_policy_descriptor() have been removed from vold.

This script wraps the incompatible fscrypt v1 block with #if 0 / #endif to disable it.
TWRP will lose the ability to save fscrypt policies in tar archives, but the recovery
itself will still boot and function normally.
"""

import re
import sys
import os

APPEND_C = 'bootable/recovery/libtar/append.c'

if not os.path.exists(APPEND_C):
    print(f"File not found: {APPEND_C}", file=sys.stderr)
    print("Searching for append.c in bootable/...")
    for root, dirs, files in os.walk('bootable'):
        for fname in files:
            if fname == 'append.c':
                print(f"  Found: {os.path.join(root, fname)}")
    sys.exit(0)

with open(APPEND_C, 'r') as f:
    lines = f.readlines()

print(f"Patching {APPEND_C} ({len(lines)} lines)")

new_lines = []
i = 0
patched = 0

while i < len(lines):
    line = lines[i]

    if 'fscrypt_policy_get_struct' in line:
        # Find the start of the enclosing 'if' block in what we've already emitted
        if_start = len(new_lines)
        for j in range(len(new_lines) - 1, max(0, len(new_lines) - 8), -1):
            stripped = new_lines[j].strip()
            # Match lines like "    if (something" or "    if(something"
            if re.match(r'^\s*if\s*\(', new_lines[j]):
                if_start = j
                break

        # Insert the #if 0 guard before the if-statement
        new_lines.insert(if_start, '#if 0  /* disabled: fscrypt v1 API incompatible with vold v2 */\n')

        # Add the current line (part of the if block)
        new_lines.append(line)

        # Track braces to find the end of the if block
        brace_depth = 0
        seen_open_brace = False
        while i < len(lines):
            current = lines[i]
            opens = current.count('{')
            closes = current.count('}')
            new_lines.append(current)
            brace_depth += opens - closes
            if opens > 0:
                seen_open_brace = True
            if seen_open_brace and brace_depth <= 0:
                new_lines.append('#endif  /* fscrypt v1 disabled: API updated to v2 in vold */\n')
                patched += 1
                print(f"  Disabled fscrypt block (started ~line {if_start+1}, ended ~line {i+1})")
                break
            i += 1
    else:
        new_lines.append(line)

    i += 1

if patched > 0:
    with open(APPEND_C, 'w') as f:
        f.writelines(new_lines)
    print(f"Successfully patched {patched} fscrypt v1 block(s) in libtar/append.c")
else:
    print("No fscrypt_policy_get_struct found in append.c - no patch needed (OK)")
