#!/usr/bin/env python3
import argparse
import os
import sys

filelist = [
    'llvm-ar', 'llvm-addr2line', 'llvm-nm', 'llvm-objcopy', 'llvm-objdump',
    'llvm-ranlib', 'llvm-readelf', 'llvm-size', 'llvm-strings', 'llvm-strip']

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
            print(f, flush=True)
            if f in test_dir:
                os.system(f'./llvm-lit -q ../../llvm/test/tools/{test_dir[f]}')
            else:
                os.system(f'./llvm-lit -q ../../llvm/test/tools/{f}')

def parse_testsuite(file):
    prog = None
    failed_tests = set()
    fileset = set(filelist)
    for line in file:
        line = line.strip()
        if line in fileset:
            if prog:
                yield (prog, failed_tests)
            prog = line
            failed_tests.clear()
        elif line[:4] == 'LLVM':
            failed_tests.add(line.split()[2])

def compare_test_results(file1, file2):
    for (p1, failed1), (p2, failed2) in zip(parse_testsuite(file1), parse_testsuite(file2)):
        try:
            if p1 != p2:
                raise ValueError('Two test results are not run in same order or one is missing some elftoolchain executables.')
        except ValueError as e:
            print(e)
            sys.exit(1)
        strbuilder = []
        for i, test in enumerate(failed1 - failed2):
            if i == 0:
                strbuilder.append(f'Additional tests that passed in {file2.name} since {file1.name}:\n')
            strbuilder.append('\t' + test + '\n')
        for i, test in enumerate(failed2 - failed1):
            if i == 0:
                strbuilder.append(f'Tests that regressed in {file2.name} since {file1.name}:\n')
            strbuilder.append('\t' + test + '\n')
        if strbuilder:
            print('For program ' + p1 + ':\n' + ''.join(strbuilder))

def main():
    parser = argparse.ArgumentParser(prog='elftoolchain_tester', description='Test elftoolchain against LLVM tests.')
    parser.add_argument('-p', '--path', help='Path of llvm-project checkout.')
    parser.add_argument('file', type=argparse.FileType('r'), nargs='*')
    args = parser.parse_args()
    
    # comparing two test run results
    if len(args.file) == 2:
        compare_test_results(*args.file)
    # testing elftoolchain
    elif len(args.file) == 0:
        if not args.path:
            raise parser.error('Please specify llvm-project checkout via -p or --path.')
        os.chdir(args.path + '/build/bin')
        create_symlinks()
        run_tests()
    else:
        raise parser.error('Either pass 2 files for comparison or no files to run a new test.')

if __name__ == "__main__":
    main()
