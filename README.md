# automation-hat-controller-client-server

A socket based wrapper around [automation-hat](https://shop.pimoroni.com/products/automation-hat) python controller to interface with `perl`.

## Requirements
### Hardware
Using Raspi and [automation-hat](https://shop.pimoroni.com/products/automation-hat)

#### Installing drivers
Follow [https://github.com/pimoroni/automation-hat](https://github.com/pimoroni/automation-hat)

which boils down to 
```bash
sudo apt-get install pimoroni
```

And also some further Python requirements
```bash
pip3 install parsec
```

## Instructions
Run python server 
```bash
python3 controller_service.py &
```

Run `perl` code using requests library as shown in `demo_read.pl` and `demo_write.pl`
Eg.
```bash
perl demo_read.pl
```
