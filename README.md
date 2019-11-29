WIP: does not do anything yet.

# rere: recall regex

rere is a regex storage and retrieval tool.
rere can save regex patterns you use frequently and retrieve them later on.  

crucially, if you have not stored a pattern, rere can search an online source for it.

(my personal use of it is as a regex search engine)

## Example Usage:

Add a pattern
`rere --add vowels|v [aeiou] # [aeiou]`

Retrieve it
`rere v # [aeiou]`
`rere vowels # [aeiou]`

Overwrite it
`rere --add vowels --force [aeiouAEIOU] # [aeiouAEIOU]`

Retrieve it
`rere v # [aeiou]`
`rere vowels # [aeiouAEIOU]`

Remove it
`rere --remove vowels # [aeiouAEIOU]`

Retrieve it from the web!
`rere vowels # [aeiou]`

You have it locally now
`rere --local vowels # [aeiou]`

Use it with ack to find vowels
`ack $(rere vowels)`

## Donations:

You do not have to donate. I do not need your money. But if you want to, I will definitely appreciate it!
Any donations over 10$ are going to the ACLU or the Conservation Fund. But I keep all the feelings of validation.
[![Donate](https://img.shields.io/badge/PayPal-ssmeke-blue)](https://www.paypal.me/ssmeke)
