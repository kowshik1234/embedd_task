import json
import re

def load_json(json_file):
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file}")
        exit(1)
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        exit(1)

def validate_config(config):
    required_fields = ["mcu", "core-type", "Floating point", "peripherals"]
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required field '{field}'")
            exit(1)

    if not re.match(r"STM32[A-Z]\d+", config["mcu"]):
        print(f"Error: Invalid MCU format: {config['mcu']}")
        exit(1)
    if not re.match(r"ARM Cortex M\d+[A-Z]*", config["core-type"]):
        print(f"Error: Invalid core-type format: {config['core-type']}")
        exit(1)
    if config["Floating point"] not in ["True", "False"]:
        print(f"Error: Invalid Floating point value: {config['Floating point']}")
        exit(1)

    peripherals = config["peripherals"]
    if not isinstance(peripherals, dict):
        print("Error: 'peripherals' must be an object")
        exit(1)

    for gpio in peripherals.get("gpio", []):
        required_keys = ["pin", "direction", "pull", "speed", "alt_function"]
        if not all(key in gpio for key in required_keys):
            print(f"Error: Invalid GPIO config, missing keys: {gpio}")
            exit(1)
        if not re.match(r"P[A-Z]\d+", gpio["pin"]):
            print(f"Error: Invalid GPIO pin format: {gpio['pin']}")
            exit(1)
        if gpio["direction"] not in ["input", "output"]:
            print(f"Error: Invalid GPIO direction: {gpio['direction']}")
            exit(1)
        if gpio["pull"] not in ["none", "up", "down"]:
            print(f"Error: Invalid GPIO pull: {gpio['pull']}")
            exit(1)
        if gpio["speed"] not in ["low", "medium", "high"]:
            print(f"Error: Invalid GPIO speed: {gpio['speed']}")
            exit(1)
        if not isinstance(gpio["alt_function"], list):
            print(f"Error: GPIO alt_function must be a list: {gpio['alt_function']}")
            exit(1)

    for uart in peripherals.get("uart", []):
        required_keys = ["interface", "baudrate", "tx_pin", "rx_pin", "parity"]
        if not all(key in uart for key in required_keys):
            print(f"Error: Invalid UART config, missing keys: {uart}")
            exit(1)
        if not re.match(r"USART\d+", uart["interface"]):
            print(f"Error: Invalid UART interface: {uart['interface']}")
            exit(1)
        if not isinstance(uart["baudrate"], int) or uart["baudrate"] <= 0:
            print(f"Error: Invalid UART baudrate: {uart['baudrate']}")
            exit(1)
        if not all(re.match(r"P[A-Z]\d+", pin) for pin in [uart["tx_pin"], uart["rx_pin"]]):
            print(f"Error: Invalid UART pin format: {uart['tx_pin']}, {uart['rx_pin']}")
            exit(1)
        if uart["parity"] not in ["none", "even", "odd"]:
            print(f"Error: Invalid UART parity: {uart['parity']}")
            exit(1)

    for i2c in peripherals.get("i2c", []):
        required_keys = ["interface", "scl_pin", "sda_pin", "speed"]
        if not all(key in i2c for key in required_keys):
            print(f"Error: Invalid I2C config, missing keys: {i2c}")
            exit(1)
        if not re.match(r"I2C\d+", i2c["interface"]):
            print(f"Error: Invalid I2C interface: {i2c['interface']}")
            exit(1)
        if not all(re.match(r"P[A-Z]\d+", pin) for pin in [i2c["scl_pin"], i2c["sda_pin"]]):
            print(f"Error: Invalid I2C pin format: {i2c['scl_pin']}, {i2c['sda_pin']}")
            exit(1)
        if i2c["speed"] not in ["100kHz", "400kHz"]:
            print(f"Error: Invalid I2C speed: {i2c['speed']}")
            exit(1)

    for timer in peripherals.get("timers", []):
        required_keys = ["timer", "prescaler", "frequency", "mode"]
        if not all(key in timer for key in required_keys):
            print(f"Error: Invalid timer config, missing keys: {timer}")
            exit(1)
        if not re.match(r"TIM\d+", timer["timer"]):
            print(f"Error: Invalid timer name: {timer['timer']}")
            exit(1)
        if not isinstance(timer["prescaler"], int) or timer["prescaler"] < 0:
            print(f"Error: Invalid timer prescaler: {timer['prescaler']}")
            exit(1)
        if not re.match(r"\d+[kM]?Hz", timer["frequency"]):
            print(f"Error: Invalid timer frequency: {timer['frequency']}")
            exit(1)
        if timer["mode"] not in ["counter", "pwm"]:
            print(f"Error: Invalid timer mode: {timer['mode']}")
            exit(1)

def print_config(config):
    print(json.dumps(config, indent=2))

json_file_path = "config.json"

config = load_json(json_file_path)
validate_config(config)
print_config(config)