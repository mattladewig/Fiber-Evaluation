# Fiber Loss Evaluation Tool
This powerful program is designed to effortlessly calculate optical loss based on the input of RX and TX power levels, measured in milliwatts (mW). Not only does it perform this calculation with precision, but it also goes the extra mile by validating the results against a predefined loss budget. With its intuitive interface and accurate calculations, this program is a must-have tool for any optical engineer or enthusiast.


## Calculating the Loss Budget for a Fiber Optic Cable Plant

Calculating the loss budget for a fiber optic link should be done as part of the initial design of the link. A loss budget will estimate the loss of the link to provide assurance that the link will support telecommunications equipment intended for use on the link. It should also be used to provide an estimated loss value to use when testing the link with a test source and power meter after installation to determine if the link has been installed correctly.

### Information Necessary to Calculate Loss Budget

The following information is needed to calculate a loss budget:
- Length of the link, end to end, in meters
- Number of connections, including connectors on each end
- Number of splices
- Fiber type (singlemode or multimode) and attenuation coefficient at each wavelength of interest

In the table below, attenuation coefficients are given from TIA-568, which is considered the worst-case, and for typical industry results. The table below shows typical loss for each component in an installed link.

#### Fiber Attenuation Coefficient

| Fiber Type | Wavelength (nm) | Max Attenuation Coefficient Per TIA-568 (dB/km) | Attenuation Coefficient (typical) (dB/km) |
|------------|------------------|-----------------------------------------------|-----------------------------------------|
| Multimode   | 850              | 3.5                                           | 3                                       |
| Multimode   | 1300             | 1.5                                           | 1                                       |
| Singlemode (Premises) | 1310 | 1.0                                           | 0.5                                     |
| Singlemode (Premises) | 1550 | 1.0                                           | 0.5                                     |
| Singlemode (Outside Plant) | 1310 | 0.5                                      | 0.4                                     |
| Singlemode (Outside Plant) | 1550 | 0.5                                      | 0.3                                     |

#### Loss of Connections and Splices

| Component | Max Loss Per TIA-568 (dB) | Typical Loss (dB) |
|-----------|---------------------------|-------------------|
| Connection (2 mated connectors) | 0.75 | 0.3 (Adhesive/polish type), 0.5-0.75 (prepolished/splice type), 0.75 (single ferrule multifiber array) |
| Splice (fusion or mechanical) | 0.3 | 0.05 (fusion), 0.3 (mechanical) |

### Manual Process

1. Calculate the loss of the fiber
2. Calculate the loss of all connections
3. Calculate the loss of all splices
4. Add all losses to get the total loss

### Calculate the Fiber Loss

Multiply the length of the fiber times the attenuation coefficient of the fiber at each wavelength of interest. Multimode fiber is calculated for 850 nm and 1300 nm. Singlemode fiber is generally calculated for 1310 nm for most premises applications and 1310 nm and 1550 nm for outside plant applications.

For example, multimode fiber at 850 nm:
- Estimated fiber loss = length in km X 3.5 dB/km (TIA Max Specification)
- or
- Estimated fiber loss = length in km X 3 dB/km (Typical Specification)

### Calculate the Connector Loss

The loss of a connection is the loss of a joint created by mating a pair of connectors. Estimates should always include the loss of the two connectors on the end of the cable plant since they will be mated to reference cables when being tested. Count the number of connections and multiply by the estimated loss of each connection.

For example, a cable plant with 3 connections plus the end connectors:
- Total connection loss = Number of connections (5) X 0.75 dB (TIA Max Specification) = 3.75 dB
- or
- Total connection loss = Number of connections (5) X 0.3 dB (Typical Specification) = 1.5 dB

### Calculate the Splice Loss

If the cable plant has splices, count the number of splices and multiply by the estimated loss of each splice. For example, a cable plant with 3 fusion splices:
- Total splice loss = Number of splices (3) X 0.3 dB (TIA Max Specification) = 0.9 dB
- or
- Total splice loss = Number of splices (3) X 0.05 dB (Typical Specification) = 0.15 dB

### Calculate the Total Cable Loss

Add the losses calculated above:
- Total fiber loss in dB = (fiber loss) + (connector loss) + (splice loss)

### Interpreting the Result

Use these numbers as estimates for "pass/fail" limits for testing. If the field-measured loss is significantly higher than the calculated value, troubleshoot the installation.


## Program Usage

```bash
python loss_calc.py --tx <transmit_power> --rx <receive_power> [--fiber_type <fiber_type>] [--wavelength <wavelength>] [--fiber_length <fiber_length>] [--num_connectors <num_connectors>] [--num_splices <num_splices>] [--json]
```

### Arguments

- `--tx <transmit_power>`: Transmission power in mW (required)
- `--rx <receive_power>`: Received power in mW (required)
- `--fiber_type <fiber_type>`: Fiber type: 's' for singlemode, 'm' for multimode
- `--wavelength <wavelength>`: Wavelength in nm
- `--fiber_length <fiber_length>`: Total length of the fiber in meters
- `--num_connectors <num_connectors>`: Number of mated connectors
- `--num_splices <num_splices>`: Number of splices
- `--json`: Output results as JSON

### Examples

1. Calculate loss and validate against loss budget:
```bash
python loss_calc.py --tx 10 --rx 5 --fiber_type s --wavelength 1310 --fiber_length 1000 --num_connectors 2 --num_splices 1
```

2. Calculate loss without validating against loss budget:
```bash
python loss_calc.py --tx 10 --rx 5
```

3. Calculate loss and output results as JSON:
```bash
python loss_calc.py --tx 10 --rx 5 --json
```

# References
- NECA301-16, Standard For Installing And Testing Fiber Optic Cables
- TIA-526-14, Optical Power Loss Measurements Of Installed Multimode Fiber Cable Plant
- TIA-526-7, Optical Power Loss Measurements Of Installed Singlemode Fiber Cable Plant

# License
 MIT License

 Copyright (c) [2024] [Matt Ladewig]

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
