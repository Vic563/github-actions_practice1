#!/usr/bin/env python3
"""
Network Configuration Renderer

This script reads user-provided YAML input files and renders them using
Jinja2 templates to generate complete network device configurations.
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class ConfigRenderer:
    def __init__(self, templates_dir="templates/arista", output_dir="output"):
        """
        Initialize the configuration renderer
        
        Args:
            templates_dir (str): Directory containing Jinja2 templates
            output_dir (str): Directory to output rendered configurations
        """
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Template mapping
        self.template_files = {
            'bgp': 'bgp.j2',
            'routing_filters': 'routing_filters.j2', 
            'interfaces': 'interfaces.j2',
            'vlans': 'vlans.j2',
            'system': 'system.j2'
        }
    
    def load_yaml_input(self, input_file):
        """
        Load and parse YAML input file
        
        Args:
            input_file (str): Path to YAML input file
            
        Returns:
            dict: Parsed YAML data
        """
        try:
            with open(input_file, 'r') as f:
                data = yaml.safe_load(f)
            print(f"✅ Successfully loaded input file: {input_file}")
            return data
        except FileNotFoundError:
            print(f"❌ Error: Input file not found: {input_file}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML file: {e}")
            sys.exit(1)
    
    def render_template(self, template_name, data):
        """
        Render a specific template with provided data
        
        Args:
            template_name (str): Name of template to render
            data (dict): Data to pass to template
            
        Returns:
            str: Rendered configuration
        """
        try:
            template_file = self.template_files[template_name]
            template = self.env.get_template(template_file)
            rendered = template.render(**data)
            return rendered
        except TemplateNotFound:
            print(f"⚠️  Warning: Template not found: {template_file}")
            return ""
        except Exception as e:
            print(f"❌ Error rendering template {template_name}: {e}")
            return ""
    
    def render_all_templates(self, data, device_name="device", output_file=None):
        """
        Render all templates and create complete configuration
        
        Args:
            data (dict): Input data from YAML file
            device_name (str): Name of the device for output file
            output_file (Path): Custom output file path
            
        Returns:
            str: Complete rendered configuration
        """
        print("🔄 Rendering configuration templates...")
        
        config_sections = []
        
        # Render each template section
        for template_name in self.template_files.keys():
            print(f"   Rendering {template_name}...")
            rendered = self.render_template(template_name, data)
            if rendered.strip():  # Only add non-empty sections
                config_sections.append(rendered)
        
        # Combine all sections
        complete_config = "\n".join(config_sections)
        
        # Write to output file in change request folder
        if not output_file:
            output_file = self.output_dir / f"{device_name}_config.txt"
        with open(output_file, 'w') as f:
            f.write(complete_config)
        
        print(f"✅ Configuration rendered successfully: {output_file}")
        return complete_config
    
    def validate_config(self, config_text):
        """
        Basic validation of rendered configuration
        
        Args:
            config_text (str): Rendered configuration text
            
        Returns:
            bool: True if validation passes
        """
        print("🔍 Validating configuration...")
        
        validation_errors = []
        
        # Basic syntax checks
        lines = config_text.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('!'):
                continue
                
            # Check for common syntax issues
            if line.endswith(' '):
                validation_errors.append(f"Line {i}: Trailing whitespace")
            
            # Add more validation rules as needed
        
        if validation_errors:
            print("❌ Validation errors found:")
            for error in validation_errors:
                print(f"   {error}")
            return False
        
        print("✅ Configuration validation passed")
        return True


def main():
    parser = argparse.ArgumentParser(description='Render network configurations from YAML input')
    parser.add_argument('input_file', help='Path to YAML input file')
    parser.add_argument('--device-name', default='device', help='Device name for output file')
    parser.add_argument('--templates-dir', default='templates/arista', help='Templates directory')
    parser.add_argument('--output-dir', default=None, help='Output directory')
    parser.add_argument('--validate', action='store_true', help='Validate rendered configuration')
    
    args = parser.parse_args()
    
    # Initialize renderer
    renderer = ConfigRenderer(
        templates_dir=args.templates_dir,
        output_dir=args.output_dir or "output"
    )
    
    # Load input data
    data = renderer.load_yaml_input(args.input_file)
    
    # Render configuration
    # Determine the output path within the change request folder
    if args.output_dir:
        output_file = Path(args.output_dir) / f"{args.device_name}_config.txt"
    else:
        output_file = Path(args.input_file).parent / f"{args.device_name}_config.txt"

    config = renderer.render_all_templates(data, args.device_name, output_file)
    
    # Validate if requested
    if args.validate:
        validation_passed = renderer.validate_config(config)
        if not validation_passed:
            sys.exit(1)
    
    print(f"🎉 Configuration rendering complete!")


if __name__ == "__main__":
    main()
