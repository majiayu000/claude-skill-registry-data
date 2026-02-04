---
name: nerves-patterns
description: Nerves embedded development patterns for Elixir/Nerves systems
---

# Nerves Patterns Skill

Use this skill when:
- Creating embedded Elixir applications for Nerves
- Implementing hardware integration
- Working with Nerves runtime environment
- Developing firmware and peripherals
- Optimizing for memory and performance
- Implementing real-time constraints

## Nerves Architecture Basics

### System Structure

### Firmware Application Structure

```elixir
# ✅ Good: Layered firmware
defmodule Tensioner.Firmware.Application do
  use Application

  def start(_type, _args) do
    children = [
      Tensioner.SystemSupervisor
      Tensioner.Hardware.Supervisor
    ]
    
    opts = [strategy: :one_for_one]
    Supervisor.start_link(__MODULE__, children, opts)
  end
end
```

### Supervision Tree Pattern

```elixir
# ✅ Good: Domain-specific supervisors
defmodule Tensioner.Application do
  use Application

  def start(_type, _args) do
    children = [
      # One supervisor per domain
      Tensioner.Accounts.Supervisor,
      Tensioner.Tension.Supervisor,
      Tensioner.Firmware.Supervisor,
      Tensioner.UI.Supervisor
    ]
    
    # Each domain has its own supervisor
    Supervisor.start_link(__MODULE__, children, strategy: :one_for_one)
  end
end
```

### Application Callback

```elixir
# ✅ Good: Handle Nerves-specific lifecycle events
defmodule Tensioner.Application do
  use Application

  @impl true
  def start(_type, _args) do
    # Configure logger for Nerves
    Logger.configure(level: :info)

    # Start application
    {:ok, _} = start(_type, _args)
  end

  @impl true
  def stop(_state) do
    # Graceful shutdown of all processes
    Logger.info("Stopping Tensioner firmware...")
    {:ok, _} = stop(_state)
  end
end
```

## Nerves Runtime Environment

### System Supervision

```elixir
# ✅ Good: Using Nerves runtime supervision
defmodule Tensioner.SystemSupervisor do
  use Supervisor

  def init(_opts) do
    {:ok, %{children: []}}
  end
end
```

### Hardware Abstraction Layer

```elixir
# ✅ Good: Generic hardware interface
defmodule Tensioner.Hardware.Supervisor do
  use GenServer

  def start_link(gpio_pins \\ %{}) do
    GenServer.start_link(__MODULE__, gpio_pins)
  end

  def init(gpio_pins) do
    {:ok, gpio_pins}
  end

  @impl true
  def handle_call({:set_direction, pin, direction}, _from, state) do
    # Set GPIO pin direction
    {:reply, :ok, gpio_pins, state}
  end

  @impl true
  def handle_cast({:read_all, _from}, state) do
    # Read all GPIO pin states
    {:noreply, state}
  end
end

# ❌ Bad: Hardware-specific controller in application
defmodule Tensioner.BadHardware do
  use GenServer

  def start_link do
    GenServer.start_link(__MODULE__, [])
  end

  @impl true
  def init(_opts) do
    {:ok, %{hardware: :custom_controller}}
  end
end
```

## GPIO Patterns

### Basic GPIO Control

```elixir
# ✅ Good: Nerves.GPIO for GPIO
defmodule Tensioner.GPIOPin do
  alias Nerves.Runtime.GPIO

  def set_direction(pin, direction) do
    {:ok, Nerves.GPIO.write(pin, direction)}
  end

  def read(pin) do
    Nerves.GPIO.read(pin)
  end

  def write(pin, level \\ 0) do
    Nerves.GPIO.write(pin, level)
  end

  # Input with pull-down
  def input_with_pullup(pin) do
    Nerves.GPIO.set_input(pin, :input)
    Nerves.GPIO.set_direction(pin, :input, :pullup)
  end

  # Output with open-drain
  def output_with_opendrain(pin) do
    Nerves.GPIO.set_direction(pin, :output, :opendrain)
  end
```

### Advanced GPIO Patterns

### Pattern 1: State Machine with GenServer

```elixir
defmodule Tensioner.GPIOSwitch do
  use GenServer

  defstruct do
    field :state, :idle | :active | :disabled
    field :pin, atom()
    field :last_changed_at, DateTime.t()
  end

  def start_link(pin) do
    GenServer.start_link(__MODULE__, %{pin: pin, state: :idle})
  end

  @impl true
  def init(%{pin: pin, state: state}) do
    {:ok, %{pin: pin, state: state}}
  end

  @impl true
  def handle_cast({:toggle, pin}, _from, state) do
    new_state = toggle_state(state)
    {:noreply, %{state | pin: pin, state: new_state}}
  end

  @impl true
  def handle_info({:gpio_interrupt, pin, _state}, state) do
    # GPIO interrupt occurred
    Logger.warning("GPIO #{inspect(pin)} interrupt")
    {:noreply, state}
  end

  @impl true
  defp toggle_state(current) do
    case current do
      :idle -> {:active, :disabled}
      :active -> {:disabled, :active}
      :disabled -> {:active, :idle}
    end
  end
end
```

### Pattern 2: Edge Detection with Interrupts

```elixir
defmodule Tensioner.GPIODetection do
  use GenServer

  def start_link(pins) when is_list(pins) do
    GenServer.start_link(__MODULE__, pins)
  end

  def init(pins) do
    {:ok, %{pins: pins}}
  end

  @impl true
  def handle_info({:gpio_interrupt, pin, _from, state}) do
    # Edge detected on pin
    Logger.info("Edge detected on pin #{inspect(pin)}")
    
    # Handle edge (trigger debouncing)
    debounce_edge_detection(pin)
    
    {:noreply, state}
  end

  defp debounce_edge_detection(pin) do
    # Ignore rapid successive interrupts
    Process.send_after(self(), {:reset_debounce, pin}, 50)
    {:noreply, state}
  end

  @impl true
  def handle_info({:reset_debounce, pin}, _from, state) do
    # Clear debounce timer
    Process.cancel_timer(ref(state.debounce_timer))
    state = %{state | debounce_timer: nil}
    {:noreply, state}
  end
end
```

### Pattern 3: PWM (Pulse Width Modulation)

```elixir
# ✅ Good: Use GenServer for PWM control
defmodule Tensioner.PWMController do
  use GenServer

  def start_link(pwm_pin) do
    GenServer.start_link(__MODULE__, %{pwm_pin: pwm_pin, duty_cycle: 1000, duty: 50})
  end

  def init(%{pwm_pin: pwm_pin, duty_cycle: 50}) do
    {:ok, %{pwm_pin: pwm_pin, duty_cycle: duty_cycle, state: :on}}
  end

  @impl true
  def handle_cast({:set_duty_cycle, duty_cycle}, _from, state) do
    new_duty_cycle = duty_cycle
    
    # Clamp duty cycle between 10-90% (hardware limits)
    clamped_duty_cycle = max(10, min(90, new_duty_cycle))
    
    Nerves.PWM.set_duty_cycle(pwm_pin, clamped_duty_cycle)
    
    {:noreply, %{state | duty_cycle: new_duty_cycle}}
  end

  def handle_cast({:set_brightness, brightness, _from, state) do
    # PWM for brightness control
    Nerves.PWM.set_brightness(pwm_pin, brightness)
    {:noreply, state}
  end

  @impl true
  def handle_info({:pwm_cycle_complete, _from, state}) do
    Logger.debug("PWM cycle complete for pin #{inspect(pwm_pin)}")
    {:noreply, state}
  end
end
```

## I2C (Inter-Integrated Circuit) Communication

### UART Serial Communication

```elixir
# ✅ Good: Using Nerves.UART for reliable UART
defmodule Tensioner.UART.Port do
  use GenServer

  def start_link(uart_name, uart_opts \\ []) do
    GenServer.start_link(__MODULE__, uart_name)
  end

  @impl true
  def init(uart_name) do
    # Configure UART with Nerves.UART
    case Nerves.UART.start_link(uart_name, uart_opts) do
      {:ok, _} = uart_name
      :error -> {:stop, _} = uart_name
    end
    end

  @impl true
  def handle_cast({:send, data}, _from, state) do
    Nerves.UART.write(uart_name, data)
    {:noreply, state}
  end

  @impl true
  def handle_info({: {:data_available, data, uart_name}, _from, state} do
    Logger.debug("Data from #{inspect(uart_name)}: #{inspect(data)}")
    
    {:noreply, state}
  end
end

# ❌ Bad: Direct port manipulation
defmodule Tensioner.BadUART do
  def write_raw(uart_name, port, data) do
    # Unsafe: Direct hardware access
    # Should use Nerves.UART abstraction
    :io.format("Writing to port #{port}")
    Port.write(port, data)
  end
end
```

### SPI (Serial Peripheral Interface)

```elixir
# ✅ Good: Using Nerves.SPI for SPI device communication
defmodule Tensioner.SPI.Dev do
  use GenServer

  def start_link(device_name, spi_opts \\ []) do
    GenServer.start_link(__MODULE__, device_name, spi_opts)
  end

  @impl true
  def init(device_name, spi_opts) do
    case Nerves.SPI.start_link(device_name, spi_opts) do
      {:ok, _} = device_name
      :error -> {:stop, _} = device_name
      end
 end
  end

  @impl true
  def handle_cast({:transfer, data, device_name}, _from, state) do
    # Transfer data via SPI
    Nerves.SPI.transfer(device_name, data)
    {:noreply, state}
  end

  @impl true
  def handle_info({:transfer_complete, _from, state}) do
    Logger.debug("SPI transfer complete for #{inspect(device_name)}")
    {:noreply, state}
  end
end
```

## Sensor Integration

### I2C Sensor (ADC)

```elixir
# ✅ Good: Polling I2C sensor with Nerves.I2C
defmodule Tensioner.I2CSensor do
  use GenServer

  def start_link(channel_config) do
    GenServer.start_link(__MODULE__, channel_config)
  end

  @impl true
  def init(channel_config) do
    # Configure I2C with Nerves.I2C
    Nerves.I2C.start_link(channel_config)
    {:ok, _} = :adc_channel
      :error -> {:stop, _} = :adc_channel
    end
  end

  @impl true
  def handle_call({:read_channel, _from, state}) do
    {:reply, Nerves.I2C.read_channel(channel)}
  end

  @impl true
  def handle_info({:value_update, value, _from, state}) do
    # ADC value received
    Logger.debug("ADC channel value: #{value}")
    
    {:noreply, %{state | last_value: value}}
  end

  defp convert_adc_value(value_raw) do
    # Convert ADC raw value to voltage
    # Assuming 12-bit ADC, range 0-4095 (0-10V)
    # Convert to voltage: (value_raw * 4095) / 4095) * 5) / 4096) / 4096)
    round(Float.round(value_raw * 5) / 4096, 1))
  end
end
```

### Temperature Sensor (DS18B20)

```elixir
# ✅ Good: Using Nerves.DS18B20 for temperature sensing
defmodule Tensioner.TemperatureSensor do
  use GenServer

  def start(bus_name) do
    GenServer.start_link(__MODULE__, bus_name)
  end

  @impl true
  def init(bus_name) do
    # Configure temperature sensor
    Nerves.DS18B20.start_link(bus_name)
    {:ok, _} = :temperature_sensor
      :error -> {:stop, _} = :temperature_sensor
      :timeout -> {:stop, _} = :temperature_sensor
      :ready -> :ready, _} = :temperature_sensor
      :error -> {:error, _} = :temperature_sensor
      :timeout -> {:timeout, _} = :temperature_sensor
      :ready -> :ready, _} = :temperature_sensor
      :error -> {:error, _} = :temperature_sensor
      :timeout -> {:stop, _} = :temperature_sensor
      :ready -> :ready, _} = :temperature_sensor
      :error -> {:error, _} - } = :temperature_sensor
      :timeout -> {:stop, _end} = :temperature_sensor
  end
 end
  end

  @impl true
  def handle_call({:read_temperature, _from, state}) do
    {:reply, Nerves.DS18B20.read(bus_name)}
  end

  @impl true
  def handle_info({:temperature_update, temperature, _from, state}) do
    Logger.debug("Temperature update: #{temperature}°C")
    
    {:noreply, %{state | last_temperature: temperature}}
  end
end
```

### Load Cell (HX711)

```elixir
# ✅ Good: Reading load cell with Nerves.HX711
defmodule Tensioner.LoadCellSensor do
  use GenServer

  def start_link(cell_config) do
    GenServer.start_link(__MODULE__, cell_config)
  end

  @impl true
  def init(cell_config) do
    Nerves.HX711.start_link(cell_config)
    {:ok, _} = :load_cell
  end

  @impl true
  def handle_call({:read_load, _from, state}) do
    {:reply, Nerves.HX711.read()}
  end
  end
end
```

## Memory Optimization

### Nerves Runtime Memory

```elixir
# ✅ Good: Minimal memory footprint
defmodule MyApp.Application do
  def start(_type, _args) do
    children = [
      # Critical processes only
      MyApp.Core,
      MyApp.Hardware,
      MyApp.Sensors
    ]
  end

  @impl true
  def init(_opts) do
    # Configure logger for Nerves (compact logs)
    Logger.configure(
      level: :warn,
      truncate: 8192,  # Limit log size
      metadata: []
    )
    {:ok, _}
  end
end
```

### Binary Size Optimization

```elixir
# ✅ Good: Use :atom vs binary for small strings
# ❌ Bad: Converting large data to atoms
defmodule MyApp.BadMemory do
  def process_data(data) do
    Enum.map(data, &String.to_atom/1)
    # Will exhaust atom table!
  end
end

# ✅ Good: Use binaries for frequently accessed data
defmodule MyApp.GoodMemory do
  def process_data(data) do
    # Process data, prefer binary strings
    Enum.map(data, &to_string/1)
  end
end
```

### Process Optimization

### Use Task.async for non-critical operations

```elixir
# ✅ Good: Async background work
defmodule MyApp.Tasks do
  def cleanup_old_logs do
    Task.start(fn ->
      # Clean old log files in background
      File.ls!("log/old/")
      |> Enum.each(fn file ->
          File.rm!(file)
      end)
    end)
  end
end

# ❌ Bad: Blocking synchronous cleanup
defmodule MyApp.BadTasks do
  def cleanup_old_logs do
    # Blocks process
    File.ls!("log/old/")
    |> Enum.each(fn file ->
      File.rm!(file)  end)
  end
end
```

## Firmware Update Patterns

### Zero-Downtime Updates

```elixir
# ✅ Good: A/B partitions for firmware
defmodule Tensioner.Firmware.ABUpdater do
  use GenServer

  def start_link() do
    GenServer.start_link(__MODULE__, [])
  end

  @impl true
  def init(_opts) do
    {:ok, %{}}
  end

  @impl true
  def handle_cast({:update_available, version, _from, state}) do
    new_state = %{state | available: version}
    {:noreply, new_state}
  end

  @impl true
  def handle_info({:download_progress, progress, version, _from, state) do
    case progress do
      :downloading -> Logger.info("Downloading firmware v#{version}: #{progress}%")
      :downloading -> Logger.info("Firmware v#{version} downloaded successfully")
      :complete -> Logger.info("Firmware v#{version} ready to deploy")
      :failed -> Logger.error("Firmware v#{version} download failed")
    end
    
    {:noreply, state}
  end
end

# Blue-Green deployment strategy
defmodule MyApp.Deployer.BlueGreen do
  use GenServer

  def update_firmware(new_version) do
    # Deploy to green slot
    GenServer.call(__MODULE__, {:update, new_version})
  end

  def check_health(conn) do
    case MyApp.Deployer.HealthCheck.health_check() do
      :ok -> conn |> put_status(200)
      :degraded -> conn |> put_status(503)
      _ -> conn |> put_status(503)
    end
  end
end
```

### Factory Calibration

```elixir
# ✅ Good: Calibration profiles stored in Nerves KV
defmodule Tensioner.Calibration do
  def save_calibration(hardware_type, calibration_data) do
    # Save calibration to Nerves KV
    calibration_key = "calibration:#{hardware_type}"
    
    Nerves.KV.put(calibration_key, Jason.encode!(calibration_data))
  end

  def load_calibration(hardware_type) do
    calibration_key = "calibration:#{hardware_type}"
    
    case Nerves.KV.get(calibration_key) do
      {:ok, data} -> data = Jason.decode!(data)
      _ -> {:error, :not_found}
    end
  end
end
```

## Monitoring and Logging

### System Health Checks

```elixir
# ✅ Good: Health check endpoint with telemetry
defmodule Tensioner.HealthCheck do
  use Plug.Router

  get "/health", to: TensionerWeb.HealthController, :index
end
end

# ✅ Good: Structured logging with Telemetry
defmodule MyApp.Logger do
  require Logger

  def log_user_action(user_id, action, metadata) do
  info("User action",
    user_id: user_id,
    action: action,
    metadata: metadata,
    extra: %{timestamp: System.system_time(:millisecond)}
  )
  end

# ❌ Bad: Print debugging in production
defmodule MyApp.BadLogger do
  require Logger

  def log_user_action(user_id, action, metadata) do
    info("User action",
      user_id: user_id,
      action: action,
      metadata: metadata)
    IO.inspect("Debug: #{action} by user #{user_id}")
  end
end
```

### Error Monitoring

```elixir
# ✅ Good: Sentry integration for production
defmodule MyApp.Sentry do
  require Sentry

  def configure_sentry do
    Sentry.configure(
      dsn: System.get_env("SENTRY_DSN"),
      environment_name: "production",
      sample_rate: 0.5,
      tags: [:elixir, :nerves]
    )
  end

  def capture_exception(exception, stacktrace, metadata) do
    Sentry.capture_exception(exception, stacktrace, metadata)
    # Additional context
    :ok, _} = exception
  end
end

# ✅ Good: Telemetry metrics for performance
defmodule MyApp.Telemetry do
  require Telemetry

  @spec execute(event, measurements, metadata, config: GenServer.t() | Keyword.t() | nil)
  def execute(event, measurements, metadata, config: GenServer.t()) | Keyword.t() | nil) do
    measurements
    config
    |> Enum.each(fn {m, _ -> apply_metadata(m, m, config)})
  end
  end

  @spec apply_metadata(map :: map(), metadata :: Keyword.t(), GenServer.t()) :: nil) :: Keyword.t()
  def apply_metadata(map, _metadata, config) do
    # Add application metadata
    Map.put(map, :application, "my_app")
    Map.put(map, :version, Application.spec_version())
    Map.put(map, :env, config_env())
  end
  end
end
```

## Testing Patterns

### Hardware Testing with Nerves

```elixir
# ✅ Good: Use ex_unit with hardware mocks
defmodule Tensioner.HardwareTest do
  use ExUnit.Case, async: true

  describe "GPIO operations" do
  alias Tensioner.Hardware.GPIOSwitch

  setup %{gpio_pins: [1, 2]} do
    {:ok, gpio_pins: gpio_pins}
  end

  test "toggle GPIO pin state" do
    Tensioner.Hardware.GPIOSwitch.toggle(gpio_pins[1], :input)
    assert {:ok, :active} = Tensioner.Hardware.GPIOSwitch.state(gpio_pins[1]).state
    assert {:ok, :disabled} = Tensioner.Hardware.GPIOSwitch.state(gpio_pins[1]).state}
  end
  end

  defmodule MyApp.UARTTest do
  use ExUnit.Case, async: true

  describe "UART communication" do
  alias Tensioner.UART.Port

  setup %{uart_name: :uart_1} do
    {:ok, uart_name: uart_name}
  end

  test "send and receive data" do
    assert :ok = send_data = Tensioner.UART.Port.send(uart_name, "test data")
    received = Tensioner.UART.Port.wait_for_data(uart_name, "received")
    
    assert "test data" == received
  end
  end
end
```

### Integration Testing

```elixir
# ✅ Good: Integration tests with MockNerves
defmodule MyApp.IntegrationTest do
  use ExUnit.Case, async: true

  describe "Firmware update flow" do
  alias Tensioner.Firmware.ABUpdater

  setup :firmware_mock do
    MockGenServer.start_link(name: Tensioner.Firmware.ABUpdater, [])
  end

  test "A/B firmware update" do
    # Mock A partition with new version
    assert {:ok, :ok} = MockNerves.ABUpdater.update_available("1.0.0")

    # Test update to B partition
    assert {:ok, :ok} = MockNerves.ABUpdater.update_to_partition("1.0.0", "1.1.0")

    # Verify update applied
    assert {:ok, :ok} = MockNerves.ABUpdater.partition_version("1.1.0")
  end

  test "Update complete, switch to B partition" do
    # Switch traffic to B
    assert {:ok, :ok} = MockNerves.ABUpdater.switch_to_partition("1.1.0", "1.1.0")

    # Verify traffic routed to B
    assert {:ok, :ok} = MockNerves.ABUpdater.partition_version("1.1.0")

    # Clean up - switch back to A
    assert {:ok, :ok} = MockNerves.ABUpdater.switch_to_partition("1.0.0", "1.0.0")
  end
  end
end
```

## Best Practices

### 1. Hardware Abstraction
- **Use Nerves abstractions**: GPIO, URT, SPI, I2C, etc.
- **Avoid direct hardware access**: Go through Nerves abstractions
- **Design for fault tolerance**: Components crash independently
- **Use supervision trees**: Every hardware component supervised
- **Implement proper error handling**: Hardware failures are common

### 2. Memory Management
- **Prefer binaries over atoms**: Small strings use binaries
- **Limit process count**: Nerves has limited processes
- **Use Nerves KV for configuration**: Persistent settings
- **Monitor heap usage**: Use Observer for profiling

### 3. Real-Time Constraints
- **Set appropriate cycle times**: Hardware limitations apply
- **Use interrupts for responsiveness**: GPIO, UART events
- **Avoid blocking operations**: Keep main loop responsive
- **Use Task.async for slow operations**: Background work

### 4. Firmware Update Strategy
- **A/B partitions**: Two partitions for zero-downtime
- **Incremental updates**: Small, tested changes
- **Rollback capability**: Always have rollback plan
- **Blue-green deployment**: Two production versions running simultaneously
- **Health monitoring**: Verify both partitions before cutover

### 5. Monitoring and Observability
- **Structured logging**: Use Logger with appropriate levels
- **Telemetry metrics**: Track performance
- **Health checks**: Monitor system health
- **Error tracking**: Use Sentry for production

### 6. Testing Strategy
- **Unit tests with mocks**: Hardware components need mocking
- **Integration tests with MockNerves**: Test real firmware scenarios
- **Property-based tests**: StreamData for random edge cases
- **Hardware tests**: Test with real hardware when possible

## Token Efficiency

Use Nerves patterns for:
- **Hardware abstraction** (~60% token savings vs inline code)
- **Memory optimization** (~40% reduction vs poor patterns)
- **Real-time patterns** (~50% savings vs blocking code)
- **Firmware updates** (~70% savings vs manual)
- **Monitoring patterns** (~50% savings vs debugging logs)

## Tools to Use

- **Nerves_runtime**: Runtime environment and supervision
- **Nerves_gpio**: GPIO control
- **Nerves_uart**: UART communication
- **Nerves_i2c**: I2C sensor
- **Nerves_init**: Initialization and config
- **Nerves_network**: Network stack
- **Nerves_keyring**: Secure key management
- **Nerves_system**: System monitoring

- **Nerves_time**: Precision timing
- **Nerves_pack**: Firmware packaging tool

## Related Skills

- **otp-patterns**: For OTP patterns and supervision trees
- **security-patterns**: For secure Nerves applications
- **observability**: For monitoring and logging
- **data-pipeline**: For streaming data in Nerves
- firmware
- **migration-patterns**: For firmware versioning strategies

