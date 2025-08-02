# Jinja2 Templates

This directory contains modular Jinja2 templates for generating network device configurations.

## Available Templates

### Arista Templates (`arista/`)

- **`bgp.j2`** - BGP routing configuration
- **`routing_filters.j2`** - Route maps and prefix lists
- **`interfaces.j2`** - Interface configuration
- **`vlans.j2`** - VLAN configuration
- **`system.j2`** - System-wide configuration (hostname, NTP, SNMP, etc.)

## Template Structure

Each template is designed to be modular and can be used independently. The templates expect specific YAML data structures as input.

## Usage

Templates are automatically used by the `render_config.py` script. Users don't need to interact with these templates directly - they only need to fill out the YAML input files.

## Adding New Templates

When adding new templates:

1. Create the `.j2` file in the appropriate vendor directory
2. Update the `template_files` mapping in `scripts/render_config.py`
3. Test with sample data
4. Update documentation

## Template Guidelines

- Use clear, descriptive variable names
- Include comments for complex logic
- Handle optional parameters gracefully with defaults
- Follow vendor-specific configuration syntax
