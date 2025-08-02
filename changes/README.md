# Network Device Configuration Changes

This directory contains configuration changes tied to ServiceNow change requests.

## Workflow Process

1. **Create Branch**: User creates a new branch from `main` using their ServiceNow change request number
   ```bash
   git checkout -b CHG0123456
   ```

2. **Add Configuration**: User adds their configuration files to `changes/CHG0123456/`
   - Directory name should match the ServiceNow change request number
   - Include all relevant device configurations

3. **Submit Pull Request**: User submits PR with:
   - Branch name: ServiceNow change request number (e.g., `CHG0123456`)
   - PR title: Include ServiceNow change request number
   - PR description: Link to ServiceNow ticket and describe changes

4. **CI/CD Pipeline**: GitHub Actions will:
   - Validate configuration syntax
   - Run security checks
   - Test configurations (if applicable)
   - Update ServiceNow ticket status

5. **Review & Approval**: 
   - Network team reviews changes
   - PR approved = Change approved in ServiceNow
   - PR rejected = Change rejected with comments

6. **Deployment**: Upon PR merge, configurations are deployed to target devices

## Directory Structure

```
changes/
├── CHG0123456/          # ServiceNow change request number
│   ├── device1.cfg      # Device configuration files
│   ├── device2.cfg
│   └── metadata.yml     # Change metadata (optional)
├── CHG0123457/
│   └── ...
```

## ServiceNow Integration

- Branch names must match ServiceNow change request numbers
- PR status automatically syncs with ServiceNow tickets
- Configuration deployment triggers ServiceNow updates
