package main

import "alignment"
import "os"
import "fmt"

func main() {
	Source := os.Args[1]
	Target := os.Args[2]
	sourceStrings, targetStrings := alignment.Align([]rune(Source), []rune(Target))
	fmt.Println(sourceStrings + "\t" + targetStrings) 
}
