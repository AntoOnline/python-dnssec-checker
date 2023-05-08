# DNSSEC Checker

This is a fork of the original DNSSEC Checker project available at https://github.com/patrikskrivanek/dnssec. It has been updated to use the latest version of the `dns` Python library and to resolve the `DeprecationWarning` issue that appeared when using the original code.

## Requirements

This project requires the following Python libraries:

- `dns`

You can install these libraries using `pip` by running the following command:

```
pip install -r requirements.txt
```

## Usage

You can run the DNSSEC Checker by running the `dnssec_checker.py` script with the `--domain` argument. For example:

```
python3 dnssec_checker.py --domain anto.online
```

This will validate the DNSSEC signatures for the `anto.online` domain and return a message and a status code. The possible status codes are:

- 0: STATE_OK (OK)
- 1: STATE_WARNING (Warning)
- 2: STATE_CRITICAL (Critical)
- 3: STATE_UNKNOWN (Unknown)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Want to connect?

Feel free to contact me on [Twitter](https://twitter.com/OnlineAnto), [DEV Community](https://dev.to/antoonline/) or [LinkedIn](https://www.linkedin.com/in/anto-online) if you have any questions or suggestions.

Or just visit my [website](https://anto.online) to see what I do.
