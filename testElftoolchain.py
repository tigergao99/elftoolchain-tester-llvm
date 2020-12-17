#!/usr/bin/env python3
import argparse
import os

filelist = {
    'llvm-ar', 'llvm-addr2line', 'llvm-nm', 'llvm-objcopy', 'llvm-objdump',
    'llvm-ranlib', 'llvm-readelf', 'llvm-size', 'llvm-strings', 'llvm-strip'}

def create_symlinks():
    bin_map = {'llvm-objdump': 'elfdump'}
    for f in filelist:
        os.system(f'mv {f} {f}-1')
        if f in bin_map:
            os.system(f'ln -s /usr/bin/{bin_map[f]} {f}')
        else:
            os.system(f"ln -s /usr/bin/{f.split('-')[-1]} {f}")

def run_tests():
    test_dir = {'llvm-addr2line': 'llvm-symbolizer', 'llvm-objcopy': 'llvm-objcopy/ELF',
        'llvm-objdump': 'llvm-objdump/ELF/', 'llvm-readelf': 'llvm-readobj/ELF'}
    for f in filelist:
        # llvm-strip tested in llvm-objcopy and llvm-objdump
        if f != 'llvm-strip':
            if f in test_dir:
                os.system(f'./llvm-lit ../../llvm/test/tools/{test_dir[f]}')
            else:
                os.system(f'./llvm-lit ../../llvm/test/tools/{f}')

def main():
    parser = argparse.ArgumentParser(prog='elftoolchain_tester', description='Test elftoolchain against LLVM tests.')
    parser.add_argument('-p', '--path', required=True, help='Path of llvm-project checkout.')
    args = parser.parse_args()
    
    os.chdir(args.path + '/build/bin')
    create_symlinks()
    run_tests()

if __name__ == "__main__":
    main()
