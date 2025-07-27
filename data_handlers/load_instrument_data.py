import os
import json
import pretty_midi
from pathlib import Path


def load_midi_files(filepath: str) -> list[Path]:
    path = Path(filepath)
    files = list(path.rglob("*.mid")) + list(path.rglob("*.midi"))
    return files


def extract_notes_from_instrument(instrument) -> list:
    notes = []
    for note in instrument.notes:
        note_data = [
            note.pitch,
            note.start,
            note.end,
            note.velocity
        ]
        notes.append(note_data)
    return notes


def save_raw_data(rawData: list, filepath: str) -> None:
    path = Path(filepath)
    data = []

    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as file:
                existingData = json.load(file)
                if isinstance(existingData, list):
                    data.extend(existingData)
        except Exception:
            data = []

    data.extend(rawData)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)



def extract_notes(config):
    files = load_midi_files(config["data_folders"]["raw_midi"])

    count = 0

    for file in files:
        try:
            midiData = pretty_midi.PrettyMIDI(str(file))
            for instrument in midiData.instruments:
                notes = extract_notes_from_instrument(instrument)
                if not notes:
                    continue
                fname = f"program_{instrument.program}.json"
                out_path = os.path.join(config["data_folders"]["raw_data"], fname)

                save_raw_data(notes, out_path)
                
            count += 1
            if count >= config["numOfMidi"]:
                break

        except Exception:
            pass

