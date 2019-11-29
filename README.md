<sub>WIP dont use</sub>
# rere: retrieve regex

rere is a regex notepad and search tool. It lets you save patterns you use frequently, and search for ones you use infrequently.  

## Get started by finding some vowels

```
pip install rere-ssmeke
ack $(rere vowels)
```

## More usage

Add a pattern  
`rere --add vowels|v [aeiou] # [aeiou]`

Retrieve it
```
rere v # [aeiou]
rere vowels # [aeiou]
```

Overwrite it  
`rere --add vowels --force [aeiouAEIOU] # [aeiouAEIOU]`

Retrieve it
```
rere v # [aeiou]
rere vowels # [aeiouAEIOU]
```

Remove it  
`rere --remove vowels # [aeiouAEIOU]`

Retrieve it from the web!  
`rere vowels # [aeiou]`

You have it locally now  
`rere --local vowels # [aeiou]`

Use it with ack to find vowels  
`ack $(rere vowels)`

## Donations [![Donate](https://img.shields.io/badge/PayPal-ssmeke-blue)](https://www.paypal.me/ssmeke)

You do not have to donate. I do not need your money. But if you want to, I will definitely appreciate it!  
Any donations over 10$ are way too high and ill send the extra to charity. But I keep all the feelings of validation.  

## Patternfile format

`PATTERNNAME:PATTERN` general formatting.  
`PATTERNNAME1|PATTERNNAME2:PATTERN` two acceptable names.  
`PA:TTERNNAME:PATTERN` bad pattern name.  
`PATTERNNAME:[:]` totally fine.
`PATTERNNAME::` totally fine.  
```
PATTERNNAME:[ \t
]
```  
multi line like that isnt allowed.  
`PATTERNNAME:[ \t\n]` but like that is fine.

TODO: Add a description of the pattern flavor, allow selecting one.

## [License](https://github.com/SalomonSmeke/rere/blob/dev/LICENSE)
