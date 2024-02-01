# Waveshare 2.4inch LCD Module

https://www.waveshare.com/wiki/2.4inch_LCD_Module

As a 2.4inch TFT display module with a resolution of 240 * 320, it uses the SPI interface for communication. LCD has an internal controller with basic functions, which can be used to draw points, lines, circles, and rectangles, and can display English, Chinese as well as pictures.
We provide complete supporting Raspberry Pi demos (BCM2835 library, WiringPi library, and python demos), STM32 demos, and Arduino demos.

## Specification
* Operating voltage: 3.3V/5V (When using 5V power supply, the logic voltage is 5V; When using 3.3V power supply, the logic voltage is 3.3V.)
* Interface: SPI
* LCD Type: TFT
* Controller: IL9341
* Resolution: 240(V) x 320(H)RGB
* Display Size: 36.72（H）x 48.96（V）mm
* Pixel Size: 0.153（H）x 0.153（V）mm
* Dimension: 70.5 x 43.3(mm)

## Raspberry Pi hardware connection

```
EPD  	=>	RPI(BCM)
VCC    	->    	5V
GND    	->    	GND
DIN    	->    	10(SPI0_MOSI)
CLK    	->    	11(SPI0_SCK)
CS     	->    	8(CE0)
DC     	->    	25
RST    	->    	27
BL  	->    	18
```
