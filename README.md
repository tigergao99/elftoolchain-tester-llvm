# elftoolchain tester
The elftoolchain tester tests FreeBSD's version of elftoolchain against LLVM test suites.
## Usage
```
usage: elftoolchain_tester [-h] [-p PATH] [file [file ...]]

Test elftoolchain against LLVM tests.

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path of llvm-project checkout.
```
### Comparing two test results:
```
[tig@tiger ~/proj/elftoolchain-tester-llvm]$ ./testElftoolchain.py samplerun1.txt samplerun.txt 
For program llvm-ar:
Additional tests that passed in samplerun.txt since samplerun1.txt:
        tools/llvm-ar/add-library.test
        tools/llvm-ar/absolute-paths.test
Tests that regressed in samplerun.txt since samplerun1.txt:
        tools/llvm-ar/delete.test
        tools/llvm-ar/error-opening-permission.test

For program llvm-readelf:
Additional tests that passed in samplerun.txt since samplerun1.txt:
        tools/llvm-readobj/ELF/groups.test
        tools/llvm-readobj/ELF/gnuhash.test
```