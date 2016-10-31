## Synopsis

This is a library which aligns two strings based on the Script used to create the Levenshtein distance of two words. The Go Library itself is held within src. External files provide an example of how to use the library in a Websocket server where the Go code is accessed through Tornado and Python.

## Code Example

SourceAlignment, TargetAlignment := alignment.Align([]rune(Source), []rune(Target))
## Motivation

The alignment library was originally created to align Neural Network text guesses to correct outputs for statistical analysis of errors. However, it can be used for statistical analysis of any sort of transcription errors whether they be digital errors, machine learning errors, or DNA transcription errors.

## Installation

The alignment folder in the src directory should be added to the src folder in your GOPATH.
The function can then be included using "import alignment" in files for which alignment is needed.

## License

This repository uses the MIT license giving open rights for it's use to innovators.
