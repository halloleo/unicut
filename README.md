# Truncate Unicode to Byte length

This project provides and analyses Python functions to truncate a Unicode string in a way that its FUT-8 byte representation does not exceed a given number of bytes.

### Introduction

For the uninitiated a brief example. Consider the string

> Happy Days!&#x1F600;

This string has 12 characters, but its UTF-8 representation has 15 bytes: 11 for the ASCII characters `Happy Days!` and 4 bytes `\xf0\x9f\x98\x80`) for the smiley &#x1F600;.

If we want to cut the string to a length of, say, 14 bytes (or more presicsly if we want to truncate *the UTF-8 representation of the string* to contain no  more than 14 bytes), than we have to cut before the last character:

> Happy Days!

But we cannot cut the byte representation just at 14 bytes, because then we have three dangling  bytes from the smiley left in the byte stream which makes it non-valid for UTF-8. Therfore we have to cut at 11 bytes!

So cutting uncode strings to (UTF-8) byte lengths is not trivial. 

### Different implementations

We have two different truncation implementations here. The 1st implementation is my first naive attempt via concatenation; the second implementation is in its core by StackOverfow user [zvone]('truncate_by_backing_up_bytes'). He kindly wrote it up in answer to [my question about this topic](https://stackoverflow.com/questions/59451048/efficient-way-to-cut-a-utf-8-string-in-python-to-a-given-maximal-byte-length). I have amended the version here to be save against some edge cases which I found via property-based testing with Hypothesis. 


### Performance 

Furthermore I wrote a few performance tests with the `timeit` module from the Standard Library. Here the output:


```
--- Timeings WITHOUT cutting the strings ---
Time 'truncate_by_concating' with SHORT_UNICODE string UNCUT
100000 loops, best of 5: 0.794 usec per loop
Time 'truncate_by_backing_up_bytes' with SHORT_UNICODE string UNCUT
100000 loops, best of 5: 3.57 usec per loop
Time 'truncate_by_concating' with LONG_UNICODE string UNCUT
100000 loops, best of 5: 0.888 usec per loop
Time 'truncate_by_backing_up_bytes' with LONG_UNICODE string UNCUT
100000 loops, best of 5: 1.62 usec per loop

--- Timeings WITH cutting the strings (at len-2) ---
Time 'truncate_by_concating' with SHORT_UNICODE string CUT at len-2
100000 loops, best of 5: 1.48 usec per loop
Time 'truncate_by_backing_up_bytes' with SHORT_UNICODE string CUT at len-2
100000 loops, best of 5: 5.18 usec per loop
Time 'truncate_by_concating' with LONG_UNICODE string CUT at len-2
100000 loops, best of 5: 22.1 usec per loop
Time 'truncate_by_backing_up_bytes' with LONG_UNICODE string CUT at len-2
100000 loops, best of 5: 4.08 usec per loop
```
Very surprisingly `truncate_by_concating` is faster than `truncate_by_backing_up_bytes`!!! This "shouldn't" be the case - particuklaly for larger strings.

### TODO

* Find out *why* `truncate_by_backing_up_bytes` is slower than `truncate_by_concating`.
