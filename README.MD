# RekordJog: a translator from third-party controllers to Rekordbox.

## Description

This is a reworking of timkondratiev's RekordJog project. This uses a different library to be able to control multiple Allen & Heath Xone:1D devices. You MUST have loopMIDI installed and running for this to work. You can download it [here](https://www.tobias-erichsen.de/software/loopmidi.html).

## Running the project

1. Run loopmidi, create a new device called "Pioneer DDJ-SX". This is the device that Rekordbox will see.

2. Start the app:
   `python jogger.py`

3. Select input devices (currently setup for two Xone:1D devices) and output device (Pioneer DDJ-SX).

4. Start Rekordbox and map the rest of your controls.
