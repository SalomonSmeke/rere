# rere: regex retrieve

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b97ea2abfb94475fa29d96e0a6d7b0aa)](https://www.codacy.com/manual/ssmeke/rere?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SalomonSmeke/rere&amp;utm_campaign=Badge_Grade)

rere is a regex notepad and search tool. It helps you save patterns you use
frequently, and search for ones you use infrequently.

It is very much still in development, and should be considered just an alpha MVP for now.

[Test PyPi Entry (will transition to regular PyPi once not in Alpha)](https://test.pypi.org/project/reretrieve/)

## Get started by finding some vowels with rere and [ack](https://beyondgrep.com/)

```console
$ pip install --index-url https://test.pypi.org/simple/ reretrieve
$ ack $(rere vowels)
```

## More usage

Add a pattern:

```console
$ rere --add "[aeiou]" vowels|v
[aeiou]
```

Retrieve it:

```console
$ rere v
[aeiou]
$ rere vowels
[aeiou]
```

Overwrite it:

```console
$ rere --add "[aeiouAEIOU]" --force vowels
[aeiouAEIOU]
```

Remove it:

```console
$ rere --remove vowels
[aeiouAEIOU]
```

Retrieve it from the web!

```console
$ rere vowels
[aeiou]
```

Use it with ack to find vowels:
```console
$ ack $(rere vowels)
```

## Donations

[![Donate](https://img.shields.io/badge/PayPal-ssmeke-blue)](https://www.paypal.me/ssmeke)

You do not have to donate. I do not need your money. But if you like the tool
and want to buy me a coffee, I will definitely appreciate it!  

## Patternfile format

The patternfile format is VERY much going to change. Probably to some sensible
TOML/YML/JSON thing. Once that transition happens, the idea is to allow
specifying the regex flavor.

*   `PATTERNNAME:PATTERN` – general formatting.
*   `PATTERNNAME1|PATTERNNAME2:PATTERN` – two acceptable names.
*   `PA:TTERNNAME:PATTERN` – bad pattern name.
*   `PATTERNNAME:[:]` – totally fine.
*   `PATTERNNAME::` – totally fine.
*   `PATTERNNAME:[ \t\n]` – also fine.

## [License](https://github.com/SalomonSmeke/rere/blob/dev/LICENSE)
