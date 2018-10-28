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
pip3 install parsy
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

### For auto-startup

The `hat_controller.service` file describes the auto-starting service. You may have to edit the `ExecStart` field to specify the executables location.
Then, to install and enable, run...
```bash
sudo cp hat_controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hat_controller
sudo systemctl status hat_controller
```
