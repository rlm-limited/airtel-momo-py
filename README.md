# MTN Momo API Client Library

This repository contains a Python client library for interacting with the MTN Momo API. The library provides an easy-to-use interface for developers to integrate MTN Momo payment functionalities into their applications.

## Features

- Create and manage payment requests

## Installation

You can install the library using pip:

```bash
pip install "mtn-momo @ git+https://github.com/rlm-limited/mtn_momo.git"
```

## Usage

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Update OpenAPI Specification

If you need to update the OpenAPI specification, you can place it in the `docs` directory and run the following script to clean it up:

```bash
python scripts/fixCollectionOpenApi.py
```

**Note:** The script will read the `collection.json` file from the `docs` directory, clean it up, and save the cleaned version as `collection_fixed.json` in the same directory. \nMake sure to update the paths in the script if your OpenAPI specification is located elsewhere. \n WorkingDir should be the root of the repository when running the script.


### Generate Client Library
To generate the client library from the OpenAPI specification, you can use the OpenAPI Generator CLI. First, make sure you have it installed:

```bash
openapi-python-client generate --path docs/collection_fixed.json
```