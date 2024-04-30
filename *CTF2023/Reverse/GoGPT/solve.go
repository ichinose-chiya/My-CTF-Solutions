package main

import (
    "math/rand"
    "fmt"
)

func main() {
    s := []byte("cH@t_GpT_15_h3R3")

    rand.Seed(34)

    for i := len(s) - 1; i >= 0; i-- {
	j := rand.Intn(i + 1)
	s[i], s[j] = s[j], s[i]
    }

    fmt.Printf("%s\n", s)
}
