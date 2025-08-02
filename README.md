# Network Configuration Management with GitHub Actions

This repository provides an automated network configuration management system using GitHub Actions, Jinja2 templates, and ServiceNow integration.

## Overview

This system allows network engineers to:
1. Submit network configuration changes via pull requests
2. Use simple YAML files instead of complex Jinja2 templates
3. Automatically render configurations for Arista switches
4. Validate configurations before deployment
5. Review and approve changes through GitHub's PR process

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

1. **Create a new branch** named after your change request number:
   ```bash
   git checkout -b CHG0123456
   ```

2. **Create your change directory**:
   ```bash
   mkdir changes/CHG0123456
   ```

3. **Add your configuration YAML file for each device**:
   ```bash
   cp examples/user_input_example.yml changes/CHG0123456/device1_config.yml
   cp examples/user_input_example.yml changes/CHG0123456/device2_config.yml
   ```

4. **Edit each YAML file** with device-specific configuration:
   - Update BGP settings
   - Configure interfaces
   - Add VLANs
   - Set system parameters

5. **Push your changes** to trigger automatic rendering:
   ```bash
   git add changes/CHG0123456/
   git commit -m "Add device configurations for CHG0123456"
   git push
   ```

6. **GitHub Actions automatically**:
   - Renders your YAML files into device configurations
   - Validates the syntax
   - Commits the rendered `.txt` files back to your branch

7. **Review the auto-generated configurations** in your change folder

8. **Submit a pull request**:
   - Title: Include your change request number
   - Description: Describe the changes and devices affected
   - The PR will include both YAML inputs and rendered configurations

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

## Workflow Summary

1. **User creates branch** with change request number (e.g., `CHG0123456`)
2. **User adds YAML files** for each device in `changes/CHG0123456/`
3. **User fills out templates** with device-specific configuration
4. **Python script renders** configurations and saves them in same folder
5. **User submits PR** for review and approval
6. **Team reviews** rendered configurations and approves/rejects
7. **Upon approval**, configurations are ready for deployment
