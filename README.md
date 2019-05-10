# Plastic Brain
> 3D real-time representation system of the brain activity.

Project created by Manik Bhattacharjee and Pierre Deman - see http://www.pyvotons.org/?page_id=377

Developed during the HUG Hackathon 2018 - see https://hackathon-hug-2018.sparkboard.com/project/5aa673d63feea30400b6362e and https://github.com/HUGrealtimeplasticbrain/realtimeEEGanalysis 

This repository is from the [2019 Brainhack Geneva hackathon](https://brainhack.ch/) and yielded the first functional prototype.

Project 07: PlasticBrain: real-time brain activity on a 3D printed brain


![](brain_sim.jpg)

## Work flow

1. Arduino + LED
2. Hardware
3. EEG Acquisition
4. EEG Filtering
5. Inverse Problem (Sources Localization)
6. Sources to LED Model
7. Communication with the hardware.

## Install
* Clone this repository:
```
git clone https://github.com/italogfernandes/xablaus.git
```
* Install the packages and dependencies...
```
pip install -r requerements.txt
```
* Charge the arduino sketch.

## Running:

* Connect the arduino to your USB port.
* Starts the EEG data stream in your local network.
* Runs the main code:
```
python BrainHackScripts/brainHack.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Authors

* **Manik Bhattacharjee**
* **Victor Ferat**
* **Jelena**
* **Gaetan**
* **Elif**
* **Jorge**
* **Italo Fernandes** - https://italogsfernandes.com - italogsfernandes@gmail.com

See also the list of [contributors](https://github.com/brainhack-ch/plastic-brain/contributors) who participated in this project.
