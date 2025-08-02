# Network Configuration Management with GitHub Actions

This repository provides an automated network configuration management system using GitHub Actions, Jinja2 templates, and ServiceNow integration.

## Overview

This system allows network engineers to:
1. Submit network configuration changes via pull requests
2. Use simple YAML files instead of complex Jinja2 templates
3. Automatically render configurations for Arista switches
4. Integrate with ServiceNow change management
5. Validate configurations before deployment

## Repository Structure

```
├── .github/workflows/     # GitHub Actions workflows
├── changes/              # ServiceNow change requests
│   └── CHG0123456/      # Example change request
├── templates/arista/     # Jinja2 templates for Arista switches
├── scripts/              # Configuration rendering scripts
├── examples/             # Example YAML configurations
└── output/               # Rendered configurations
```

## Quick Start

### For Network Engineers (Users)

1. **Create a new branch** named after your ServiceNow change request:
   ```bash
   git checkout -b CHG0123456
   ```

2. **Create your change directory**:
   ```bash
   mkdir changes/CHG0123456
   ```

3. **Add your configuration YAML file**:
   ```bash
   cp examples/user_input_example.yml changes/CHG0123456/device_config.yml
   ```

4. **Edit the YAML file** with your specific configuration:
   - Update BGP settings
   - Configure interfaces
   - Add VLANs
   - Set system parameters

5. **Submit a pull request**:
   - Title: Include your ServiceNow change request number
   - Description: Link to ServiceNow ticket and describe changes

6. **CI/CD Pipeline** will automatically:
   - Validate your YAML
   - Render the configuration
   - Run syntax checks
   - Update ServiceNow status

### For Administrators

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test configuration rendering**:
   ```bash
   python scripts/render_config.py examples/user_input_example.yml --validate
   ```

## Configuration Examples

See `examples/user_input_example.yml` for a complete example of how to structure your YAML configuration files.

## Templates

The system uses modular Jinja2 templates:
- **BGP**: `templates/arista/bgp.j2`
- **Routing Filters**: `templates/arista/routing_filters.j2`
- **Interfaces**: `templates/arista/interfaces.j2`
- **VLANs**: `templates/arista/vlans.j2`
- **System**: `templates/arista/system.j2`

## GitHub Actions Workflow

The CI/CD pipeline triggers on pull requests to the `changes/` directory and:
1. Validates YAML syntax
2. Renders configurations using Jinja2 templates
3. Performs basic configuration validation
4. Updates ServiceNow change request status
5. Prepares configurations for deployment upon approval

## ServiceNow Integration

- Branch names must match ServiceNow change request numbers (e.g., `CHG0123456`)
- Pull request status automatically syncs with ServiceNow tickets
- Configuration deployment triggers ServiceNow updates
