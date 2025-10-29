# Wise plugin for ofxstatement

This plugin parses CSV statements from [Wise](https://wise.com/) and converts them to OFX format for use with personal finance software.

## Installation

### From GitHub (Latest Version)

Install directly from the GitHub repository:

```bash
pipx install git+https://github.com/wigny/ofxstatement-wise.git
```

### Development Installation

For development or testing:

```bash
git clone https://github.com/wigny/ofxstatement-wise.git
cd ofxstatement-wise
pipx install -e .
```

## Usage

### Basic Conversion

Convert a Wise CSV statement to OFX:

```bash
ofxstatement convert -t wise statement.csv statement.ofx
```

The plugin automatically detects the currency from your CSV file, so no configuration is needed for basic usage!

### Configuration (Optional)

Configuration can be edited with `ofxstatement edit-config` command. These configuration parameters are understood by this plugin:

| Parameter      | Required? | Description                                | Example Values                 |
| -------------- | --------- | ------------------------------------------ | ------------------------------ |
| `currency`     | Optional  | The currency of the statement transactions | `GBP`, `BRL`                   |
| `account`      | Optional  | Account number/identifier                  | `25635393`, `1176697`          |
| `bank_id`      | Optional  | Bank routing/sort code or COMPE code       | `230801` (UK), `40571694` (BR) |
| `branch_id`    | Optional  | Branch/agency code                         | `0001` (BR)                    |
| `account_type` | Optional  | Type of account (default: `CHECKING`)      | `CHECKING`, `SAVINGS`          |

#### Example: UK Wise Account

For a UK Wise account with:

- Account number: 25635393
- Sort code: 23-08-01

```ini
[wise:gbp]
plugin = wise
currency = GBP
account = 25635393
bank_id = 230801
```

Then convert using:

```bash
ofxstatement convert -t wise:gbp statement.csv statement.ofx
```

#### Example: Brazilian Wise Account

For a Brazilian Wise account with:

- Bank code: 40571694 (or COMPE: 0405)
- Branch code: 0001
- Account number: 1176697

```ini
[wise:brl]
plugin = wise
currency = BRL
account = 1176697
bank_id = 40571694
branch_id = 0001
```

Then convert using:

```bash
ofxstatement convert -t wise:brl statement.csv statement.ofx
```

## Development

### Installing Dependencies

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management. First, install `uv`:

```bash
# Install uv
mise install
```

Then install all dependencies (including development tools):

```bash
# Install the project with dev dependencies
uv sync --dev
```

### Running Tests

Run the test suite:

```bash
uv run pytest -v
```

To update snapshots after intentional changes:

```bash
uv run pytest --snapshot-update
```

### Other Development Commands

```bash
# Run type checking
uv run mypy src/

# Format code
uv run black src/

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --group dev package-name
```
