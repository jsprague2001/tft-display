# tft-display

## Setup new Raspberry PI 4
```
$ sudo apt update
$ sudo apt upgrade
```

## Setup system-wide libraries
```
$ sudo apt install python3-pip
$ sudo apt-get install python3-venv
$ sudo apt-get install git
```

## Clone repository
```
# Run in home directory
$ git clone https://github.com/jsprague2001/tft-display.git
$ ls -l
drwxr-xr-x 6 admin admin 4096 Jan 31 16:48 tft-display
```

## Setup SPI display
```
# Interface Options -> SPI -> Enable
$ sudo raspi-config
```

## Setup Python Virtual Environment
```
$ cd tft-display
$ python -m venv --system-site-packages v_env
$ source ./v_env/bin/activate
(v_env) admin@lcdnas:$
```

## Setup a systemd service

```
$ cat tftdisplay.service
# Install the service
$ sudo cp tftdisplay.service /etc/systemd/system/tftdisplay.service
```
Problems with the service? Check permissions in ```/etc/systemd/system/```

## Manage services

```
$ sudo systemctl start tftdisplay.service
$ sudo systemctl enable tftdisplay.service
$ systemctl status tftdisplay.service

# Service logging
$ journalctl -u tftdisplay.service

# Log messages for the current boot:
$ journalctl -u tftdisplay.service -b
```

