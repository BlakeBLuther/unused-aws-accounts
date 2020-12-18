# Unused AWS Account Finder

This is a quick script to identify any AWS accounts that have
not seen a login for more than a specific timeframe, OR any accounts
that have a creation date over a specific amount of time ago and
have seen no logins.

The idea is to identify accounts that are unused and forgotten about
so that they may be decomissioned by the appropriate parties.

## Installation
Create a venv in the project directory:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Create a `config.yaml` in the project directory.
There needs to be a key `profiles` with values matching
the name of the profiles in your `~/.aws/credentials` file.
For example, if my AWS credentials file was:

```ini
[default]
aws_access_key_id=YOURIDHERE
aws_secret_access_key=YOURKEYHERE

[account1]
aws_access_key_id=YOURIDHERE
aws_secret_access_key=YOURKEYHERE

[account2]
aws_access_key_id=YOURIDHERE
aws_secret_access_key=YOURKEYHERE

[account3]
aws_access_key_id=YOURIDHERE
aws_secret_access_key=YOURKEYHERE

...
```

and I wanted to run the script against AWS profiles 
`account2` and `account3`, I would create a `config.yaml` file
like so:

```yaml
---
 - profiles:
    - account2
    - account3
```

Then run with
```bash
python ./main.py
```

## Sample output
```
-----
Unused account2 users:
User:         john.smith@example.com
Creation date:             03 Jun 20
Last login:                20 Oct 20

User:           not.real@example.com
Creation date:             06 Apr 20
Last login:                    Never

User:           service-account-user
Creation date:             16 Jul 19
Last login:                    Never
```