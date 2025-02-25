# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2](https://pypi.org/project/Pyntel4004/1.2/) - 2022-07-08

### Notes
- Replacement release for 1.1.0

## 1.1.0 - **Release Revoked** 2022-06-27

### Notes
- Release revoked, since extra code inadvertently made it into the relase, which would have 
  broken the compatibility with Pyntel4004-cli
### Fixed
- Fixed documentation build issue

## [1.0.0](https://pypi.org/project/Pyntel4004/1.0.0/) - 2022-06-27

### Notes
- 
### Added
- Added platform-aware code (to enable a central codebase of cpython and micropython supported platforms)
- Added accumulator, registers and memory to core dump to core dump
- Replaced inbuilt `zfill` with hand-written `zfl` function due to micropython not supporting zfill
### Changed
- Switched to more efficient memory-allocation method for ROM/RAM/PRAM etc...
- Moved operation vectors inside Processor class
### Deprecated
-
### Fixed
- Fixed an issue where BIN file is used and there is no "end" mnemonic - did produce an error. Now doesnt.
- Tidied up some code to make it less complex, and improve quality
- Fixed issue in quiet mode when executing a program - now doesnt print opcodes
### Removed
- "4004" command line facility. This is now part of the Pyntel4004-cli project
- `init.py` module - now all initialisation occurs efficiently inside the processor class
- now no "eval" function - removed dangerous code and replaced with instruction vectors (only now left in test support code)
### Security
- N/A

## [0.0.1-beta.5](https://pypi.org/project/Pyntel4004/0.0.1b5/) - 2022-01-20

### Notes
- 
### Added
- Switched to Sonarcloud.io code scanning
- Added bytes to disassemble
- Added quiet mode to all functions
- Added a '--labels' option to dissassembly function
- Added ability to specify type of output file(s)
### Changed
- 
### Deprecated
- **Commands for running the assembler, disassembler and executer are now deprecated.**
  **The command-line commands should no longer be used, and will be removed in the next release.** 
  **To use the command-line, use:** 
  **`pip install Pyntel4004-cli`**
### Fixed
- Reduced code complexity in `construct.py` from 21 -> 15
- Code smells in the documentation construction script
- Code smells in some suboperations fixed
- Fixed bug in tests for WPM instruction
- Fixed major bugs in FIM and END processing
- Fixed minor bugs with pseudo-opcode 256 and writing .bin and retroshield files
### Removed
- Deepsource.io integration
- Codacy.com integration
### Security
- N/A

## [0.0.1-beta.4](https://pypi.org/project/Pyntel4004/0.0.1b4/) - 2022-01-13
### Notes
- Fixed issue with 0.0.1-beta.3 relating to incorrent merge process
- Release yanked and replaced with this release.
- See details below in 0.0.1-beta.3 for changes.

## 0.0.1-beta.3 **PULLED** - 2022-01-13

### Notes
- ***Successfully ran a copy of the Busicom calculator code on the Retroshield Arduino 4004.***
- ***The next stage will be to compile a short program using Pyntel4004 and run it on the Retroshield.***
### Added
- Completed first pass at all opcode documentation
- Write code to Retroshield-compatible `.h` file
- Added Glossary of Terms
- Added all Appendices in MSC-4 manual (partially automated where tables are required)
- Included initial content from the MCS-4 data sheet
- Added custom role to allow superscript substitutions
### Changed
- Consolidated all acknowledgements into a single page
### Deprecated
-
### Fixed
- Incorrect symbolic image being displayed on SRC instruction page
- Fixed a number of incorrect links
### Removed
-
### Security
-
## [0.0.1-beta.2](https://pypi.org/project/Pyntel4004/0.0.1b2/) - 2021-12-11

### Notes

- Includes first release of a disassembler
- **Successfully completely disassembled the BUSICOM 141-PF ROM object code**
### Added
- Additional documentation about the Intel 4004 and its' companion chipset
- Additional opcode documentation
- Initial version of a disassembler
- Mechanism to determine loading mechanism - either from an `.bin` or a `.bin` file
- Type hinting
- `other.py`
- `suboperations` directory
- Switched to `codefactor.io` for code analysis (on-demand only)
### Changed
- Broken out suboperations and reads to their own files for simplicity - all functions for a specific portion of the processor are now together in the hardware.suboperations module.
- Changed the "end" mnemonic from 255 to 256 - data in BUSICOM ROM could be confused with a 255 value.
### Deprecated
- N/A
### Fixed
- Error in assembler when the second label in a program had a corresponding operator with more than one operand; that and subsequent labels were being assigned incorrectly.
### Removed
- `suboperation.py`
- `reads.py`
- `codacy.com` code coverage
### Security
- N/A
## [0.0.1-beta.1](https://pypi.org/project/Pyntel4004/0.0.1b1/) - 2021-11-19

### Notes

- First Beta Release

### Added
-

### Changed
-

### Deprecated
-
### Fixed
- Code Style, Documentation, Bug Risks, Anti-Patterns

### Removed
- machine.py - no longer needed

### Security

## [0.0.1-alpha.6](https://pypi.org/project/Pyntel4004/0.0.1a7/) - 2021-11-04

### Added
- EQUATE function (symbols only - no EXPressions yet)
- Added functionality for option for JCN to specify flags numerically or alphabetically
- First stage of core dump facility to help debug code

### Changed
- Refactored some shared functions into a shared module and tested
- Rationalised some code to support functions
- Improved exception handling

### Deprecated
-
### Fixed
- Bug in SRC function where decimal number was used instead of binary number

### Removed
-
### Security
-
## [0.0.1-alpha.6](https://pypi.org/project/Pyntel4004/0.0.1a6/) - 2021-10-24

### Added
- Tests for WPM instruction
- Tests for SBM instruction
- Abstracted and tested new suboperations
- Tests now over 98% of opcode code

### Changed
- Switched to [KeepAChangeLog](https://keepchangelog.com) format.

### Deprecated
-
### Fixed
- Some small bugs in the WPM instruction code
- Abstracted some functions for readability

### Removed
-
### Security
-
## [0.0.1-alpha.5](https://pypi.org/project/Pyntel4004/0.0.1a5/) - 2021-10-10

### Added
- Completed WMP, WRx and WRR function tests.

### Changed
- Updated RDx and RDR functions.
- Improved Assembler code by simplifying
- Simplified some low-level instruction code

### Fixed
- Improved code style
- Finally fixed ongoing bug with build pipeline

## [0.0.1-alpha.4](https://pypi.org/project/Pyntel4004/0.0.1a4/) - 2021-10-03

### Added
- Auto added version from release branch name
- Completed tests for JCN instruction
- Completed tests for ISZ instruction
- Completed tests for WRM instruction

## [0.0.1-alpha.3](https://pypi.org/project/Pyntel4004/0.0.1a3/) - 2021-09-26

### Added
- Improved build pipeline
- Improved README
- Created CHANGELOG


## [0.0.1-alpha.2](https://pypi.org/project/Pyntel4004/0.0.1a2/) - 2021-09-24

### Not documented

## [0.0.1-alpha.1](https://pypi.org/project/Pyntel4004/0.0.1a1/) - 2021-09-24

### Not documented

