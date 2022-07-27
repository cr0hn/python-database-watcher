# Python Database Watcher Library

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)
![Pypi](https://img.shields.io/pypi/v/databases_watcher)
![Python Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue)

In a nutshell ``Python Database Watcher Library`` is a small library with a set of utilities to help you to monitor and watch the database changes.

# Install

```bash
> pip install databases_watcher
```

# Supported databases

## Redis

Supported modes:

- **Single mode**: `redis://[[user]:[password]]@host:port/?db=[INT]&queue=[STRING]`
- **Pub/Sub mode**: `redis+pubsub://[[user]:[password]]@host:port/?db=[INT]&channel=[STRING]`
- **Watch mode**: `redis+watch://[[user]:[password]]@host:port/?db=[INT]&queue=[STRING]`

> TODO: improve watch mode

# Usage examples

TODO

# License

Dictionary Search is Open Source and available under the [MIT](https://github.com/cr0hn/python-performance-tools/blob/main/LICENSE).

# Contributions

Contributions are very welcome. See [CONTRIBUTING.md](https://github.com/cr0hn/python-performance-tools/blob/main/CONTRIBUTING.md) or skim existing tickets to see where you could help out.


