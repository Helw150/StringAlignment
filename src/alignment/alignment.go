package alignment

import (
	"levenshtein"
	"bytes"
)

func Align(source []rune, target []rune) (SOURCE string, TARGET string) {
	var sourcebuffer bytes.Buffer
	var targetbuffer bytes.Buffer
	script := levenshtein.EditScriptForStrings(source, target, levenshtein.DefaultOptions)
	i := 0
	j := 0
	for _, operation := range script {
		if operation == 3 || operation == 2 {
			sourcebuffer.WriteString(string(source[i]))
			targetbuffer.WriteString(string(target[j]))
			i++
			j++
		} else if operation == 0 {
			sourcebuffer.WriteString("-")
			targetbuffer.WriteString(string(target[j]))
			j++
		} else {
			sourcebuffer.WriteString(string(source[i]))
			targetbuffer.WriteString("-")
			i++
		}
	}
	return sourcebuffer.String(), targetbuffer.String()
}
