---
name: sensor-manager
description: Help users deploy, configure, manage, troubleshoot, and perform operations on LimaCharlie endpoint sensors across Windows, macOS, Linux, Chrome, and Edge platforms.
---

# LimaCharlie Sensor Manager

This skill provides comprehensive guidance for deploying, configuring, managing, and troubleshooting LimaCharlie endpoint sensors (also called endpoint agents). Use this skill when users need help with sensor installation, sensor commands, sensor management, tagging, versioning, or any sensor-related operations.

## What You'll Find Here

- **Quick Start**: Deploy your first sensor in minutes
- **Common Operations**: The most frequently used sensor tasks
- **Sensor Management**: List, filter, tag, and organize sensors
- **Installation Keys**: Configure and use installation keys effectively
- **Navigation**: Find detailed guides for specific topics

For comprehensive information, see:
- [Command Reference](./REFERENCE.md) - All 60+ sensor commands with syntax and platform support
- [Deployment Guide](./DEPLOYMENT.md) - Complete platform-specific installation instructions
- [Troubleshooting Guide](./TROUBLESHOOTING.md) - Resolve connectivity, permissions, and performance issues

---

## Sensor Overview

### What are LimaCharlie Sensors?

LimaCharlie sensors (also called endpoint agents) are lightweight agents that run on endpoints to collect EDR (Endpoint Detection and Response) telemetry and forward it to the LimaCharlie cloud platform. Sensors provide deep visibility into endpoint activity while maintaining minimal performance impact.

**Key Characteristics:**
- Serverless, scalable solution for endpoint monitoring
- Support for Windows, macOS, Linux, Chrome, and Edge platforms
- Over 60 commands for file operations, memory operations, process operations, and more
- Single TCP connection over port 443 with pinned SSL certificates
- Two-component architecture: on-disk agent and over-the-air core

### Sensor Architecture

The LimaCharlie endpoint agent consists of two independently versioned components:

1. **On-disk agent**: Implements core identity, cryptography, and transport mechanisms. Rarely requires updates and typically remains static.
2. **Over-the-air core**: The main component that receives frequent updates (every few weeks) and delivers advanced functionality. Can be easily updated via the LimaCharlie cloud. Update size is generally 3-5 MB.

---

## Quick Start

### Deploy Your First Sensor

**1. Get your installation key:**
- Navigate to **Sensors > Installation Keys** in the web app
- Copy an existing key or create a new one with appropriate tags

**2. Choose your platform:**

**Windows:**
```bash
# Download and install
hcp_win_x64_release.exe -i YOUR_INSTALLATION_KEY
```

**macOS:**
```bash
# Download, make executable, install
chmod +x lc_sensor
sudo ./lc_sensor -i YOUR_INSTALLATION_KEY
# Grant required permissions when prompted
```

**Linux (Debian):**
```bash
# Install with dpkg
echo "limacharlie limacharlie/installation_key string YOUR_KEY" | sudo debconf-set-selections && sudo dpkg -i limacharlie.deb
```

**Linux (Other):**
```bash
# Install with custom script
chmod +x lc_sensor
sudo ./lc_sensor -d YOUR_INSTALLATION_KEY
```

**3. Verify enrollment:**
- Check **Sensors** page in web app
- Your new sensor should appear within 1-2 minutes

For complete platform-specific instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

---

## Working with Timestamps

**IMPORTANT**: When users provide relative time offsets (e.g., "last hour", "past 24 hours", "last week"), you MUST dynamically compute the current epoch timestamp based on the actual current time. Never use hardcoded or placeholder timestamps.

### Computing Current Epoch

```python
import time

# Compute current time dynamically
current_epoch_seconds = int(time.time())
current_epoch_milliseconds = int(time.time() * 1000)
```

**The granularity (seconds vs milliseconds) depends on the specific API or MCP tool**. Always check the tool signature or API documentation to determine which unit to use.

### Common Relative Time Calculations

**Example: "Show sensor activity from the last hour"**
```python
end_time = int(time.time())  # Current time
start_time = end_time - 3600  # 1 hour ago
```

**Common offsets (in seconds)**:
- 1 hour = 3600
- 24 hours = 86400
- 7 days = 604800
- 30 days = 2592000

**For millisecond-based APIs, multiply by 1000**.

### Critical Rules

**NEVER**:
- Use hardcoded timestamps
- Use placeholder values like `1234567890`
- Assume a specific current time

**ALWAYS**:
- Compute dynamically using `time.time()`
- Check the API/tool signature for correct granularity
- Verify the time range is valid (start < end)

---

## Installation Keys

### What are Installation Keys?

Installation keys are Base64-encoded strings that associate sensors with the correct Organization. They provide a way to label and control your deployment population.

**Four Components of an Installation Key:**
1. **Organization ID (OID)**: The Organization ID that this key should enroll into
2. **Installer ID (IID)**: Generated and associated with every installation key
3. **Tags**: A list of tags automatically applied to sensors enrolling with the key
4. **Description**: Helps differentiate uses of various keys

### Managing Installation Keys

Installation keys can be managed on the **Sensors > Installation Keys** page in the web app.

### Use Installation Keys for Classification

Use different installation keys to classify and organize your sensor deployments:

**Examples:**
- Key with "server" tag for server installations
- Key with "vip" tag for executive machines
- Key with "sales" tag for sales department
- Key with "production" tag for production environments
- Key with "staging" tag for staging environments

This enables you to:
- Write different detection and response rules for different host types
- Apply different security policies based on tags
- Organize and filter sensors effectively

### Installation Key Best Practices

1. **Create multiple keys** for different use cases
2. **Use descriptive names** for easy identification
3. **Apply tags automatically** via installation keys
4. **Document key usage** for team reference

**Example Key Structure:**
- `prod-servers`: Production servers with tags `production`, `server`
- `prod-workstations`: Production workstations with tags `production`, `workstation`
- `dev-servers`: Development servers with tags `development`, `server`
- `vip-users`: Executive machines with tags `vip`, `workstation`

### Proxy Support

The LimaCharlie sensor supports unauthenticated proxy tunneling through HTTP CONNECT.

**Configuration:**
Set the `LC_PROXY` environment variable to the DNS or hostname of the proxy:
```
LC_PROXY=proxy.corp.com:8080
```

**Windows-specific:**
- Use `LC_PROXY=-` for auto-detection of globally-configured, unauthenticated proxy
- The sensor will query: `HKLM\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyServer`
- Use `LC_PROXY=!` to explicitly disable proxy

---

## Common Operations

### 1. List Running Processes

```
os_processes
```

Shows all running processes on the endpoint with PID, name, and path information.

### 2. Retrieve a File

```
file_get --path "C:\Windows\System32\suspicious.exe"
```

Downloads a file from the endpoint for analysis. The file is stored in the LimaCharlie cloud and available for download.

### 3. Network Isolate a Sensor

```
segregate_network
```

Isolates the endpoint from the network while maintaining connection to LimaCharlie. Use this during incident response to contain threats.

**Restore network connectivity:**
```
rejoin_network
```

### 4. Kill a Malicious Process

```
os_kill_process --pid 1234
```

Terminates a process by PID. Useful for stopping malicious processes during incident response.

### 5. Get System Information

```
os_version
```

Returns detailed OS version information including build, architecture, and system details.

For all available commands, see [REFERENCE.md](./REFERENCE.md).

---

## Sensor Management

### Listing Sensors

**In Web App:**
- Navigate to Sensors section
- View all enrolled sensors with metadata

**Via API/SDK (Python):**
```python
import limacharlie
lc = limacharlie.Manager()
for sensor in lc.sensors():
    print(sensor.sid, sensor.hostname)
```

### Filtering Sensors

Use **Sensor Selector Expressions** to filter sensors based on characteristics.

#### Available Fields

- `sid`: Sensor ID
- `oid`: Organization ID
- `iid`: Installation Key ID
- `plat`: Platform name (windows, linux, macos, chrome, etc.)
- `ext_plat`: Extended platform name
- `arch`: Architecture (x86, x64, arm, arm64)
- `enroll`: Enrollment timestamp (epoch seconds)
- `hostname`: Hostname
- `mac_addr`: Latest MAC address
- `alive`: Last connection timestamp (epoch seconds)
- `ext_ip`: Last external IP
- `int_ip`: Last internal IP
- `isolated`: Boolean - network isolated
- `should_isolate`: Boolean - marked for isolation
- `kernel`: Boolean - has kernel-level visibility
- `did`: Device ID
- `tags`: List of tags

#### Operators

- `==`: Equals
- `!=`: Not equal
- `in`: Element in list, or substring in string
- `not in`: Element not in list, or substring not in string
- `matches`: Matches regular expression
- `not matches`: Does not match regular expression
- `contains`: String contained within element

#### Example Selector Expressions

**All sensors with "test" tag:**
```
test in tags
```

**All Windows boxes with internal IP starting with 10.3.x.x:**
```
plat == windows and int_ip matches ^10\.3\..*
```

**All Linux sensors with network isolation or "evil" tag:**
```
plat == linux or (isolated == true or evil in tags)
```

**All Azure-related platforms:**
```
plat contains "azure"
```

**All sensors with platform starting with a number (use backticks):**
```
plat == `1password`
```

### Tagging Sensors

#### Tag Use Cases
- **Classification**: Departments (sales, finance), usage type (workstation, server), importance (vip, critical)
- **Automation**: Trigger different detection rules, apply response actions, route detections to outputs

#### Adding Tags
1. **Via Installation Key**: Tags automatically applied during enrollment
2. **Via API**: `POST /{sid}/tags`
3. **Via D&R Rule**: Use `add tag` action in response section
4. **Via Web App**: Click sensor to expand, then add/edit/remove tags

#### System Tags

Special tags that control sensor behavior:

- `lc:latest`: Use latest sensor version (for testing)
- `lc:stable`: Use stable sensor version
- `lc:experimental`: Use experimental sensor version
- `lc:no_kernel`: Disable kernel component
- `lc:debug`: Use debug version of sensor
- `lc:limit-update`: Only update version at startup/reboot
- `lc:sleeper`: Enter sleeper mode (minimal activity)
- `lc:usage`: Usage-based billing mode

### Deleting Sensors

**Via Web App:**
Navigate to sensor, click delete.

**Via API/SDK:**
```python
import limacharlie
lc = limacharlie.Manager()
sensor = lc.sensor('SENSOR_ID')
sensor.delete()
```

**Note:** Deleting a sensor from the platform does not uninstall it from the endpoint. Use the `uninstall` command to remove the agent from the endpoint.

---

## Versioning and Upgrades

### Version Labels

LimaCharlie provides three version labels:

1. **Latest**: Most recent release with new fixes and features
2. **Stable**: Less frequently updated, ideal for slower update cadences
3. **Experimental**: Beta version of next "Latest" release

### Managing Sensor Versions

**Organization-Level:**
Set the default sensor version for your organization via web interface or API.

**Individual Sensor-Level:**
Use system tags to override organization default:
- `lc:latest`: Receive latest version
- `lc:stable`: Receive stable version
- `lc:experimental`: Receive experimental version

### Update Mechanisms

**Manual Update:**
Click button in web interface to update all sensors in organization. Updates take effect within 20 minutes.

**Auto-Update:**
Apply `lc:stable` tag to automatically update to latest stable version upon release.

**Staged Deployment:**
1. Tag representative sensors with `lc:latest`
2. Monitor for issues (stability, performance, telemetry quality)
3. If successful, update organization-level version
4. Remove `lc:latest` tag from test sensors

### Best Practices for Updates

1. **Test First**: Apply `lc:latest` to small subset of representative systems
2. **Monitor**: Evaluate stability, performance, telemetry quality
3. **Diverse Testing**: Test across different OS versions and workloads
4. **Gradual Rollout**: Update organization-wide only after successful testing
5. **Rollback Plan**: Keep `lc:stable` tag ready for quick rollback
6. **Update Timing**: Schedule updates during maintenance windows

---

## Quick Reference

### Common Commands

```bash
# List processes
os_processes

# Get file
file_get --path "/path/to/file"

# Kill process
os_kill_process --pid 1234

# Network isolate
segregate_network

# Restore network
rejoin_network

# YARA scan
yara_scan --path "/path" --rule-name "signatures"

# Uninstall sensor
uninstall --is-confirmed

# Get system info
os_version
```

### Sensor Selector Examples

```
# All Windows servers
plat == windows and server in tags

# All isolated sensors
isolated == true

# All sensors in production
production in tags

# All sensors not seen in 24 hours
alive < {timestamp_24h_ago}

# All VIP workstations
vip in tags and workstation in tags
```

### System Tags Quick Reference

```
lc:latest       - Use latest version
lc:stable       - Use stable version
lc:experimental - Use experimental version
lc:no_kernel    - Disable kernel component
lc:debug        - Use debug version
lc:limit-update - Only update at startup
lc:sleeper      - Enter sleeper mode
lc:usage        - Usage-based billing
```

---

## Navigation

### Detailed Guides

- **[Command Reference](./REFERENCE.md)**: Complete list of all 60+ sensor commands with syntax, parameters, and platform support
- **[Deployment Guide](./DEPLOYMENT.md)**: Platform-specific installation instructions for Windows, macOS, Linux, Docker, Chrome, and Edge
- **[Troubleshooting Guide](./TROUBLESHOOTING.md)**: Resolve connectivity issues, permission problems, and performance concerns

### Documentation References

- Installation Keys: `/limacharlie/doc/Sensors/installation-keys.md`
- Sensor Tags: `/limacharlie/doc/Sensors/sensor-tags.md`
- Sensor Connectivity: `/limacharlie/doc/Sensors/sensor-connectivity.md`
- Versioning: `/limacharlie/doc/Sensors/Endpoint_Agent/endpoint-agent-versioning-and-upgrades.md`
- Uninstallation: `/limacharlie/doc/Sensors/Endpoint_Agent/endpoint-agent-uninstallation.md`
- Sleeper Mode: `/limacharlie/doc/Sensors/Endpoint_Agent/sleeper.md`

### API/SDK Resources

- REST API: https://api.limacharlie.io/static/swagger/
- Python SDK: https://github.com/refractionPOINT/python-limacharlie
- Go SDK: https://github.com/refractionPOINT/go-limacharlie

### Support

- Email: answers@limacharlie.io
- Community Slack: https://limacharlie.io/slack
- Documentation: https://doc.limacharlie.io

---

## When to Use This Skill

Use the sensor-manager skill when users ask about:

- Installing or deploying LimaCharlie sensors
- Sensor commands and capabilities
- Managing sensors (listing, filtering, tagging)
- Troubleshooting sensor issues
- Sensor versioning and updates
- Network isolation
- Platform-specific installation (Windows, macOS, Linux, Chrome, Edge)
- Enterprise deployment (MDM, Intune, custom installers)
- Installation keys and sensor enrollment
- Uninstalling sensors
- Performance optimization
- Sleeper mode deployments
- Containerized deployments (Docker, Kubernetes)
- Proxy configuration
- Permission issues (especially macOS)
- Sensor connectivity
- Sensor health monitoring

This skill provides comprehensive, authoritative guidance for all sensor-related operations in LimaCharlie.
