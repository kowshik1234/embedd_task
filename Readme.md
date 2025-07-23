# Simple Peripheral Config Parser

## Reasoning
Choice of JSON is made for the config file to leverage the widely used parsing frameworks. Scaling with JSON is also easier for most of the MCU/MPU/Heterogenous architectures.

Python is chosen to parse for the ease of coding and demonstration. The python parser essentially takes the path of the config file and starts to perform some pattern matching using regex to quickly weed out the obvious formatting errors.

Then validate config method performs the value equivalence checks to see if the fields are containing legal values.

## How easy is it to scale?

It's rather easy to scale the JSON by just incrementing the fields and categories of peripherals. Similarly the parser script also grows in size as the peripherals type increases which could be a slight disadvantage but the brighter side being wider adaptability. 

## How to optimize further?

A "C language" based script can be written to speed up the parsing process and to simplify the C based script to read the config a simple text based config can be adopted to skip the whitespace parsing.

## How to run the parser?

`cd` into the directory and simply run `python json_parser.py`

If the json is correct, you will see the replica of the config file in the terminal else appropriate value error will be printed.

`Note - I have used AI tools as assistants to clarify my doubts and move forward when stuck while writing the script`