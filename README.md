# elan-fs
Tools for working with storing Elan-formatted tasks in the file system.

Includes:
- loading a task from a ZIP archive in Polygon format
- reading an Elan-formatted task into a Python object
- API for accessing the contents of tests, task conditions and internal programs (validator, scorer, checker and their tests)

## Roadmap for Polygon parser
- [x] short name (id)
- [x] problem name (on multiple languages)
- [x] time and memory limits
- [x] support statements text
    - [x] multi languages
    - [x] support variate statement sections (legend, notes, tutorial, scoring)
    - [x] example tests
- [ ] validators support
    - [ ] validators
    - [ ] validators tests
- [ ] checker
- [ ] base files (testlib.h, built-in checkers, so on)
- [ ] author solutions

## Roadmap for Elan FS
- [ ] Elan archive validator
- [ ] Elan-formatted ZIP-archive parser
- [ ] `getProblemById`
- [ ] Add problem to MongoDB